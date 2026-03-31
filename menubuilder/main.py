"""
MenuBuilder Bot — main entry point.
Runs the main management bot and restarts all previously-active child bots.
"""
import asyncio
import logging
import signal
import sys

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config import MAIN_BOT_TOKEN, MAIN_BOT_ADMIN
from models.database import init_db
import utils.bot_runner as runner

from handlers.start import cmd_start, show_home, show_help, show_my_stats
from handlers.bot_manager import (
    show_my_bots,
    start_add_bot,
    receive_bot_token,
    show_bot_panel,
    toggle_bot_start,
    confirm_delete_bot,
    do_delete_bot,
    WAITING_TOKEN,
)
from handlers.menu_builder import (
    show_menu_list,
    start_new_menu,
    show_menu_edit,
    start_new_button,
    start_edit_menu_text,
    confirm_del_menu,
    do_del_menu,
    show_edit_btn,
    handle_btn_type,
    del_button,
    handle_text_input,
    WAIT_MENU_TITLE,
    WAIT_MENU_TEXT,
    WAIT_BTN_LABEL,
    WAIT_BTN_RESPONSE,
    WAIT_BTN_URL,
)
from handlers.broadcast import (
    start_broadcast,
    handle_broadcast_message,
    WAIT_BROADCAST_MSG,
)
from handlers.settings import (
    show_settings,
    toggle_setting,
    start_set_welcome,
    start_set_ref_bonus,
    handle_settings_input,
    show_bot_users,
    show_stats,
    show_admins,
    WAIT_WELCOME,
    WAIT_REF_BONUS,
)
from handlers.shop import (
    show_shop_panel,
    start_new_category,
    show_category_products,
    start_new_product,
    handle_shop_input,
    show_orders,
    WAIT_CAT_NAME,
    WAIT_CAT_EMOJI,
    WAIT_PROD_NAME,
    WAIT_PROD_PRICE,
    WAIT_PROD_DESC,
)
from handlers.child_bot import build_child_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def _is_waiting_input(context):
    """Return True if the user is in any text-input conversation state."""
    ud = context.user_data
    return any(ud.get(k) for k in [
        WAITING_TOKEN, WAIT_MENU_TITLE, WAIT_MENU_TEXT,
        WAIT_BTN_LABEL, WAIT_BTN_RESPONSE, WAIT_BTN_URL,
        WAIT_BROADCAST_MSG, WAIT_WELCOME, WAIT_REF_BONUS,
        WAIT_CAT_NAME, WAIT_CAT_EMOJI,
        WAIT_PROD_NAME, WAIT_PROD_PRICE, WAIT_PROD_DESC,
    ])


async def dispatch_text(update: Update, context):
    """Route incoming text to the correct waiting handler."""
    ud = context.user_data

    if ud.get(WAITING_TOKEN):
        await receive_bot_token(update, context)
    elif ud.get(WAIT_MENU_TITLE) or ud.get(WAIT_MENU_TEXT) or \
            ud.get(WAIT_BTN_LABEL) or ud.get(WAIT_BTN_RESPONSE) or ud.get(WAIT_BTN_URL):
        await handle_text_input(update, context)
    elif ud.get(WAIT_BROADCAST_MSG):
        await handle_broadcast_message(update, context)
    elif ud.get(WAIT_WELCOME) or ud.get(WAIT_REF_BONUS):
        await handle_settings_input(update, context)
    elif ud.get(WAIT_CAT_NAME) or ud.get(WAIT_CAT_EMOJI) or \
            ud.get(WAIT_PROD_NAME) or ud.get(WAIT_PROD_PRICE) or ud.get(WAIT_PROD_DESC):
        await handle_shop_input(update, context)


def build_main_app() -> Application:
    if not MAIN_BOT_TOKEN:
        logger.error("❌ MAIN_BOT_TOKEN is not set in .env!")
        sys.exit(1)

    app = Application.builder().token(MAIN_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("cancel", cmd_start))

    # ── home
    app.add_handler(CallbackQueryHandler(show_home, pattern="^home$"))
    app.add_handler(CallbackQueryHandler(show_help, pattern="^help$"))
    app.add_handler(CallbackQueryHandler(show_my_stats, pattern="^my_stats$"))

    # ── bots list & add
    app.add_handler(CallbackQueryHandler(show_my_bots, pattern="^my_bots$"))
    app.add_handler(CallbackQueryHandler(start_add_bot, pattern="^add_bot$"))

    # ── bot panel
    app.add_handler(CallbackQueryHandler(show_bot_panel, pattern=r"^bot:"))
    app.add_handler(CallbackQueryHandler(toggle_bot_start, pattern=r"^start_bot:"))
    app.add_handler(CallbackQueryHandler(toggle_bot_start, pattern=r"^stop_bot:"))
    app.add_handler(CallbackQueryHandler(confirm_delete_bot, pattern=r"^delete_bot:"))
    app.add_handler(CallbackQueryHandler(do_delete_bot, pattern=r"^do_delete:"))

    # ── menu builder
    app.add_handler(CallbackQueryHandler(show_menu_list, pattern=r"^menu_list:"))
    app.add_handler(CallbackQueryHandler(start_new_menu, pattern=r"^new_menu:"))
    app.add_handler(CallbackQueryHandler(show_menu_edit, pattern=r"^edit_menu:"))
    app.add_handler(CallbackQueryHandler(start_new_button, pattern=r"^new_btn:"))
    app.add_handler(CallbackQueryHandler(start_edit_menu_text, pattern=r"^edit_menu_text:"))
    app.add_handler(CallbackQueryHandler(confirm_del_menu, pattern=r"^del_menu:"))
    app.add_handler(CallbackQueryHandler(do_del_menu, pattern=r"^do_del_menu:"))
    app.add_handler(CallbackQueryHandler(show_edit_btn, pattern=r"^edit_btn:"))
    app.add_handler(CallbackQueryHandler(handle_btn_type, pattern=r"^btntype:"))
    app.add_handler(CallbackQueryHandler(del_button, pattern=r"^del_btn:"))

    # ── broadcast
    app.add_handler(CallbackQueryHandler(start_broadcast, pattern=r"^broadcast:"))

    # ── settings
    app.add_handler(CallbackQueryHandler(show_settings, pattern=r"^bot_settings:"))
    app.add_handler(CallbackQueryHandler(toggle_setting, pattern=r"^toggle:"))
    app.add_handler(CallbackQueryHandler(start_set_welcome, pattern=r"^set_welcome:"))
    app.add_handler(CallbackQueryHandler(start_set_ref_bonus, pattern=r"^set_ref_bonus:"))
    app.add_handler(CallbackQueryHandler(show_bot_users, pattern=r"^bot_users:"))
    app.add_handler(CallbackQueryHandler(show_stats, pattern=r"^stats:"))
    app.add_handler(CallbackQueryHandler(show_admins, pattern=r"^admins:"))

    # ── shop
    app.add_handler(CallbackQueryHandler(show_shop_panel, pattern=r"^shop:"))
    app.add_handler(CallbackQueryHandler(start_new_category, pattern=r"^new_cat:"))
    app.add_handler(CallbackQueryHandler(show_category_products, pattern=r"^shopcat:"))
    app.add_handler(CallbackQueryHandler(start_new_product, pattern=r"^new_product:"))
    app.add_handler(CallbackQueryHandler(show_orders, pattern=r"^orders:"))

    # ── text input dispatcher
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        dispatch_text
    ))
    # ── broadcast media
    app.add_handler(MessageHandler(
        (filters.PHOTO | filters.VIDEO | filters.Document.ALL |
         filters.AUDIO | filters.VOICE | filters.Sticker.ALL) & ~filters.COMMAND,
        handle_broadcast_message
    ))

    return app


async def restore_active_bots():
    """Re-start all bots that were active before shutdown."""
    import aiosqlite
    from config import DB_PATH
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT token FROM managed_bots WHERE is_active=1"
        ) as cur:
            tokens = [r["token"] for r in await cur.fetchall()]

    for token in tokens:
        logger.info(f"Restoring child bot: {token[:20]}...")
        await runner.start_child_bot(token, build_child_app)


async def main():
    logger.info("🚀 MenuBuilder Bot starting...")
    await init_db()

    main_app = build_main_app()

    await main_app.initialize()
    await main_app.start()
    await main_app.updater.start_polling(drop_pending_updates=True)
    logger.info("✅ Main management bot is running")

    await restore_active_bots()

    stop_event = asyncio.Event()

    def _signal_handler(sig, frame):
        logger.info(f"Received signal {sig}, shutting down...")
        stop_event.set()

    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)

    logger.info("🟢 All bots running. Press Ctrl+C to stop.")
    await stop_event.wait()

    logger.info("⏹️ Stopping all child bots...")
    await runner.stop_all()
    await main_app.updater.stop()
    await main_app.stop()
    await main_app.shutdown()
    logger.info("✅ Shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
