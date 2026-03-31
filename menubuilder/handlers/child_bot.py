"""
Child bot logic — handles /start, menu navigation, button presses,
user registration, referrals, shop browsing, and cart/orders for each managed bot.
"""
import aiosqlite
import json
import logging
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

from config import DB_PATH
from models.database import setting_get, setting_set
from utils.keyboards import (
    shop_categories_keyboard, shop_products_keyboard, back_keyboard
)
from utils.macros import process_macros

logger = logging.getLogger(__name__)


async def _register_user(token: str, user, referrer_id=None):
    """Register or update a user in the bot's user table."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id FROM bot_users WHERE bot_token=? AND user_id=?",
            (token, user.id)
        ) as cur:
            existing = await cur.fetchone()

        if not existing:
            await db.execute(
                "INSERT INTO bot_users(bot_token, user_id, username, first_name, referrer_id) "
                "VALUES(?,?,?,?,?)",
                (token, user.id, user.username, user.first_name, referrer_id)
            )
            if referrer_id:
                await db.execute(
                    "INSERT OR IGNORE INTO referrals(bot_token, referrer_id, referred_id) "
                    "VALUES(?,?,?)",
                    (token, referrer_id, user.id)
                )
                ref_bonus = await setting_get(token, "ref_bonus", "0")
                try:
                    bonus = float(ref_bonus)
                    if bonus > 0:
                        await db.execute(
                            "UPDATE bot_users SET balance=balance+? "
                            "WHERE bot_token=? AND user_id=?",
                            (bonus, token, referrer_id)
                        )
                except (ValueError, TypeError):
                    pass
        else:
            await db.execute(
                "UPDATE bot_users SET username=?, first_name=? "
                "WHERE bot_token=? AND user_id=?",
                (user.username, user.first_name, token, user.id)
            )
        await db.commit()


async def _get_user_balance(token: str, user_id: int) -> float:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT balance FROM bot_users WHERE bot_token=? AND user_id=?",
            (token, user_id)
        ) as cur:
            row = await cur.fetchone()
    return row["balance"] if row else 0.0


async def _get_users_count(token: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT COUNT(*) as cnt FROM bot_users WHERE bot_token=?", (token,)
        ) as cur:
            row = await cur.fetchone()
    return row["cnt"] if row else 0


async def _build_menu_message(token: str, menu_key: str, user, bot_username: str):
    """Build the text and keyboard for a given menu."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM menus WHERE bot_token=? AND menu_key=?",
            (token, menu_key)
        ) as cur:
            menu = await cur.fetchone()
        if not menu:
            return None, None
        menu = dict(menu)

        async with db.execute(
            "SELECT * FROM menu_buttons WHERE bot_token=? AND menu_key=? ORDER BY position, id",
            (token, menu_key)
        ) as cur:
            buttons = [dict(r) for r in await cur.fetchall()]

    balance = await _get_user_balance(token, user.id)
    users_count = await _get_users_count(token)
    text = process_macros(
        menu.get("text") or menu.get("title", ""),
        user=user,
        balance=balance,
        users_count=users_count,
        bot_username=bot_username
    )

    from utils.keyboards import build_inline_keyboard
    rows = []
    per_row = buttons[0].get("per_row", 1) if buttons else 1
    for btn in buttons:
        btype = btn.get("btn_type", "callback")
        label = btn.get("label", "—")
        if btype == "url" and btn.get("url"):
            rows.append(InlineKeyboardButton(label, url=btn["url"]))
        elif btype == "submenu" and btn.get("submenu_key"):
            rows.append(InlineKeyboardButton(label, callback_data=f"cmenu:{btn['submenu_key']}"))
        else:
            rows.append(InlineKeyboardButton(label, callback_data=f"cbtn:{btn['id']}"))

    from utils.keyboards import chunk_list
    keyboard_rows = list(chunk_list(rows, max(1, min(8, per_row))))

    if menu.get("parent_key"):
        keyboard_rows.append([InlineKeyboardButton("🔙 رجوع", callback_data=f"cmenu:{menu['parent_key']}")])
    markup = InlineKeyboardMarkup(keyboard_rows) if keyboard_rows else None
    return text, markup


async def child_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = context.bot.token
    user = update.effective_user
    args = context.args or []
    referrer_id = None

    if args and args[0].startswith("ref_"):
        try:
            referrer_id = int(args[0].split("_", 1)[1])
            if referrer_id == user.id:
                referrer_id = None
        except (ValueError, IndexError):
            pass

    await _register_user(token, user, referrer_id)

    maintenance = await setting_get(token, "maintenance", "0")
    is_admin = await _is_admin(token, user.id)

    if maintenance == "1" and not is_admin:
        maint_text = await setting_get(token, "maintenance_text", "🔧 البوت في وضع الصيانة. يرجى المحاولة لاحقاً.")
        await update.message.reply_text(maint_text)
        return

    captcha = await setting_get(token, "captcha", "0")
    if captcha == "1" and not is_admin:
        await _show_captcha(update, context, token)
        return

    welcome = await setting_get(token, "welcome_text", "")
    if not welcome:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT text FROM menus WHERE bot_token=? AND menu_key='main'", (token,)
            ) as cur:
                row = await cur.fetchone()
            welcome = row["text"] if row else f"🤖 أهلاً {user.first_name}!"

    bot_username = context.bot.username
    text, markup = await _build_menu_message(token, "main", user, bot_username)
    if text is None:
        balance = await _get_user_balance(token, user.id)
        users_count = await _get_users_count(token)
        text = process_macros(welcome, user=user, balance=balance,
                              users_count=users_count, bot_username=bot_username)
    await update.message.reply_text(text or "👋", reply_markup=markup)


async def child_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    token = context.bot.token
    user = update.effective_user
    data = query.data

    if data.startswith("cmenu:"):
        menu_key = data.split(":", 1)[1]
        text, markup = await _build_menu_message(token, menu_key, user, context.bot.username)
        if text is None:
            await query.answer("❌ القائمة غير موجودة!", show_alert=True)
            return
        await query.answer()
        await query.edit_message_text(text, reply_markup=markup)
        return

    if data.startswith("cbtn:"):
        btn_id = data.split(":", 1)[1]
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
        balance = await _get_user_balance(token, user.id)
        users_count = await _get_users_count(token)
        response = process_macros(
            btn.get("response") or btn.get("label", ""),
            user=user, balance=balance,
            users_count=users_count,
            bot_username=context.bot.username
        )
        await query.answer()
        await query.message.reply_text(response or "✅")
        return

    if data.startswith("view_cat:"):
        parts = data.split(":")
        cat_id = int(parts[2])
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM shop_products WHERE bot_token=? AND category_id=? AND is_available=1",
                (token, cat_id)
            ) as cur:
                products = [dict(r) for r in await cur.fetchall()]
        await query.answer()
        if not products:
            await query.edit_message_text("❌ لا توجد منتجات في هذا التصنيف.")
            return
        rows = []
        for p in products:
            rows.append([InlineKeyboardButton(
                f"{p['emoji']} {p['name']} — {p['price']:.2f}",
                callback_data=f"view_product:{p['id']}"
            )])
        rows.append([InlineKeyboardButton("🔙 رجوع", callback_data="shop_home")])
        await query.edit_message_text(
            "🛒 اختر منتجاً:",
            reply_markup=InlineKeyboardMarkup(rows)
        )
        return

    if data.startswith("view_product:"):
        prod_id = int(data.split(":", 1)[1])
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM shop_products WHERE id=?", (prod_id,)
            ) as cur:
                prod = await cur.fetchone()
        if not prod:
            await query.answer("❌ المنتج غير موجود!", show_alert=True)
            return
        prod = dict(prod)
        await query.answer()
        await query.edit_message_text(
            f"{prod['emoji']} <b>{prod['name']}</b>\n\n"
            f"{prod['description'] or ''}\n\n"
            f"💰 السعر: <b>{prod['price']:.2f}</b>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 اضافة للسلة", callback_data=f"add_cart:{prod_id}")],
                [InlineKeyboardButton("🔙 رجوع", callback_data=f"view_cat:{token[:20]}:{prod['category_id']}")],
            ])
        )
        return

    if data.startswith("add_cart:"):
        prod_id = int(data.split(":", 1)[1])
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT id FROM cart_items WHERE bot_token=? AND user_id=? AND product_id=?",
                (token, user.id, prod_id)
            ) as cur:
                existing = await cur.fetchone()
            if existing:
                await db.execute(
                    "UPDATE cart_items SET quantity=quantity+1 "
                    "WHERE bot_token=? AND user_id=? AND product_id=?",
                    (token, user.id, prod_id)
                )
            else:
                await db.execute(
                    "INSERT INTO cart_items(bot_token, user_id, product_id) VALUES(?,?,?)",
                    (token, user.id, prod_id)
                )
            await db.commit()
        await query.answer("✅ تمت إضافة المنتج للسلة!", show_alert=True)
        return

    if data == "cart":
        await _show_cart(query, token, user)
        return

    if data == "checkout":
        await _do_checkout(query, token, user)
        return

    if data == "shop_home":
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM shop_categories WHERE bot_token=? ORDER BY id", (token,)
            ) as cur:
                categories = [dict(r) for r in await cur.fetchall()]
        await query.answer()
        await query.edit_message_text(
            "🛒 <b>المتجر</b>\n\nاختر تصنيفاً:",
            reply_markup=shop_categories_keyboard(token, categories, for_admin=False)
        )
        return

    if data.startswith("captcha_ok:"):
        expected = data.split(":", 1)[1]
        await query.answer("✅ تم التحقق!", show_alert=True)
        text, markup = await _build_menu_message(token, "main", user, context.bot.username)
        await query.edit_message_text(text or "👋", reply_markup=markup)
        return

    await query.answer()


async def _show_cart(query, token: str, user):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT ci.quantity, sp.name, sp.price, sp.emoji "
            "FROM cart_items ci JOIN shop_products sp ON ci.product_id=sp.id "
            "WHERE ci.bot_token=? AND ci.user_id=?",
            (token, user.id)
        ) as cur:
            items = [dict(r) for r in await cur.fetchall()]

    if not items:
        await query.answer("🛒 السلة فارغة!", show_alert=True)
        return
    total = sum(i["price"] * i["quantity"] for i in items)
    lines = ["🛒 <b>سلة التسوق</b>\n"]
    for item in items:
        lines.append(f"• {item['emoji']} {item['name']} × {item['quantity']} = {item['price'] * item['quantity']:.2f}")
    lines.append(f"\n💰 الإجمالي: <b>{total:.2f}</b>")
    await query.answer()
    await query.edit_message_text(
        "\n".join(lines),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ تأكيد الطلب", callback_data="checkout")],
            [InlineKeyboardButton("🗑️ تفريغ السلة", callback_data="clear_cart")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="shop_home")],
        ])
    )


async def _do_checkout(query, token: str, user):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT ci.product_id, ci.quantity, sp.name, sp.price "
            "FROM cart_items ci JOIN shop_products sp ON ci.product_id=sp.id "
            "WHERE ci.bot_token=? AND ci.user_id=?",
            (token, user.id)
        ) as cur:
            items = [dict(r) for r in await cur.fetchall()]

        if not items:
            await query.answer("🛒 السلة فارغة!", show_alert=True)
            return

        total = sum(i["price"] * i["quantity"] for i in items)
        items_json = json.dumps(items, ensure_ascii=False)
        await db.execute(
            "INSERT INTO orders(bot_token, user_id, items_json, total) VALUES(?,?,?,?)",
            (token, user.id, items_json, total)
        )
        await db.execute(
            "DELETE FROM cart_items WHERE bot_token=? AND user_id=?",
            (token, user.id)
        )
        await db.commit()

    await query.answer("✅ تم تأكيد طلبك!", show_alert=True)
    await query.edit_message_text(
        f"✅ <b>تم استلام طلبك</b>\n\n"
        f"المبلغ الإجمالي: <b>{total:.2f}</b>\n"
        f"سيتم التواصل معك قريباً.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 الرئيسية", callback_data="cmenu:main")]
        ])
    )


async def _is_admin(token: str, user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id FROM managed_bots WHERE token=? AND owner_id=?",
            (token, user_id)
        ) as cur:
            if await cur.fetchone():
                return True
        async with db.execute(
            "SELECT id FROM bot_admins WHERE bot_token=? AND user_id=?",
            (token, user_id)
        ) as cur:
            return bool(await cur.fetchone())


async def _show_captcha(update, context, token: str):
    import random
    a, b = random.randint(1, 9), random.randint(1, 9)
    correct = a + b
    options = list({correct, random.randint(1, 18), random.randint(1, 18), random.randint(1, 18)})
    random.shuffle(options)
    rows = [[InlineKeyboardButton(str(o), callback_data=f"captcha_ok:{o}" if o == correct else f"captcha_fail:{o}") for o in options]]
    await update.message.reply_text(
        f"🤖 <b>التحقق من الهوية</b>\n\nكم يساوي {a} + {b}؟",
        reply_markup=InlineKeyboardMarkup(rows)
    )


async def child_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    token = context.bot.token
    user = update.effective_user
    await _register_user(token, user)
    text, markup = await _build_menu_message(token, "main", user, context.bot.username)
    await update.message.reply_text(text or "👋 أرسل /start للبدء", reply_markup=markup)


async def build_child_app(token: str) -> Application:
    """Build and configure a child bot Application."""
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", child_start))
    app.add_handler(CommandHandler("help", child_help))
    app.add_handler(CommandHandler("menu", child_help))
    app.add_handler(CallbackQueryHandler(child_menu_callback))
    return app
