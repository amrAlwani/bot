"""
Broadcast/mailing handler — sends messages to all bot users.
"""
import asyncio
import aiosqlite
import logging
from telegram import Update, Bot
from telegram.ext import ContextTypes

from config import DB_PATH, MAIL_DELAY
from utils.keyboards import back_keyboard

logger = logging.getLogger(__name__)
WAIT_BROADCAST_MSG = "wait_broadcast_msg"


async def start_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    short = query.data.split(":", 1)[1]
    context.user_data["broadcast_short"] = short
    context.user_data[WAIT_BROADCAST_MSG] = True
    await query.edit_message_text(
        "📢 <b>ارسال جماعي</b>\n\n"
        "أرسل الرسالة التي تريد إرسالها لجميع مستخدمي البوت.\n"
        "تدعم: النص، الصور، الفيديو، والملفات.\n\n"
        "أرسل /cancel للإلغاء",
        reply_markup=back_keyboard(f"bot:{short}")
    )


async def handle_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles incoming broadcast message (text or media)."""
    if not context.user_data.get(WAIT_BROADCAST_MSG):
        return
    context.user_data.pop(WAIT_BROADCAST_MSG)
    short = context.user_data.pop("broadcast_short", "")

    message = update.message
    user = update.effective_user

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT token FROM managed_bots WHERE token LIKE ? AND owner_id=?",
            (f"{short}%", user.id)
        ) as cur:
            row = await cur.fetchone()
        if not row:
            await message.reply_text("❌ البوت غير موجود.")
            return
        token = row["token"]

        async with db.execute(
            "SELECT user_id FROM bot_users WHERE bot_token=? AND is_blocked=0",
            (token,)
        ) as cur:
            users = [r["user_id"] for r in await cur.fetchall()]

    if not users:
        await message.reply_text("⚠️ لا يوجد مستخدمون لإرسال الرسالة إليهم.")
        return

    status_msg = await message.reply_text(
        f"📤 جاري الإرسال لـ {len(users)} مستخدم..."
    )
    sent = 0
    failed = 0
    bot = Bot(token)

    for uid in users:
        try:
            await _forward_message(bot, message, uid)
            sent += 1
            await asyncio.sleep(MAIL_DELAY)
        except Exception as e:
            if "blocked" in str(e).lower() or "deactivated" in str(e).lower():
                async with aiosqlite.connect(DB_PATH) as db:
                    await db.execute(
                        "UPDATE bot_users SET is_blocked=1 WHERE bot_token=? AND user_id=?",
                        (token, uid)
                    )
                    await db.commit()
            failed += 1

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO mailing_history(bot_token, message_text, sent_count, fail_count) "
            "VALUES(?,?,?,?)",
            (token, message.text or "[media]", sent, failed)
        )
        await db.commit()

    await status_msg.edit_text(
        f"✅ <b>اكتملت الاذاعة</b>\n\n"
        f"✓ تم الإرسال: <b>{sent}</b>\n"
        f"✗ فشل: <b>{failed}</b>",
        reply_markup=back_keyboard(f"bot:{short}")
    )


async def _forward_message(bot: Bot, message, chat_id: int):
    """Copy the original message to the target chat."""
    if message.text:
        await bot.send_message(chat_id, message.text, parse_mode="HTML")
    elif message.photo:
        await bot.send_photo(chat_id, message.photo[-1].file_id, caption=message.caption)
    elif message.video:
        await bot.send_video(chat_id, message.video.file_id, caption=message.caption)
    elif message.document:
        await bot.send_document(chat_id, message.document.file_id, caption=message.caption)
    elif message.audio:
        await bot.send_audio(chat_id, message.audio.file_id, caption=message.caption)
    elif message.sticker:
        await bot.send_sticker(chat_id, message.sticker.file_id)
    elif message.voice:
        await bot.send_voice(chat_id, message.voice.file_id)


async def show_mailing_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            "SELECT * FROM mailing_history WHERE bot_token=? ORDER BY created_at DESC LIMIT 10",
            (token,)
        ) as cur:
            history = [dict(r) for r in await cur.fetchall()]

    if not history:
        text = "📭 لا يوجد سجل ارسال جماعي."
    else:
        lines = ["📊 <b>آخر 10 إرسالات جماعية:</b>\n"]
        for h in history:
            lines.append(
                f"• {h['created_at'][:16]} | ✓{h['sent_count']} ✗{h['fail_count']}"
            )
        text = "\n".join(lines)
    await query.edit_message_text(text, reply_markup=back_keyboard(f"bot:{short}"))
