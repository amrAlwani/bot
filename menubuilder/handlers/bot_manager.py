"""
Handlers for adding, listing, starting, stopping, and deleting managed bots.
"""
import logging
import aiosqlite
from telegram import Update, Bot
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from config import DB_PATH, MAX_BOTS_PER_USER
from utils.keyboards import (
    bots_list_keyboard, bot_panel_keyboard, back_keyboard, confirm_keyboard
)
import utils.bot_runner as runner

logger = logging.getLogger(__name__)

WAITING_TOKEN = "waiting_bot_token"


async def show_my_bots(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM managed_bots WHERE owner_id=? ORDER BY created_at DESC",
            (user.id,)
        ) as cur:
            bots = [dict(r) for r in await cur.fetchall()]

    if not bots:
        text = (
            "🤖 <b>لا توجد بوتات مضافة</b>\n\n"
            "اضغط «➕ اضافة بوت» للبدء."
        )
    else:
        text = f"🤖 <b>بوتاتك</b> ({len(bots)} بوت):\n\nاختر بوتاً لإدارته:"

    from utils.keyboards import main_panel_keyboard
    kb = bots_list_keyboard(bots) if bots else main_panel_keyboard()
    if not bots:
        await query.edit_message_text(text, reply_markup=kb)
    else:
        await query.edit_message_text(text, reply_markup=bots_list_keyboard(bots))


async def start_add_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = update.effective_user

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT COUNT(*) as cnt FROM managed_bots WHERE owner_id=?",
            (user.id,)
        ) as cur:
            row = await cur.fetchone()
            count = row["cnt"] if row else 0

    if count >= MAX_BOTS_PER_USER:
        await query.edit_message_text(
            f"⚠️ وصلت للحد الأقصى ({MAX_BOTS_PER_USER} بوتات).\n"
            "احذف بوتاً قديماً لإضافة جديد.",
            reply_markup=back_keyboard("my_bots")
        )
        return

    context.user_data[WAITING_TOKEN] = True
    await query.edit_message_text(
        "🔑 <b>أرسل توكن البوت</b>\n\n"
        "انسخ التوكن من @BotFather وأرسله هنا:\n"
        "<code>123456789:AAF...</code>\n\n"
        "أرسل /cancel للإلغاء",
        reply_markup=back_keyboard("my_bots")
    )


async def receive_bot_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get(WAITING_TOKEN):
        return
    context.user_data.pop(WAITING_TOKEN, None)

    user = update.effective_user
    token = update.message.text.strip()
    status_msg = await update.message.reply_text("⏳ جاري التحقق من التوكن...")

    try:
        test_bot = Bot(token)
        bot_info = await test_bot.get_me()
    except TelegramError as e:
        await status_msg.edit_text(
            f"❌ <b>التوكن غير صالح</b>\n\n{e}\n\nأرسل توكناً صحيحاً أو /cancel للإلغاء"
        )
        context.user_data[WAITING_TOKEN] = True
        return

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id FROM managed_bots WHERE token=?", (token,)
        ) as cur:
            existing = await cur.fetchone()
        if existing:
            await status_msg.edit_text(
                "⚠️ هذا البوت مضاف من قبل.",
                reply_markup=back_keyboard("my_bots")
            )
            return

        await db.execute(
            "INSERT INTO managed_bots(token, bot_id, username, name, owner_id) "
            "VALUES(?,?,?,?,?)",
            (token, bot_info.id, bot_info.username, bot_info.full_name, user.id)
        )
        await db.execute(
            "INSERT INTO menus(bot_token, menu_key, title, text) VALUES(?,?,?,?)",
            (token, "main", "القائمة الرئيسية", f"🤖 أهلاً بك في {bot_info.full_name}!")
        )
        await db.commit()

    await status_msg.edit_text(
        f"✅ <b>تمت إضافة البوت بنجاح!</b>\n\n"
        f"الاسم: <b>{bot_info.full_name}</b>\n"
        f"المعرف: @{bot_info.username}\n\n"
        f"الآن يمكنك بناء القائمة وتشغيل البوت.",
        reply_markup=bot_panel_keyboard(token, False)
    )
    context.user_data["current_bot"] = token


async def show_bot_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    short = query.data.split(":", 1)[1]

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM managed_bots WHERE token LIKE ? AND owner_id=?",
            (f"{short}%", update.effective_user.id)
        ) as cur:
            bot_data = await cur.fetchone()

    if not bot_data:
        await query.edit_message_text("❌ البوت غير موجود.", reply_markup=back_keyboard("my_bots"))
        return

    bot_data = dict(bot_data)
    context.user_data["current_bot"] = bot_data["token"]
    is_active = runner.is_running(bot_data["token"])

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT COUNT(*) as cnt FROM bot_users WHERE bot_token=?",
            (bot_data["token"],)
        ) as cur:
            row = await cur.fetchone()
            user_count = row["cnt"] if row else 0

    text = (
        f"🤖 <b>{bot_data['name']}</b> (@{bot_data['username']})\n\n"
        f"الحالة: {'🟢 يعمل' if is_active else '🔴 متوقف'}\n"
        f"👥 المستخدمين: <b>{user_count}</b>\n"
        f"📅 الإضافة: <code>{bot_data['created_at'][:10]}</code>"
    )
    await query.edit_message_text(
        text,
        reply_markup=bot_panel_keyboard(bot_data["token"], is_active)
    )


async def toggle_bot_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    short = query.data.split(":", 1)[1]

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM managed_bots WHERE token LIKE ? AND owner_id=?",
            (f"{short}%", update.effective_user.id)
        ) as cur:
            bot_data = await cur.fetchone()

    if not bot_data:
        await query.answer("❌ البوت غير موجود!", show_alert=True)
        return

    bot_data = dict(bot_data)
    token = bot_data["token"]

    if runner.is_running(token):
        await query.answer("⏳ جاري الإيقاف...")
        await query.edit_message_text("⏳ جاري إيقاف البوت...")
        success = await runner.stop_child_bot(token)
        msg = "⏹️ تم إيقاف البوت" if success else "❌ فشل الإيقاف"
    else:
        await query.edit_message_text("⏳ جاري تشغيل البوت...")
        from handlers.child_bot import build_child_app
        success = await runner.start_child_bot(token, build_child_app)
        msg = "▶️ تم تشغيل البوت بنجاح!" if success else "❌ فشل التشغيل — تحقق من التوكن"

    is_active = runner.is_running(token)
    text = (
        f"🤖 <b>{bot_data['name']}</b>\n\n"
        f"{msg}\n"
        f"الحالة: {'🟢 يعمل' if is_active else '🔴 متوقف'}"
    )
    await query.edit_message_text(
        text,
        reply_markup=bot_panel_keyboard(token, is_active)
    )


async def confirm_delete_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    short = query.data.split(":", 1)[1]
    context.user_data["delete_bot_short"] = short
    await query.edit_message_text(
        "⚠️ <b>تأكيد الحذف</b>\n\nهل تريد حذف هذا البوت وجميع بياناته؟",
        reply_markup=confirm_keyboard(f"do_delete:{short}", f"bot:{short}")
    )


async def do_delete_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    short = query.data.split(":", 1)[1]

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT token FROM managed_bots WHERE token LIKE ? AND owner_id=?",
            (f"{short}%", update.effective_user.id)
        ) as cur:
            row = await cur.fetchone()

    if not row:
        await query.edit_message_text("❌ البوت غير موجود.", reply_markup=back_keyboard("my_bots"))
        return

    token = row["token"]
    if runner.is_running(token):
        await runner.stop_child_bot(token)

    async with aiosqlite.connect(DB_PATH) as db:
        for tbl in ["managed_bots", "bot_admins", "bot_users", "menus", "menu_buttons",
                    "bot_commands", "bot_settings", "shop_categories", "shop_products",
                    "cart_items", "orders", "mailing_history", "referrals"]:
            await db.execute(f"DELETE FROM {tbl} WHERE bot_token=?", (token,))
        await db.execute("DELETE FROM managed_bots WHERE token=?", (token,))
        await db.commit()

    await query.edit_message_text(
        "🗑️ تم حذف البوت وجميع بياناته.",
        reply_markup=back_keyboard("my_bots")
    )
