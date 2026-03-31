"""
Bot settings handler — maintenance mode, captcha, welcome, referral, balance.
"""
import aiosqlite
from telegram import Update
from telegram.ext import ContextTypes

from config import DB_PATH
from models.database import setting_get, setting_set
from utils.keyboards import settings_keyboard, back_keyboard

WAIT_WELCOME = "wait_welcome_msg"
WAIT_REF_BONUS = "wait_ref_bonus"


async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            await query.answer("❌ البوت غير موجود!", show_alert=True)
            return
        token = row["token"]
        context.user_data["current_bot"] = token
        context.user_data["current_short"] = short

        async with db.execute(
            "SELECT key, value FROM bot_settings WHERE bot_token=?", (token,)
        ) as cur:
            settings = {r["key"]: r["value"] for r in await cur.fetchall()}

    text = (
        "⚙️ <b>إعدادات البوت</b>\n\n"
        "اضغط على الإعداد لتفعيله أو تعطيله:"
    )
    await query.edit_message_text(text, reply_markup=settings_keyboard(token, settings))


async def toggle_setting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split(":", 2)
    key, short = parts[1], parts[2]

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT token FROM managed_bots WHERE token LIKE ? AND owner_id=?",
            (f"{short}%", update.effective_user.id)
        ) as cur:
            row = await cur.fetchone()
        if not row:
            await query.answer("❌", show_alert=True)
            return
        token = row["token"]

    current = await setting_get(token, key, "0")
    new_val = "0" if current == "1" else "1"
    await setting_set(token, key, new_val)

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT key, value FROM bot_settings WHERE bot_token=?", (token,)
        ) as cur:
            settings = {r["key"]: r["value"] for r in await cur.fetchall()}

    await query.edit_message_text(
        "⚙️ <b>إعدادات البوت</b>",
        reply_markup=settings_keyboard(token, settings)
    )


async def start_set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    short = query.data.split(":", 1)[1]
    context.user_data["settings_short"] = short
    context.user_data[WAIT_WELCOME] = True
    await query.edit_message_text(
        "✏️ <b>رسالة الترحيب</b>\n\n"
        "أرسل رسالة الترحيب الجديدة.\n"
        "متغيرات متاحة: {name} {username} {id} {ref_link}\n\n"
        "أرسل /cancel للإلغاء"
    )


async def start_set_ref_bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    short = query.data.split(":", 1)[1]
    context.user_data["settings_short"] = short
    context.user_data[WAIT_REF_BONUS] = True
    await query.edit_message_text(
        "💰 <b>مكافأة الإحالة</b>\n\n"
        "أرسل قيمة المكافأة التي يحصل عليها المستخدم عند دعوة صديق:\n"
        "(أرقام فقط، مثلاً: 10)\n\n"
        "أرسل /cancel للإلغاء"
    )


async def handle_settings_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user = update.effective_user

    if text == "/cancel":
        context.user_data.pop(WAIT_WELCOME, None)
        context.user_data.pop(WAIT_REF_BONUS, None)
        await update.message.reply_text("❌ تم الإلغاء.")
        return

    short = context.user_data.get("settings_short", "")
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT token FROM managed_bots WHERE token LIKE ? AND owner_id=?",
            (f"{short}%", user.id)
        ) as cur:
            row = await cur.fetchone()
        if not row:
            await update.message.reply_text("❌ البوت غير موجود.")
            return
        token = row["token"]

    if context.user_data.pop(WAIT_WELCOME, None):
        await setting_set(token, "welcome_text", text)
        await update.message.reply_text(
            "✅ تم حفظ رسالة الترحيب.",
            reply_markup=back_keyboard(f"bot_settings:{short}")
        )
    elif context.user_data.pop(WAIT_REF_BONUS, None):
        try:
            bonus = float(text)
            await setting_set(token, "ref_bonus", str(bonus))
            await update.message.reply_text(
                f"✅ تم تعيين مكافأة الإحالة: <b>{bonus}</b>",
                reply_markup=back_keyboard(f"bot_settings:{short}")
            )
        except ValueError:
            await update.message.reply_text("❌ أرسل رقماً صحيحاً.")
            context.user_data[WAIT_REF_BONUS] = True


async def show_bot_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            await query.answer("❌", show_alert=True)
            return
        token = row["token"]
        async with db.execute(
            "SELECT COUNT(*) as total, "
            "SUM(CASE WHEN is_blocked=0 THEN 1 ELSE 0 END) as active, "
            "SUM(CASE WHEN is_blocked=1 THEN 1 ELSE 0 END) as blocked "
            "FROM bot_users WHERE bot_token=?",
            (token,)
        ) as cur:
            stats = dict(await cur.fetchone())
        async with db.execute(
            "SELECT first_name, username, user_id, balance, joined_at "
            "FROM bot_users WHERE bot_token=? ORDER BY joined_at DESC LIMIT 10",
            (token,)
        ) as cur:
            recent = [dict(r) for r in await cur.fetchall()]

    lines = [
        f"👥 <b>مستخدمو البوت</b>\n",
        f"الإجمالي: <b>{stats['total']}</b>",
        f"النشطون: <b>{stats['active']}</b>",
        f"المحظورون: <b>{stats['blocked']}</b>\n",
        "<b>آخر 10 مستخدمين:</b>"
    ]
    for u in recent:
        uname = f"@{u['username']}" if u['username'] else u['first_name']
        lines.append(f"• {uname} | ID: <code>{u['user_id']}</code> | رصيد: {u['balance']:.1f}")
    await query.edit_message_text(
        "\n".join(lines),
        reply_markup=back_keyboard(f"bot:{short}")
    )


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    short = query.data.split(":", 1)[1]
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT token, name, username, created_at FROM managed_bots WHERE token LIKE ? AND owner_id=?",
            (f"{short}%", update.effective_user.id)
        ) as cur:
            row = await cur.fetchone()
        if not row:
            await query.answer("❌", show_alert=True)
            return
        token, name, username, created_at = row["token"], row["name"], row["username"], row["created_at"]

        async with db.execute(
            "SELECT COUNT(*) as u FROM bot_users WHERE bot_token=?", (token,)
        ) as cur:
            users = (await cur.fetchone())["u"]
        async with db.execute(
            "SELECT COUNT(*) as o FROM orders WHERE bot_token=?", (token,)
        ) as cur:
            orders = (await cur.fetchone())["o"]
        async with db.execute(
            "SELECT COUNT(*) as m FROM mailing_history WHERE bot_token=?", (token,)
        ) as cur:
            mailings = (await cur.fetchone())["m"]
        async with db.execute(
            "SELECT COUNT(*) as r FROM referrals WHERE bot_token=?", (token,)
        ) as cur:
            refs = (await cur.fetchone())["r"]

    text = (
        f"📊 <b>إحصائيات {name}</b>\n"
        f"@{username}\n\n"
        f"📅 تاريخ الإضافة: {created_at[:10]}\n"
        f"👥 المستخدمين: <b>{users}</b>\n"
        f"🛒 الطلبات: <b>{orders}</b>\n"
        f"📢 الإرسالات الجماعية: <b>{mailings}</b>\n"
        f"🔗 الإحالات: <b>{refs}</b>"
    )
    await query.edit_message_text(text, reply_markup=back_keyboard(f"bot:{short}"))


async def show_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    short = query.data.split(":", 1)[1]
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT token, owner_id FROM managed_bots WHERE token LIKE ? AND owner_id=?",
            (f"{short}%", update.effective_user.id)
        ) as cur:
            row = await cur.fetchone()
        if not row:
            await query.answer("❌", show_alert=True)
            return
        token = row["token"]
        async with db.execute(
            "SELECT user_id, added_at FROM bot_admins WHERE bot_token=? ORDER BY added_at",
            (token,)
        ) as cur:
            admins = [dict(r) for r in await cur.fetchall()]

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    lines = [f"👤 <b>مشرفو البوت</b>\n\nالمالك: <code>{row['owner_id']}</code>\n"]
    for a in admins:
        lines.append(f"• <code>{a['user_id']}</code> — {a['added_at'][:10]}")
    rows = [
        [InlineKeyboardButton("➕ اضافة مشرف", callback_data=f"add_admin:{short}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data=f"bot:{short}")],
    ]
    await query.edit_message_text(
        "\n".join(lines) or "لا يوجد مشرفون.",
        reply_markup=InlineKeyboardMarkup(rows)
    )
