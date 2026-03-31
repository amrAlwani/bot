"""
Main bot /start handler and home panel.
"""
import aiosqlite
from telegram import Update
from telegram.ext import ContextTypes
from config import DB_PATH, MAIN_BOT_ADMIN
from utils.keyboards import main_panel_keyboard


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user:
        return
    text = (
        f"👋 أهلاً <b>{user.first_name}</b>!\n\n"
        "🤖 <b>MenuBuilder Bot</b> — منشئ بوتات القوائم\n\n"
        "• أضف بوتك عبر توكن BotFather\n"
        "• صمّم قوائم وأزرار بدون برمجة\n"
        "• أرسل رسائل جماعية لمستخدميك\n"
        "• أدر متجراً داخل بوتك\n\n"
        "اختر من الأسفل للبدء:"
    )
    await update.message.reply_text(text, reply_markup=main_panel_keyboard())


async def show_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = update.effective_user
    text = (
        f"🏠 <b>الصفحة الرئيسية</b>\n\n"
        f"مرحباً {user.first_name}!"
    )
    await query.edit_message_text(text, reply_markup=main_panel_keyboard())


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "📖 <b>كيف تبدأ؟</b>\n\n"
        "<b>1.</b> اذهب إلى @BotFather وأنشئ بوتاً جديداً\n"
        "<b>2.</b> انسخ التوكن (API Token)\n"
        "<b>3.</b> اضغط «➕ اضافة بوت» وأرسل التوكن\n"
        "<b>4.</b> ابنِ قائمتك بالأزرار التي تريدها\n"
        "<b>5.</b> شغّل بوتك وشاركه مع مستخدميك!\n\n"
        "<b>المتغيرات المتاحة في الرسائل:</b>\n"
        "• <code>{name}</code> — اسم المستخدم\n"
        "• <code>{username}</code> — معرّف المستخدم\n"
        "• <code>{id}</code> — رقم المستخدم\n"
        "• <code>{balance}</code> — رصيد المستخدم\n"
        "• <code>{users}</code> — عدد المستخدمين\n"
        "• <code>{ref_link}</code> — رابط الإحالة"
    )
    from utils.keyboards import back_keyboard
    await query.edit_message_text(text, reply_markup=back_keyboard("home"))


async def show_my_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            bot_count = row["cnt"] if row else 0
        async with db.execute(
            "SELECT SUM(u.cnt) as total FROM "
            "(SELECT COUNT(*) as cnt FROM bot_users bu "
            "JOIN managed_bots mb ON bu.bot_token=mb.token "
            "WHERE mb.owner_id=?) u",
            (user.id,)
        ) as cur:
            row = await cur.fetchone()
            user_count = row["total"] or 0
    text = (
        f"📊 <b>إحصائياتك</b>\n\n"
        f"🤖 البوتات: <b>{bot_count}</b>\n"
        f"👥 إجمالي المستخدمين: <b>{user_count}</b>"
    )
    from utils.keyboards import back_keyboard
    await query.edit_message_text(text, reply_markup=back_keyboard("home"))
