"""
Handlers for building and editing bot menus and buttons.
"""
import aiosqlite
from telegram import Update
from telegram.ext import ContextTypes

from config import DB_PATH
from utils.keyboards import (
    menu_list_keyboard, menu_edit_keyboard, btn_type_keyboard,
    back_keyboard, confirm_keyboard
)

WAIT_MENU_TITLE = "wait_menu_title"
WAIT_MENU_TEXT = "wait_menu_text"
WAIT_BTN_LABEL = "wait_btn_label"
WAIT_BTN_RESPONSE = "wait_btn_response"
WAIT_BTN_URL = "wait_btn_url"


async def show_menu_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

        async with db.execute(
            "SELECT * FROM menus WHERE bot_token=? ORDER BY id",
            (token,)
        ) as cur:
            menus = [dict(r) for r in await cur.fetchall()]

    await query.edit_message_text(
        f"📋 <b>القوائم</b> ({len(menus)}):\n\nاختر قائمة لتعديلها أو أضف قائمة جديدة:",
        reply_markup=menu_list_keyboard(token, menus)
    )


async def start_new_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    short = query.data.split(":", 1)[1]
    context.user_data[WAIT_MENU_TITLE] = short
    await query.edit_message_text(
        "📋 <b>قائمة جديدة</b>\n\nأرسل اسم/عنوان القائمة الجديدة:\n\nأرسل /cancel للإلغاء"
    )


async def show_menu_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split(":", 2)
    short, menu_key = parts[1], parts[2]

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
        context.user_data["current_menu_key"] = menu_key

        async with db.execute(
            "SELECT * FROM menus WHERE bot_token=? AND menu_key=?", (token, menu_key)
        ) as cur:
            menu = await cur.fetchone()

        async with db.execute(
            "SELECT * FROM menu_buttons WHERE bot_token=? AND menu_key=? ORDER BY position, id",
            (token, menu_key)
        ) as cur:
            buttons = [dict(r) for r in await cur.fetchall()]

    if not menu:
        await query.answer("❌ القائمة غير موجودة!", show_alert=True)
        return
    menu = dict(menu)
    text = (
        f"📋 <b>تعديل القائمة: {menu['title']}</b>\n\n"
        f"النص: {menu['text'] or '(لا يوجد)'}\n"
        f"الأزرار: {len(buttons)}"
    )
    await query.edit_message_text(
        text,
        reply_markup=menu_edit_keyboard(token, menu_key, buttons)
    )


async def start_new_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split(":", 2)
    short, menu_key = parts[1], parts[2]
    context.user_data["new_btn_short"] = short
    context.user_data["new_btn_menu_key"] = menu_key
    await query.edit_message_text(
        "🔘 <b>زر جديد</b>\n\nأرسل نص الزر (ما يظهر للمستخدم):\n\nأرسل /cancel للإلغاء"
    )
    context.user_data[WAIT_BTN_LABEL] = True


async def start_edit_menu_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split(":", 2)
    short, menu_key = parts[1], parts[2]
    context.user_data["edit_menu_text_short"] = short
    context.user_data["edit_menu_text_key"] = menu_key
    context.user_data[WAIT_MENU_TEXT] = True
    await query.edit_message_text(
        "✏️ أرسل النص الجديد لهذه القائمة.\n"
        "يمكنك استخدام: {name} {username} {balance}\n\n"
        "أرسل /cancel للإلغاء"
    )


async def confirm_del_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split(":", 2)
    short, menu_key = parts[1], parts[2]
    context.user_data["del_menu_short"] = short
    context.user_data["del_menu_key"] = menu_key
    await query.edit_message_text(
        f"⚠️ هل تريد حذف قائمة <b>{menu_key}</b> وجميع أزرارها؟",
        reply_markup=confirm_keyboard(
            f"do_del_menu:{short}:{menu_key}",
            f"edit_menu:{short}:{menu_key}"
        )
    )


async def do_del_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split(":", 2)
    short, menu_key = parts[1], parts[2]

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
        if menu_key == "main":
            await query.answer("❌ لا يمكن حذف القائمة الرئيسية!", show_alert=True)
            return
        await db.execute(
            "DELETE FROM menu_buttons WHERE bot_token=? AND menu_key=?", (token, menu_key)
        )
        await db.execute(
            "DELETE FROM menus WHERE bot_token=? AND menu_key=?", (token, menu_key)
        )
        await db.commit()
    await query.edit_message_text(
        "🗑️ تم حذف القائمة.",
        reply_markup=back_keyboard(f"menu_list:{short}")
    )


async def show_edit_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split(":", 2)
    short, btn_id = parts[1], parts[2]

    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM menu_buttons WHERE id=?", (btn_id,)
        ) as cur:
            btn = await cur.fetchone()
    if not btn:
        await query.answer("❌ الزر غير موجود!", show_alert=True)
        return
    btn = dict(btn)
    text = (
        f"🔘 <b>تعديل الزر</b>\n\n"
        f"النص: <b>{btn['label']}</b>\n"
        f"النوع: {btn['btn_type']}\n"
        f"الرد: {btn['response'] or btn['url'] or btn['submenu_key'] or '—'}"
    )
    await query.edit_message_text(text, reply_markup=_btn_actions_kb(short, btn))


def _btn_actions_kb(short: str, btn: dict):
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✏️ تعديل النص", callback_data=f"edit_btn_label:{short}:{btn['id']}"),
         InlineKeyboardButton("✏️ تعديل الرد", callback_data=f"edit_btn_resp:{short}:{btn['id']}")],
        [InlineKeyboardButton("🗑️ حذف", callback_data=f"del_btn:{short}:{btn['id']}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data=f"edit_menu:{short}:{btn['menu_key']}")],
    ])


async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles all text inputs for the menu builder conversation flow."""
    text = update.message.text.strip()
    user = update.effective_user

    if text == "/cancel":
        for k in [WAIT_MENU_TITLE, WAIT_MENU_TEXT, WAIT_BTN_LABEL,
                  WAIT_BTN_RESPONSE, WAIT_BTN_URL, "btn_type_pending"]:
            context.user_data.pop(k, None)
        await update.message.reply_text("❌ تم الإلغاء.")
        return

    if context.user_data.get(WAIT_MENU_TITLE):
        short = context.user_data.pop(WAIT_MENU_TITLE)
        await _create_menu(update, context, short, text)
        return

    if context.user_data.get(WAIT_MENU_TEXT):
        context.user_data.pop(WAIT_MENU_TEXT)
        short = context.user_data.get("edit_menu_text_short", "")
        menu_key = context.user_data.get("edit_menu_text_key", "")
        await _save_menu_text(update, context, short, menu_key, text)
        return

    if context.user_data.get(WAIT_BTN_LABEL):
        context.user_data.pop(WAIT_BTN_LABEL)
        context.user_data["pending_btn_label"] = text
        short = context.user_data.get("new_btn_short", "")
        menu_key = context.user_data.get("new_btn_menu_key", "")
        await update.message.reply_text(
            f"🔘 الزر: <b>{text}</b>\n\nاختر نوع الزر:",
            reply_markup=btn_type_keyboard(short, menu_key)
        )
        return

    if context.user_data.get(WAIT_BTN_RESPONSE):
        context.user_data.pop(WAIT_BTN_RESPONSE)
        await _save_btn_response(update, context, text)
        return

    if context.user_data.get(WAIT_BTN_URL):
        context.user_data.pop(WAIT_BTN_URL)
        await _save_btn_url(update, context, text)
        return


async def _create_menu(update, context, short, title):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT token FROM managed_bots WHERE token LIKE ? AND owner_id=?",
            (f"{short}%", update.effective_user.id)
        ) as cur:
            row = await cur.fetchone()
        if not row:
            await update.message.reply_text("❌ البوت غير موجود.")
            return
        token = row["token"]
        import re
        menu_key = f"menu_{re.sub(r'[^a-z0-9]', '', title.lower())[:15]}_{update.effective_user.id % 1000}"
        async with db.execute(
            "SELECT id FROM menus WHERE bot_token=? AND menu_key=?", (token, menu_key)
        ) as cur:
            if await cur.fetchone():
                menu_key += "_2"
        await db.execute(
            "INSERT INTO menus(bot_token, menu_key, title, text) VALUES(?,?,?,?)",
            (token, menu_key, title, f"📋 {title}")
        )
        await db.commit()
    await update.message.reply_text(
        f"✅ تم إنشاء القائمة <b>{title}</b>",
        reply_markup=menu_edit_keyboard(token, menu_key, [])
    )


async def _save_menu_text(update, context, short, menu_key, text):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT token FROM managed_bots WHERE token LIKE ? AND owner_id=?",
            (f"{short}%", update.effective_user.id)
        ) as cur:
            row = await cur.fetchone()
        if not row:
            await update.message.reply_text("❌ البوت غير موجود.")
            return
        token = row["token"]
        await db.execute(
            "UPDATE menus SET text=? WHERE bot_token=? AND menu_key=?",
            (text, token, menu_key)
        )
        await db.commit()
    await update.message.reply_text(
        "✅ تم تحديث نص القائمة.",
        reply_markup=back_keyboard(f"menu_list:{short}")
    )


async def handle_btn_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split(":")
    btn_type, short, menu_key = parts[1], parts[2], parts[3]
    context.user_data["btn_type_pending"] = btn_type
    context.user_data["new_btn_short"] = short
    context.user_data["new_btn_menu_key"] = menu_key

    if btn_type == "callback":
        context.user_data[WAIT_BTN_RESPONSE] = True
        await query.edit_message_text(
            "💬 أرسل نص الرد الذي سيظهر عند الضغط على الزر:\n\n"
            "يمكنك استخدام {name} {balance} {id}\n\nأرسل /cancel للإلغاء"
        )
    elif btn_type == "url":
        context.user_data[WAIT_BTN_URL] = True
        await query.edit_message_text(
            "🔗 أرسل الرابط الذي سيفتح عند الضغط على الزر:\n"
            "(يجب أن يبدأ بـ https://)\n\nأرسل /cancel للإلغاء"
        )
    elif btn_type == "submenu":
        await _save_btn_submenu(query, context, short, menu_key)


async def _save_btn_response(update, context, response):
    short = context.user_data.get("new_btn_short", "")
    menu_key = context.user_data.get("new_btn_menu_key", "")
    label = context.user_data.get("pending_btn_label", "زر")
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT token FROM managed_bots WHERE token LIKE ? AND owner_id=?",
            (f"{short}%", update.effective_user.id)
        ) as cur:
            row = await cur.fetchone()
        if not row:
            await update.message.reply_text("❌ البوت غير موجود.")
            return
        token = row["token"]
        async with db.execute(
            "SELECT MAX(position) as mp FROM menu_buttons WHERE bot_token=? AND menu_key=?",
            (token, menu_key)
        ) as cur:
            r = await cur.fetchone()
            pos = (r["mp"] or 0) + 1
        await db.execute(
            "INSERT INTO menu_buttons(bot_token,menu_key,label,btn_type,response,position) "
            "VALUES(?,?,?,?,?,?)",
            (token, menu_key, label, "callback", response, pos)
        )
        await db.commit()
    await update.message.reply_text(
        f"✅ تم إضافة الزر <b>{label}</b>",
        reply_markup=back_keyboard(f"edit_menu:{short}:{menu_key}")
    )


async def _save_btn_url(update, context, url):
    short = context.user_data.get("new_btn_short", "")
    menu_key = context.user_data.get("new_btn_menu_key", "")
    label = context.user_data.get("pending_btn_label", "رابط")
    if not url.startswith("http"):
        await update.message.reply_text("❌ الرابط يجب أن يبدأ بـ https://")
        context.user_data[WAIT_BTN_URL] = True
        return
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT token FROM managed_bots WHERE token LIKE ? AND owner_id=?",
            (f"{short}%", update.effective_user.id)
        ) as cur:
            row = await cur.fetchone()
        if not row:
            await update.message.reply_text("❌ البوت غير موجود.")
            return
        token = row["token"]
        async with db.execute(
            "SELECT MAX(position) as mp FROM menu_buttons WHERE bot_token=? AND menu_key=?",
            (token, menu_key)
        ) as cur:
            r = await cur.fetchone()
            pos = (r["mp"] or 0) + 1
        await db.execute(
            "INSERT INTO menu_buttons(bot_token,menu_key,label,btn_type,url,position) "
            "VALUES(?,?,?,?,?,?)",
            (token, menu_key, label, "url", url, pos)
        )
        await db.commit()
    await update.message.reply_text(
        f"✅ تم إضافة الزر <b>{label}</b> (رابط)",
        reply_markup=back_keyboard(f"edit_menu:{short}:{menu_key}")
    )


async def _save_btn_submenu(query, context, short, parent_key):
    label = context.user_data.get("pending_btn_label", "قائمة فرعية")
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT token FROM managed_bots WHERE token LIKE ?",
            (f"{short}%",)
        ) as cur:
            row = await cur.fetchone()
        if not row:
            await query.answer("❌", show_alert=True)
            return
        token = row["token"]
        import re
        sub_key = f"sub_{re.sub(r'[^a-z0-9]', '', label.lower())[:12]}_{query.from_user.id % 100}"
        await db.execute(
            "INSERT OR IGNORE INTO menus(bot_token, menu_key, title, text, parent_key) "
            "VALUES(?,?,?,?,?)",
            (token, sub_key, label, f"📂 {label}", parent_key)
        )
        async with db.execute(
            "SELECT MAX(position) as mp FROM menu_buttons WHERE bot_token=? AND menu_key=?",
            (token, parent_key)
        ) as cur:
            r = await cur.fetchone()
            pos = (r["mp"] or 0) + 1
        await db.execute(
            "INSERT INTO menu_buttons(bot_token,menu_key,label,btn_type,submenu_key,position) "
            "VALUES(?,?,?,?,?,?)",
            (token, parent_key, label, "submenu", sub_key, pos)
        )
        await db.commit()
    await query.edit_message_text(
        f"✅ تم إنشاء القائمة الفرعية <b>{label}</b>",
        reply_markup=back_keyboard(f"edit_menu:{short}:{parent_key}")
    )


async def del_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split(":", 2)
    short, btn_id = parts[1], parts[2]
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT menu_key FROM menu_buttons WHERE id=?", (btn_id,)) as cur:
            row = await cur.fetchone()
        if row:
            menu_key = row["menu_key"]
            await db.execute("DELETE FROM menu_buttons WHERE id=?", (btn_id,))
            await db.commit()
            await query.edit_message_text(
                "🗑️ تم حذف الزر.",
                reply_markup=back_keyboard(f"edit_menu:{short}:{menu_key}")
            )
        else:
            await query.answer("❌ الزر غير موجود!", show_alert=True)
