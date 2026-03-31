"""
eShop handler — categories, products, cart, and orders management.
"""
import aiosqlite
import json
from telegram import Update
from telegram.ext import ContextTypes

from config import DB_PATH
from utils.keyboards import (
    shop_categories_keyboard, shop_products_keyboard, back_keyboard, confirm_keyboard
)

WAIT_CAT_NAME = "wait_cat_name"
WAIT_CAT_EMOJI = "wait_cat_emoji"
WAIT_PROD_NAME = "wait_prod_name"
WAIT_PROD_PRICE = "wait_prod_price"
WAIT_PROD_DESC = "wait_prod_desc"


async def show_shop_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            "SELECT * FROM shop_categories WHERE bot_token=? ORDER BY id",
            (token,)
        ) as cur:
            categories = [dict(r) for r in await cur.fetchall()]

    text = (
        "🛒 <b>إدارة المتجر</b>\n\n"
        f"التصنيفات: {len(categories)}\n\n"
        "اختر تصنيفاً لإدارة منتجاته أو أضف تصنيفاً جديداً:"
    )
    await query.edit_message_text(
        text,
        reply_markup=shop_categories_keyboard(token, categories, for_admin=True)
    )


async def start_new_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    short = query.data.split(":", 1)[1]
    context.user_data["shop_short"] = short
    context.user_data[WAIT_CAT_NAME] = True
    await query.edit_message_text(
        "📦 <b>تصنيف جديد</b>\n\nأرسل اسم التصنيف:\n\nأرسل /cancel للإلغاء"
    )


async def show_category_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split(":", 2)
    short, cat_id = parts[1], int(parts[2])

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
        context.user_data["current_bot"] = token
        context.user_data["current_cat_id"] = cat_id

        async with db.execute(
            "SELECT * FROM shop_categories WHERE id=?", (cat_id,)
        ) as cur:
            cat = await cur.fetchone()
        async with db.execute(
            "SELECT * FROM shop_products WHERE bot_token=? AND category_id=? ORDER BY id",
            (token, cat_id)
        ) as cur:
            products = [dict(r) for r in await cur.fetchall()]

    if not cat:
        await query.answer("❌ التصنيف غير موجود!", show_alert=True)
        return
    cat = dict(cat)
    text = (
        f"🛒 <b>{cat['emoji']} {cat['name']}</b>\n\n"
        f"المنتجات: {len(products)}"
    )
    await query.edit_message_text(
        text,
        reply_markup=shop_products_keyboard(token, cat_id, products)
    )


async def start_new_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split(":", 2)
    short, cat_id = parts[1], int(parts[2])
    context.user_data["shop_short"] = short
    context.user_data["new_prod_cat"] = cat_id
    context.user_data[WAIT_PROD_NAME] = True
    await query.edit_message_text(
        "🛍️ <b>منتج جديد</b>\n\nأرسل اسم المنتج:\n\nأرسل /cancel للإلغاء"
    )


async def handle_shop_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user = update.effective_user

    if text == "/cancel":
        for k in [WAIT_CAT_NAME, WAIT_CAT_EMOJI, WAIT_PROD_NAME, WAIT_PROD_PRICE, WAIT_PROD_DESC]:
            context.user_data.pop(k, None)
        await update.message.reply_text("❌ تم الإلغاء.")
        return

    short = context.user_data.get("shop_short", "")
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

    if context.user_data.pop(WAIT_CAT_NAME, None):
        context.user_data["new_cat_name"] = text
        context.user_data[WAIT_CAT_EMOJI] = True
        await update.message.reply_text(
            f"التصنيف: <b>{text}</b>\n\nأرسل إيموجي للتصنيف (مثلاً: 📱 أو 👗):"
        )
        return

    if context.user_data.pop(WAIT_CAT_EMOJI, None):
        name = context.user_data.pop("new_cat_name", "تصنيف")
        emoji = text if len(text) <= 5 else "📦"
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO shop_categories(bot_token, name, emoji) VALUES(?,?,?)",
                (token, name, emoji)
            )
            await db.commit()
        await update.message.reply_text(
            f"✅ تم إضافة التصنيف {emoji} <b>{name}</b>",
            reply_markup=back_keyboard(f"shop:{short}")
        )
        return

    if context.user_data.pop(WAIT_PROD_NAME, None):
        context.user_data["new_prod_name"] = text
        context.user_data[WAIT_PROD_DESC] = True
        await update.message.reply_text(
            f"المنتج: <b>{text}</b>\n\nأرسل وصفاً للمنتج (أو أرسل - للتخطي):"
        )
        return

    if context.user_data.pop(WAIT_PROD_DESC, None):
        context.user_data["new_prod_desc"] = "" if text == "-" else text
        context.user_data[WAIT_PROD_PRICE] = True
        await update.message.reply_text("💰 أرسل سعر المنتج (أرقام فقط):")
        return

    if context.user_data.pop(WAIT_PROD_PRICE, None):
        try:
            price = float(text)
        except ValueError:
            await update.message.reply_text("❌ أرسل رقماً صحيحاً للسعر.")
            context.user_data[WAIT_PROD_PRICE] = True
            return
        name = context.user_data.pop("new_prod_name", "منتج")
        desc = context.user_data.pop("new_prod_desc", "")
        cat_id = context.user_data.pop("new_prod_cat", None)
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT INTO shop_products(bot_token, category_id, name, description, price) "
                "VALUES(?,?,?,?,?)",
                (token, cat_id, name, desc, price)
            )
            await db.commit()
        await update.message.reply_text(
            f"✅ تم إضافة المنتج <b>{name}</b> بسعر {price}",
            reply_markup=back_keyboard(f"shopcat:{short}:{cat_id}")
        )
        return


async def show_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
            "SELECT * FROM orders WHERE bot_token=? ORDER BY created_at DESC LIMIT 20",
            (token,)
        ) as cur:
            orders = [dict(r) for r in await cur.fetchall()]

    if not orders:
        text = "🛒 لا توجد طلبات بعد."
    else:
        lines = [f"🛒 <b>آخر {len(orders)} طلبات:</b>\n"]
        for o in orders:
            lines.append(
                f"• #{o['id']} | المستخدم: {o['user_id']} | الإجمالي: {o['total']:.2f} | {o['status']}"
            )
        text = "\n".join(lines)
    await query.edit_message_text(text, reply_markup=back_keyboard(f"bot:{short}"))
