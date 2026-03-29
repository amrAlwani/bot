#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import logging
import sys
import os
import re
import html
import requests
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, ReplyKeyboardRemove
)
from telegram.ext import (
    Application, ContextTypes, CommandHandler, MessageHandler,
    filters, Defaults
)
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

try:
    from config import r, TOKEN, OWNER_ID, BOT_NAME, Dev_Zaid, botUsername, NAME
    from kvsqlite.sync import Client as DB
    ytdb = DB('ytdb.sqlite')
    sounddb = DB('sounddb.sqlite')
    wsdb = DB('wsdb.sqlite')
    logger.info("✅ تم تحميل الإعدادات")
    # Restore persisted group enable flags from wsdb when Redis fallback is in use
    try:
        restored = 0
        for key in wsdb.keys():
            try:
                if f":enable:{Dev_Zaid}" in key:
                    val = wsdb.get(key)
                    if val:
                        r.set(key, val)
                        # also ensure enablelist contains the chat id
                        try:
                            chat_id = int(key.split(":enable:")[0])
                            r.sadd(f'enablelist:{Dev_Zaid}', chat_id)
                        except Exception:
                            pass
                        restored += 1
            except Exception:
                continue
        if restored:
            logger.info(f"✅ استعادة {restored} إعداد(ات) مجموعة من wsdb")
    except Exception:
        pass
except Exception as e:
    logger.critical(f"❌ خطأ في تحميل الإعدادات: {e}")
    sys.exit(1)

from helpers.Ranks import dev_pls, dev2_pls, devp_pls, get_rank, get_devs_br

print('''
Loading…
█████████████ 50%
''')


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


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        chat = update.effective_chat
        message = update.message
        if not user or not message:
            return

        logger.info(f"start_handler triggered: chat={getattr(chat, 'type', None)} user={getattr(user, 'id', None)} text={getattr(message, 'text', None)!r}")

        name = r.get(f'{Dev_Zaid}:BotName') or NAME
        channel = r.get(f'{Dev_Zaid}:BotChannel') or 'scatteredda'
        k = r.get(f'{Dev_Zaid}:botkey') or '☆'
        safe_user_first_name = html.escape(user.first_name or "")

        # خاص
        if chat and chat.type == "private":
            full_text = message.text or ""

            # مطور - لوحة التحكم
            if dev_pls(user.id, user.id):
                if user.id == 6168217372 or user.id == 5117901887:
                    rank = 'تاج راسي ☆'
                else:
                    rank = get_rank(user.id, user.id)

                if not r.sismember(f'{Dev_Zaid}:UsersList', user.id):
                    r.sadd(f'{Dev_Zaid}:UsersList', user.id)

                reply_markup = ReplyKeyboardMarkup(
                    [
                        [('الاحصائيات')],
                        [('تغيير المطور الاساسي')],
                        [("جلب نسخة القروبات"), ("جلب نسخة المستخدمين")],
                        [('تفعيل البوت الخدمي'), ('تعطيل البوت الخدمي')],
                        [('تفعيل التحميل واليوتيوب'), ('تعطيل التحميل واليوتيوب')],
                        [('الردود العامه'), ('الاوامر العامه')],
                        [('المحظورين عام'), ('المجموعات المحظورة')],
                        [('اذاعة بالخاص'), ('بالمجموعات اذاعة')],
                        [("المكتومين عام"), ("المحظورين من الالعاب")],
                        [('اذاعة بالخاص'), ('اذاعة بالخاص تثبيت')],
                        [('اذاعة بالمجموعات'), ('اذاعه بالمجموعات بالتثبيت')],
                        [('رمز السورس'), ('قناة السورس'), ('اسم البوت')],
                        [('مسح اسم البوت'), ('تعيين اسم البوت')],
                        [('مسح رمز السورس'), ('وضع رمز السورس')],
                        [('مسح قناة السورس'), ('وضع قناة السورس')],
                        [("السيرفر"), ("الملفات"), ("/eval")],
                        [('مجموعة المطور')],
                        [('وضع مجموعة المطور'), ('مسح مجموعة المطور')],
                        [('الغاء')]
                    ],
                    resize_keyboard=True,
                    input_field_placeholder=f'@{context.bot.username} 🧚‍♀️'
                )
                return await message.reply_text(
                    quote=True,
                    text=f'{k} هلا بك {rank}\n{k} قدامك لوحة التحكم',
                    reply_markup=reply_markup
                )

            # مستخدم عادي
            if not r.sismember(f'{Dev_Zaid}:UsersList', user.id):
                r.sadd(f'{Dev_Zaid}:UsersList', user.id)
                # إشعار المطور بمستخدم جديد
                username_str = f'@{user.username}' if user.username else 'ماعنده يوزر'
                count = len(r.smembers(f'{Dev_Zaid}:UsersList'))
                notify_text = (
                    f'☆ شخص جديد دخل للبوت\n'
                    f'☆ اسمه : {safe_user_first_name}\n'
                    f'☆ ايديه : `{user.id}`\n'
                    f'☆ معرفه : {username_str}\n\n'
                    f'☆ عدد المستخدمين صار {count}'
                )
                dev_group = r.get(f'DevGroup:{Dev_Zaid}')
                if dev_group:
                    try:
                        await context.bot.send_message(int(dev_group), notify_text, parse_mode=ParseMode.MARKDOWN)
                    except Exception:
                        pass
                else:
                    for dev in get_devs_br():
                        try:
                            await context.bot.send_message(int(dev), notify_text, parse_mode=ParseMode.MARKDOWN)
                        except Exception:
                            pass

            if "/start Commands" in full_text:
                return await message.reply_text(
                    text=f'{k} اهلين فيك باوامر البوت\n\nللاستفسار - @{channel}',
                    reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton('م1', callback_data=f'commands1:{user.id}'),
                            InlineKeyboardButton('م2', callback_data=f'commands2:{user.id}')
                        ],
                        [InlineKeyboardButton('م3', callback_data=f'commands3:{user.id}')],
                        [
                            InlineKeyboardButton('الالعاب', callback_data=f'commands4:{user.id}'),
                            InlineKeyboardButton('التسليه', callback_data=f'commands5:{user.id}'),
                        ],
                        [InlineKeyboardButton('اليوتيوب', callback_data=f'commands6:{user.id}')],
                    ])
                )

            await message.reply_text(
                text=f'''اهلين انا ،{name} 🧚

↞ اختصاصي ادارة المجموعات من السبام والخ..
↞ كت تويت, يوتيوب, ساوند , واشياء كثير ..
↞ عشان تفعلني ارفعني اشراف وارسل تفعيل.
''',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        'ضيفني لـ مجموعتك 🧚‍♀️',
                        url=f'https://t.me/{context.bot.username}?startgroup=Commands&admin=ban_users+restrict_members+delete_messages+add_admins+change_info+invite_users+pin_messages+manage_call+manage_chat+manage_video_chats+promote_members'
                    )],
                    [InlineKeyboardButton(f'تحديثات {name} 🍻', url=f'https://t.me/{channel}')]
                ])
            )

        # جروب
        else:
            name = r.get(f'{Dev_Zaid}:BotName') or NAME
            is_enabled = r.get(f'{chat.id}:enable:{Dev_Zaid}')
            if is_enabled:
                await message.reply_text(
                    f"مرحباً {safe_user_first_name}! 👋\n"
                    f"البوت مفعّل في هذه المجموعة ✅\n"
                    f"اكتب ( الاوامر ) لعرض كل الأوامر."
                )
            else:
                await message.reply_text(
                    f"مرحباً {safe_user_first_name}! 👋\n\n"
                    f"لتفعيل البوت في هذه المجموعة، يجب على مالك المجموعة إرسال:\n"
                    f"( تفعيل البوت )\n\n"
                    f"ثم يمكن استخدام جميع الأوامر."
                )

        logger.info(f"✅ المستخدم {user.id} بدأ البوت")
    except Exception as e:
        logger.error(f"❌ خطأ في start_handler: {e}", exc_info=True)


async def private_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج رسائل الخاص للمطور - لوحة التحكم"""
    try:
        user = update.effective_user
        chat = update.effective_chat
        message = update.message
        if not user or not message or not message.text:
            return
        if not chat or chat.type != "private":
            return

        logger.info(f"private_text_handler triggered: user={getattr(user, 'id', None)} text={getattr(message, 'text', None)!r}")

        if r.get(f'{user.id}:sarhni'):
            return

        text = message.text.strip()
        k = r.get(f'{Dev_Zaid}:botkey') or '☆'
        name = r.get(f'{Dev_Zaid}:BotName') or NAME
        channel = r.get(f'{Dev_Zaid}:BotChannel') or 'scatteredda'

        if r.get(f'{user.id}:mute:{Dev_Zaid}'):
            return

        # أوامر المطور
        if not dev2_pls(user.id, user.id):
            return

        if text == 'الاحصائيات':
            users_count = len(r.smembers(f'{Dev_Zaid}:UsersList')) if r.smembers(f'{Dev_Zaid}:UsersList') else 0
            chats_count = len(r.smembers(f'enablelist:{Dev_Zaid}')) if r.smembers(f'enablelist:{Dev_Zaid}') else 0
            return await message.reply_text(
                quote=True,
                text=f'{k} هلا بك مطوري\n{k} المستخدمين ~ {users_count}\n{k} المجموعات ~ {chats_count}'
            )

        if text == 'تفعيل البوت الخدمي':
            if r.get(f'DisableBot:{Dev_Zaid}'):
                r.delete(f'DisableBot:{Dev_Zaid}')
                return await message.reply_text(quote=True, text=f'{k} ابشر فعلت البوت الخدمي')
            return await message.reply_text(quote=True, text=f'{k} البوت الخدمي مفعل من قبل')

        if text == 'تعطيل البوت الخدمي':
            if not r.get(f'DisableBot:{Dev_Zaid}'):
                r.set(f'DisableBot:{Dev_Zaid}', 1)
                return await message.reply_text(quote=True, text=f'{k} ابشر عطلت البوت الخدمي')
            return await message.reply_text(quote=True, text=f'{k} البوت الخدمي معطل من قبل')

        if text == 'تفعيل التحميل واليوتيوب':
            if r.get(f':disableYT:{Dev_Zaid}'):
                r.delete(f':disableYT:{Dev_Zaid}')
                return await message.reply_text(quote=True, text=f'{k} ابشر فعلت التحميل')
            return await message.reply_text(quote=True, text=f'{k} التحميل مفعل من قبل')

        if text == 'تعطيل التحميل واليوتيوب':
            if not r.get(f':disableYT:{Dev_Zaid}'):
                r.set(f':disableYT:{Dev_Zaid}', 1)
                return await message.reply_text(quote=True, text=f'{k} ابشر عطلت التحميل')
            return await message.reply_text(quote=True, text=f'{k} التحميل معطل من قبل')

        if text == 'الردود العامه':
            filters_list = r.smembers(f'FiltersList:{Dev_Zaid}')
            if not filters_list:
                return await message.reply_text(quote=True, text=f'{k} مافيه ردود عامه مضافه')
            reply_text = 'ردود البوت:\n'
            for i, rep in enumerate(filters_list, 1):
                ftype = r.get(f'{rep}:filtertype:{Dev_Zaid}')
                reply_text += f'\n{i} - ( {rep} ) ࿓ ( {ftype} )'
            reply_text += '\n☆'
            return await message.reply_text(quote=True, text=reply_text)

        if text == 'المحظورين عام':
            banned = r.smembers(f'listGBAN:{Dev_Zaid}')
            if not banned:
                return await message.reply_text(quote=True, text=f'{k} مافيه حمير محظورين')
            reply_text = 'الحمير المحظورين عام:\n'
            for i, uid in enumerate(banned, 1):
                reply_text += f'{i}) [{uid}](tg://user?id={uid}) ~ ( `{uid}` )\n'
            return await message.reply_text(quote=True, text=reply_text, parse_mode=ParseMode.MARKDOWN)

        if text == 'المحظورين من الالعاب':
            banned = r.smembers(f'listGBANGAMES:{Dev_Zaid}')
            if not banned:
                return await message.reply_text(quote=True, text=f'{k} مافيه حمير محظورين من الالعاب')
            reply_text = 'الحمير المحظورين من الالعاب:\n'
            for i, uid in enumerate(banned, 1):
                reply_text += f'{i}) [{uid}](tg://user?id={uid}) ~ ( `{uid}` )\n'
            return await message.reply_text(quote=True, text=reply_text, parse_mode=ParseMode.MARKDOWN)

        if text == 'المجموعات المحظورة':
            banned_chats = r.smembers(f':BannedChats:{Dev_Zaid}')
            if not banned_chats:
                return await message.reply_text(quote=True, text=f'{k} مافي قروب محظور عام')
            reply_text = 'المجموعات المحظورة عام:\n'
            for i, cid in enumerate(banned_chats, 1):
                reply_text += f'{i}) {cid}\n'
            return await message.reply_text(quote=True, text=reply_text)

        if text == 'رمز السورس':
            return await message.reply_text(quote=True, text=f'`{k}`', parse_mode=ParseMode.MARKDOWN)

        if text == 'قناة السورس':
            ch = r.get(f'{Dev_Zaid}:BotChannel')
            if not ch:
                return await message.reply_text(quote=True, text=f'{k} قناة السورس مو معينة')
            return await message.reply_text(quote=True, text=f'@{ch}')

        if text == 'اسم البوت':
            bot_name = r.get(f'{Dev_Zaid}:BotName')
            if not bot_name:
                return await message.reply_text(quote=True, text=f'{k} مافي اسم للبوت')
            return await message.reply_text(quote=True, text=bot_name)

        if text == 'مجموعة المطور':
            if not devp_pls(user.id, user.id):
                return
            dev_group = r.get(f'DevGroup:{Dev_Zaid}')
            if not dev_group:
                return await message.reply_text(quote=True, text=f'{k} مجموعة المطور مو معينة')
            return await message.reply_text(quote=True, text=f'`{dev_group}`', parse_mode=ParseMode.MARKDOWN)

        if text == 'تعيين اسم البوت':
            r.set(f'{chat.id}:setBotName:{user.id}{Dev_Zaid}', 1)
            return await message.reply_text(quote=True, text=f'{k} ارسل الاسم الجديد للبوت')

        if text == 'مسح اسم البوت':
            r.delete(f'{Dev_Zaid}:BotName')
            return await message.reply_text(quote=True, text=f'{k} ابشر مسحت اسم البوت')

        if text == 'وضع رمز السورس':
            r.set(f'{chat.id}:setBotKey:{user.id}{Dev_Zaid}', 1)
            return await message.reply_text(quote=True, text=f'{k} ارسل الرمز الجديد')

        if text == 'مسح رمز السورس':
            r.delete(f'{Dev_Zaid}:botkey')
            return await message.reply_text(quote=True, text=f'{k} ابشر مسحت الرمز')

        if text == 'وضع قناة السورس':
            r.set(f'{chat.id}:setBotChannel:{user.id}{Dev_Zaid}', 1)
            return await message.reply_text(quote=True, text=f'{k} ارسل يوزر القناة')

        if text == 'مسح قناة السورس':
            r.delete(f'{Dev_Zaid}:BotChannel')
            return await message.reply_text(quote=True, text=f'{k} ابشر مسحت قناة السورس')

        if text == 'وضع مجموعة المطور':
            if not devp_pls(user.id, user.id):
                return
            r.set(f'{chat.id}:setDevGroup:{user.id}{Dev_Zaid}', 1)
            return await message.reply_text(quote=True, text=f'{k} ارسل ايدي مجموعة المطور')

        if text == 'مسح مجموعة المطور':
            if not devp_pls(user.id, user.id):
                return
            r.delete(f'DevGroup:{Dev_Zaid}')
            return await message.reply_text(quote=True, text=f'{k} ابشر مسحت مجموعة المطور')

        if text == 'الغاء':
            r.delete(f'{chat.id}:setBotName:{user.id}{Dev_Zaid}')
            r.delete(f'{chat.id}:setBotChannel:{user.id}{Dev_Zaid}')
            r.delete(f'{chat.id}:setBotKey:{user.id}{Dev_Zaid}')
            r.delete(f'{chat.id}:setDevGroup:{user.id}{Dev_Zaid}')
            return await message.reply_text(
                quote=True,
                text=f'{k} من عيوني لغيت كل شي',
                reply_markup=ReplyKeyboardRemove()
            )

        # استقبال قيم الإعدادات
        if r.get(f'{chat.id}:setBotName:{user.id}{Dev_Zaid}'):
            r.delete(f'{chat.id}:setBotName:{user.id}{Dev_Zaid}')
            r.set(f'{Dev_Zaid}:BotName', text)
            return await message.reply_text(quote=True, text=f'{k} ابشر غيرت اسمي لـ {text}')

        if r.get(f'{chat.id}:setBotChannel:{user.id}{Dev_Zaid}'):
            r.delete(f'{chat.id}:setBotChannel:{user.id}{Dev_Zaid}')
            r.set(f'{Dev_Zaid}:BotChannel', text.replace('@', ''))
            return await message.reply_text(quote=True, text=f'{k} ابشر غيرت قناة السورس لـ {text}')

        if r.get(f'{chat.id}:setBotKey:{user.id}{Dev_Zaid}'):
            r.delete(f'{chat.id}:setBotKey:{user.id}{Dev_Zaid}')
            r.set(f'{Dev_Zaid}:botkey', text)
            return await message.reply_text(quote=True, text=f'{k} ابشر غيرت الرمز لـ {text}')

        if r.get(f'{chat.id}:setDevGroup:{user.id}{Dev_Zaid}') and devp_pls(user.id, user.id):
            r.delete(f'{chat.id}:setDevGroup:{user.id}{Dev_Zaid}')
            try:
                gid = int(text)
            except Exception:
                return await message.reply_text(quote=True, text=f'{k} الايدي غلط!')
            r.set(f'DevGroup:{Dev_Zaid}', gid)
            return await message.reply_text(quote=True, text=f'{k} ابشر قروب المطور لـ {text}')

    except Exception as e:
        logger.error(f"❌ خطأ في private_text_handler: {e}", exc_info=True)


def main():
    print('''
[═══════════════════════════════════════]

  █████╗░██████╗░██████╗░
  ██╔══██╗╚════██╗██╔══██╗
  ██████╔╝░█████╔╝██║░░██║
  ██╔══██╗░╚═══██╗██║░░██║
  ██║░░██║██████╔╝██████╔╝
  ╚═╝░░╚═╝╚═════╝░╚═════╝░

  R3D Bot - python-telegram-bot
  ✅ Async + Safe + Secure

[═══════════════════════════════════════]
    ''')

    logger.info("=" * 70)
    logger.info("🚀 يتم بدء البوت...")
    logger.info("=" * 70)
    logger.info(f"✅ TOKEN: {TOKEN[:20]}...")
    logger.info(f"✅ OWNER_ID: {OWNER_ID}")
    logger.info(f"✅ BOT_NAME: {BOT_NAME}")

    try:
        if sys.platform == 'win32' and hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.set_event_loop(asyncio.new_event_loop())

        defaults = Defaults(parse_mode=ParseMode.HTML)
        async def post_init(application):
            import config, sys
            real_username = application.bot.username
            config.botUsername = real_username
            config.BOT_NAME = real_username
            # Update botUsername in all already-imported plugin modules
            for mod in list(sys.modules.values()):
                if mod and hasattr(mod, 'botUsername'):
                    try:
                        setattr(mod, 'botUsername', real_username)
                    except Exception:
                        pass

        app = Application.builder().token(TOKEN).defaults(defaults).post_init(post_init).build()
        logger.info("✅ التطبيق جاهز")

        # أوامر البدء
        app.add_handler(CommandHandler("start", start_handler))

        # معالج رسائل الخاص للمطور (group=4 مستقل)
        app.add_handler(
            MessageHandler(
                filters.TEXT & filters.ChatType.PRIVATE,
                private_text_handler
            ),
            group=4,
        )

        logger.info("🔄 جاري تحميل الـ Plugins...")

        # قائمة كل الـ plugins مع أسماء دوال التسجيل
        plugins_to_load = [
            ("Plugins.welcome_and_rules", "register_welcome_handlers"),
            ("Plugins.fun",               "register"),
            ("Plugins.all",               "register"),
            ("Plugins.mute_and_gban",     "register"),
            ("Plugins.set_ranks",         "register"),
            ("Plugins.get_ranks",         "register"),
            ("Plugins.del_ranks",         "register"),
            ("Plugins.customCommad",      "register"),
            ("Plugins.customFilter",      "register"),
            ("Plugins.globalFilters",     "register"),
            ("Plugins.customRank",        "register"),
            ("Plugins.replace",           "register"),
            ("Plugins.custom_plugin",     "register"),
            ("Plugins.games",             "register"),
            ("Plugins.group_update",      "register"),
            ("Plugins.id",                "register"),
            ("Plugins.sarhni",            "register"),
            ("Plugins.downloader",        "register"),
            ("Plugins.whisper",           "register"),
            ("Plugins.private&sudos",     "register"),
        ]

        import importlib
        import importlib.util as _iutil
        base_path = os.path.dirname(os.path.abspath(__file__))

        for module_name, func_name in plugins_to_load:
            try:
                # ملفات بأسماء خاصة تحتوي & نحملها مباشرة
                if "&" in module_name:
                    plugin_file = module_name.replace("Plugins.", "Plugins/").replace(".", "/") + ".py"
                    plugin_path = os.path.join(base_path, plugin_file)
                    spec = _iutil.spec_from_file_location(module_name, plugin_path)
                    if spec is None or spec.loader is None:
                        raise ImportError(f"Cannot load spec for {module_name}")
                    mod = _iutil.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                else:
                    mod = importlib.import_module(module_name)

                reg_func = getattr(mod, func_name, None)
                if reg_func:
                    reg_func(app)
                    logger.info(f"✅ تم تحميل {module_name}")
                else:
                    logger.warning(f"⚠️ لم يوجد {func_name} في {module_name}")
            except Exception as e:
                logger.error(f"⚠️ خطأ في تحميل {module_name}: {e}", exc_info=True)

        # تسجيل معالج الأخطاء
        app.add_error_handler(error_handler)
        logger.info("✅ جميع المعالجات مسجلة")

        logger.info("════════════════════════════════════════════════════════════════")
        logger.info("🔮 جاري تشغيل البوت...")
        logger.info("════════════════════════════════════════════════════════════════")
        print("🔮 Your bot started successfully!")
        print("")

        app.run_polling(
            allowed_updates=[
                "message",
                "edited_message",
                "chat_member",
                "callback_query",
                "inline_query",
                "chat_join_request",
            ]
        )

    except TelegramConflict as e:
        logger.critical(f"❌ CONFLICT ERROR: {e}")
        print("=" * 70)
        print("❌ CONFLICT ERROR")
        print("Another bot instance is already running with this token.")
        print("Stop other instances and restart.")
        print("=" * 70)
        sys.exit(1)

    except KeyboardInterrupt:
        logger.info("⏹️ تم إيقاف البوت بواسطة المستخدم")
        print("\n✅ Bot stopped by user")

    except Exception as e:
        logger.critical(f"❌ خطأ حرج: {e}", exc_info=True)
        print(f"❌ Critical Error: {e}")
        sys.exit(1)

    finally:
        logger.info("════════════════════════════════════════════════════════════════")
        logger.info("👋 البوت متوقف")
        logger.info("════════════════════════════════════════════════════════════════")


if __name__ == "__main__":
    main()
