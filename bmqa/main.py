#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import sys
import os

from telegram.ext import Application, Defaults
from telegram.constants import ParseMode
from telegram.error import Conflict as TelegramConflict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ================= CONFIG =================
try:
    from config import TOKEN
    from kvsqlite.sync import Client as DB
    ytdb = DB('ytdb.sqlite')
    sounddb = DB('sounddb.sqlite')
    wsdb = DB('wsdb.sqlite')
    logger.info("✅ تم تحميل الإعدادات وقواعد البيانات")
except Exception as e:
    logger.critical(f"❌ خطأ في تحميل الإعدادات: {e}")
    sys.exit(1)

# ================= PLUGINS LOADER =================
def load_plugins(app: Application):
    plugins_list = [
        "Plugins.welcome_and_rules",
        "Plugins.fun",
        "Plugins.all",
        "Plugins.mute_and_gban",
        "Plugins.set_ranks",
        "Plugins.get_ranks",
        "Plugins.del_ranks",
        "Plugins.customCommad",
        "Plugins.customFilter",
        "Plugins.globalFilters",
        "Plugins.customRank",
        "Plugins.replace",
        "Plugins.custom_plugin",
        "Plugins.games",
        "Plugins.group_update",
        "Plugins.id",
        "Plugins.sarhni",
        "Plugins.downloader",
        "Plugins.whisper",
        "Plugins.private&sudos",   # تم تفعيله
    ]

    import importlib
    import importlib.util as iutil
    base_path = os.path.dirname(os.path.abspath(__file__))

    for module_name in plugins_list:
        try:
            if "&" in module_name:
                plugin_file = module_name.replace("Plugins.", "Plugins/").replace(".", "/") + ".py"
                plugin_path = os.path.join(base_path, plugin_file)
                spec = iutil.spec_from_file_location(module_name, plugin_path)
                if spec is None or spec.loader is None:
                    raise ImportError(f"Cannot load spec for {module_name}")
                mod = iutil.module_from_spec(spec)
                spec.loader.exec_module(mod)
            else:
                mod = importlib.import_module(module_name)

            reg_func = getattr(mod, "register", None)
            if reg_func is None:
                reg_func = getattr(mod, "register_welcome_handlers", None)
            if reg_func:
                reg_func(app)
                logger.info(f"✅ تم تحميل {module_name}")
            else:
                logger.warning(f"⚠️ لم توجد دالة تسجيل في {module_name}")
        except Exception as e:
            logger.error(f"⚠️ خطأ في تحميل {module_name}: {e}", exc_info=True)

# ================= ERROR HANDLER =================
async def error_handler(update, context):
    error = context.error
    logger.error(f"❌ حدث خطأ: {error}", exc_info=True)
    if isinstance(error, TelegramConflict):
        logger.critical("⚠️ CONFLICT: نسخة أخرى من البوت تعمل!")
        print("=" * 70)
        print("⚠️  CONFLICT ERROR")
        print("Another bot instance is already running with this token.")
        print("Stop other instances and restart.")
        print("=" * 70)

# ================= MAIN =================
def main():
    print('''
[═══════════════════════════════════════]

  █████╗░██████╗░██████╗░
  ██╔══██╗╚════██╗██╔══██╗
  ██████╔╝░█████╔╝██║░░██║
  ██╔══██╗░╚═══██╗██║░░██║
  ██║░░██║██████╔╝██████╔╝
  ╚═╝░░╚═╝╚═════╝░╚═════╝░

  R3D Bot - Full Features
  ✅ All plugins enabled

[═══════════════════════════════════════]
    ''')

    if not TOKEN:
        logger.critical("❌ TOKEN غير موجود في config")
        return

    if sys.platform == 'win32' and hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    defaults = Defaults(parse_mode=ParseMode.HTML)

    async def post_init(application: Application):
        real_username = application.bot.username
        try:
            import config
            config.botUsername = real_username
            config.BOT_NAME = real_username
        except Exception:
            pass
        for mod in list(sys.modules.values()):
            if mod and hasattr(mod, 'botUsername'):
                try:
                    setattr(mod, 'botUsername', real_username)
                except Exception:
                    pass

    app = Application.builder()\
        .token(TOKEN)\
        .defaults(defaults)\
        .post_init(post_init)\
        .build()

    load_plugins(app)
    app.add_error_handler(error_handler)

    logger.info("🚀 بدء تشغيل البوت...")
    print("🔮 Bot starting... (All plugins active)")

    try:
        app.run_polling(
            allowed_updates=[
                "message", "edited_message", "chat_member",
                "callback_query", "inline_query", "chat_join_request"
            ]
        )
    except TelegramConflict:
        logger.critical("❌ تعارض: يوجد نسخة أخرى من البوت تعمل")
    except KeyboardInterrupt:
        logger.info("⏹ تم إيقاف البوت يدوياً")
    except Exception as e:
        logger.critical(f"❌ خطأ حرج: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
