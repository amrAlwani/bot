from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List, Optional


def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def build_inline_keyboard(buttons_data: List[dict]) -> InlineKeyboardMarkup:
    """
    Build InlineKeyboardMarkup from a list of button dicts.
    Each dict: {label, btn_type, url, callback_data, per_row}
    """
    if not buttons_data:
        return InlineKeyboardMarkup([])

    per_row = buttons_data[0].get("per_row", 1) if buttons_data else 1
    all_buttons = []

    for btn in buttons_data:
        btype = btn.get("btn_type", "callback")
        label = btn.get("label", "—")

        if btype == "url" and btn.get("url"):
            all_buttons.append(InlineKeyboardButton(label, url=btn["url"]))
        elif btype == "submenu" and btn.get("submenu_key"):
            all_buttons.append(InlineKeyboardButton(label, callback_data=f"menu:{btn['submenu_key']}"))
        else:
            cd = btn.get("callback_data") or f"btn:{btn.get('id', label)}"
            all_buttons.append(InlineKeyboardButton(label, callback_data=cd))

    per_row = max(1, min(8, per_row))
    rows = list(chunk_list(all_buttons, per_row))
    return InlineKeyboardMarkup(rows)


def main_panel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 بوتاتي", callback_data="my_bots"),
         InlineKeyboardButton("➕ اضافة بوت", callback_data="add_bot")],
        [InlineKeyboardButton("📖 كيف أبدأ؟", callback_data="help"),
         InlineKeyboardButton("📊 احصائياتي", callback_data="my_stats")],
    ])


def bots_list_keyboard(bots: list) -> InlineKeyboardMarkup:
    rows = []
    for bot in bots:
        status = "🟢" if bot["is_active"] else "🔴"
        name = bot["name"] or bot["username"] or "بوت"
        rows.append([InlineKeyboardButton(
            f"{status} {name}",
            callback_data=f"bot:{bot['token'][:20]}"
        )])
    rows.append([InlineKeyboardButton("🏠 الرئيسية", callback_data="home")])
    return InlineKeyboardMarkup(rows)


def bot_panel_keyboard(token: str, is_active: bool) -> InlineKeyboardMarkup:
    short = token[:20]
    toggle = "⏹️ ايقاف" if is_active else "▶️ تشغيل"
    toggle_cb = f"stop_bot:{short}" if is_active else f"start_bot:{short}"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(toggle, callback_data=toggle_cb)],
        [InlineKeyboardButton("📋 القائمة الرئيسية", callback_data=f"menu_list:{short}"),
         InlineKeyboardButton("⚙️ الإعدادات", callback_data=f"bot_settings:{short}")],
        [InlineKeyboardButton("📢 ارسال جماعي", callback_data=f"broadcast:{short}"),
         InlineKeyboardButton("👥 المستخدمين", callback_data=f"bot_users:{short}")],
        [InlineKeyboardButton("🛒 المتجر", callback_data=f"shop:{short}"),
         InlineKeyboardButton("👤 المشرفين", callback_data=f"admins:{short}")],
        [InlineKeyboardButton("📊 الاحصائيات", callback_data=f"stats:{short}"),
         InlineKeyboardButton("🗑️ حذف البوت", callback_data=f"delete_bot:{short}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="my_bots")],
    ])


def menu_list_keyboard(token: str, menus: list) -> InlineKeyboardMarkup:
    short = token[:20]
    rows = []
    for m in menus:
        rows.append([InlineKeyboardButton(
            f"📋 {m['title']}",
            callback_data=f"edit_menu:{short}:{m['menu_key']}"
        )])
    rows.append([InlineKeyboardButton("➕ قائمة جديدة", callback_data=f"new_menu:{short}")])
    rows.append([InlineKeyboardButton("🔙 رجوع", callback_data=f"bot:{short}")])
    return InlineKeyboardMarkup(rows)


def menu_edit_keyboard(token: str, menu_key: str, buttons: list) -> InlineKeyboardMarkup:
    short = token[:20]
    rows = []
    for btn in buttons:
        rows.append([InlineKeyboardButton(
            f"🔘 {btn['label']}",
            callback_data=f"edit_btn:{short}:{btn['id']}"
        )])
    rows += [
        [InlineKeyboardButton("➕ اضافة زر", callback_data=f"new_btn:{short}:{menu_key}"),
         InlineKeyboardButton("✏️ تعديل النص", callback_data=f"edit_menu_text:{short}:{menu_key}")],
        [InlineKeyboardButton("🗑️ حذف القائمة", callback_data=f"del_menu:{short}:{menu_key}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data=f"menu_list:{short}")],
    ]
    return InlineKeyboardMarkup(rows)


def btn_type_keyboard(token: str, menu_key: str) -> InlineKeyboardMarkup:
    short = token[:20]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 رد نصي", callback_data=f"btntype:callback:{short}:{menu_key}"),
         InlineKeyboardButton("🔗 رابط", callback_data=f"btntype:url:{short}:{menu_key}")],
        [InlineKeyboardButton("📂 قائمة فرعية", callback_data=f"btntype:submenu:{short}:{menu_key}")],
        [InlineKeyboardButton("❌ الغاء", callback_data=f"edit_menu:{short}:{menu_key}")],
    ])


def settings_keyboard(token: str, settings: dict) -> InlineKeyboardMarkup:
    short = token[:20]
    maint = "✅ وضع الصيانة: تشغيل" if settings.get("maintenance") == "1" else "⬜ وضع الصيانة: ايقاف"
    captcha = "✅ الكابتشا: تشغيل" if settings.get("captcha") == "1" else "⬜ الكابتشا: ايقاف"
    shop = "✅ المتجر: تشغيل" if settings.get("shop_enabled") == "1" else "⬜ المتجر: ايقاف"
    balance = "✅ الرصيد: تشغيل" if settings.get("balance_enabled") == "1" else "⬜ الرصيد: ايقاف"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(maint, callback_data=f"toggle:maintenance:{short}")],
        [InlineKeyboardButton(captcha, callback_data=f"toggle:captcha:{short}")],
        [InlineKeyboardButton(shop, callback_data=f"toggle:shop_enabled:{short}")],
        [InlineKeyboardButton(balance, callback_data=f"toggle:balance_enabled:{short}")],
        [InlineKeyboardButton("✏️ رسالة الترحيب", callback_data=f"set_welcome:{short}")],
        [InlineKeyboardButton("💰 مكافأة الإحالة", callback_data=f"set_ref_bonus:{short}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data=f"bot:{short}")],
    ])


def back_keyboard(cb: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data=cb)]])


def confirm_keyboard(yes_cb: str, no_cb: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ تأكيد", callback_data=yes_cb),
        InlineKeyboardButton("❌ الغاء", callback_data=no_cb),
    ]])


def shop_categories_keyboard(token: str, categories: list, for_admin=False) -> InlineKeyboardMarkup:
    short = token[:20]
    rows = []
    for cat in categories:
        label = f"{cat['emoji']} {cat['name']}"
        if for_admin:
            rows.append([InlineKeyboardButton(label, callback_data=f"shopcat:{short}:{cat['id']}")])
        else:
            rows.append([InlineKeyboardButton(label, callback_data=f"view_cat:{short}:{cat['id']}")])
    if for_admin:
        rows.append([InlineKeyboardButton("➕ تصنيف جديد", callback_data=f"new_cat:{short}")])
        rows.append([InlineKeyboardButton("🔙 رجوع", callback_data=f"bot:{short}")])
    else:
        rows.append([InlineKeyboardButton("🛒 سلة التسوق", callback_data=f"cart:{short}")])
    return InlineKeyboardMarkup(rows)


def shop_products_keyboard(token: str, cat_id: int, products: list) -> InlineKeyboardMarkup:
    short = token[:20]
    rows = []
    for p in products:
        avail = "✅" if p["is_available"] else "❌"
        rows.append([InlineKeyboardButton(
            f"{avail} {p['emoji']} {p['name']} — {p['price']:.2f}",
            callback_data=f"product:{short}:{p['id']}"
        )])
    rows.append([InlineKeyboardButton("➕ منتج جديد", callback_data=f"new_product:{short}:{cat_id}")])
    rows.append([InlineKeyboardButton("🔙 رجوع", callback_data=f"shop:{short}")])
    return InlineKeyboardMarkup(rows)
