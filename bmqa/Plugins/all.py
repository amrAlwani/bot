
import random
import re
import time
import pytz
import os
try:
    import gtts
except ModuleNotFoundError:
    gtts = None

try:
    import requests
except ModuleNotFoundError:
    requests = None

try:
    import speech_recognition as sr
except ModuleNotFoundError:
    sr = None
try:
    from pydub import AudioSegment
except ModuleNotFoundError:
    AudioSegment = None
try:
    from hijri_converter import Hijri, Gregorian
except ModuleNotFoundError:
    Hijri = None
    Gregorian = None
from datetime import datetime
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions, MessageEntity, ForceReply, ForceReply
from telegram.ext import ContextTypes, filters, MessageHandler, CallbackQueryHandler, ChatJoinRequestHandler
from telegram.error import BadRequest, RetryAfter
from telegram.constants import ChatMemberStatus
from config import *
from helpers.Ranks import *
from helpers.persianData import persianInformation
from .welcome_and_rules import *
from .games import *
from PIL import Image

# Defensive fallback if config module does not provide r or Dev_Zaid in runtime context.
try:
    Dev_Zaid
except NameError:
    Dev_Zaid = ""

try:
    if r is None:
        raise NameError
except NameError:
    try:
        from config import DummyRedis
        r = DummyRedis()
    except Exception:
        class DummyRedis:
            def get(self, key, default=None):
                return default
            def set(self, key, value, ex=None):
                return True
            def delete(self, *keys):
                return 0
            def hgetall(self, name):
                return {}
            def hget(self, name, key):
                return None
            def hset(self, name, key, value):
                return 1
            def smembers(self, name):
                return set()
            def sadd(self, name, *values):
                return 0
            def sismember(self, name, value):
                return False
            def exists(self, key):
                return False
            def incr(self, key, amount=1):
                return 0
            def setex(self, key, ex, value):
                return True
        r = DummyRedis()

from aiohttp import ClientSession
try:
    from Python_ARQ import ARQ
except Exception:
    ARQ = None
from aiohttp import ClientSession

# from googletrans import Translator as googletranstr
from mutagen.mp3 import MP3 as mutagenMP3
# from main import TelegramBot

ARQ_API_KEY = "OZJRWV-SAURXD-PMBUKF-GMVSNS-ARQ"
ARQ_API_URL = "https://arq.hamker.dev"

# translator = googletranstr()

list_UwU = [
    "كس",
    "كسمك",
    "كسختك",
    "عير",
    "كسخالتك",
    "خرا بالله",
    "عير بالله",
    "كسخواتكم",
    "كحاب",
    "مناويج",
    "مناويج",
    "كحبه",
    "ابن الكحبه",
    "فرخ",
    "فروخ",
    "طيزك",
    "طيزختك",
    "كسمك",
    "يا ابن الخول",
    "المتناك",
    "شرموط",
    "شرموطه",
    "ابن الشرموطه",
    "ابن الخول",
    "ابن العرص",
    "منايك",
    "متناك",
    "ابن المتناكه",
    "زبك",
    "عرص",
    "زبي",
    "خول",
    "لبوه",
    "لباوي",
    "ابن اللبوه",
    "منيوك",
    "كسمكك",
    "متناكه",
    "يا عرص",
    "يا خول",
    "قحبه",
    "القحبه",
    "شراميط",
    "العلق",
    "العلوق",
    "العلقه",
    "كسمك",
    "يا ابن الخول",
    "المتناك",
    "شرموط",
    "شرموطه",
    "ابن الشرموطه",
    "ابن الخول",
    "االمنيوك",
    "كسمككك",
    "الشرموطه",
    "ابن العرث",
    "ابن الحيضانه",
    "زبك",
    "خول",
    "زبي",
    "قاحب",
]

list_Shiaa = [
    "يا علي",
    "يا حسين",
    "ياعلي",
    "ياحسين",
    "علي ولي الله",
    "عليا ولي الله",
    "عائشه زانيه",
    "عائشة زانية",
    "عائشة عاهرة",
    "عائشه عاهره",
    "خرب ربك",
    "خرب الله",
    "يلعن ربك",
    "يلعن الله",
    "يا عمر",
    "ياعمر",
    "يا محمد",
    "يامحمد",
    "زوجات الرسول",
    "عير بالسنة",
    "عير بالسنه",
    "خرب السنه",
    "خرا بالسنه",
    "خرب السنة",
    "خرا بالسنة",
    "والحسين",
    "والعباس",
    "وعلي",
    "والامام علي",
    "ربنا علي",
    "علي الله",
    "الله علي",
    "رب علي",
    "علي رب",
]

def Find(text):
    m = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(m, text)
    return [x[0] for x in url]


def get_event_text(event):
    if event is None:
        return ""
    if hasattr(event, "text") and event.text:
        return str(event.text)
    if hasattr(event, "data") and event.data:
        return str(event.data)
    if hasattr(event, "message") and event.message:
        return get_event_text(event.message)
    return ""


def get_event_from_user(event):
    if event is None:
        return None
    if hasattr(event, "from_user") and event.from_user:
        return event.from_user
    if hasattr(event, "sender_chat") and event.sender_chat:
        return event.sender_chat
    if hasattr(event, "message") and event.message:
        return get_event_from_user(event.message)
    return None


def get_event_chat(event):
    if event is None:
        return None
    if hasattr(event, "chat") and event.chat:
        return event.chat
    if hasattr(event, "message") and event.message:
        return get_event_chat(event.message)
    return None


def get_message_actor(message, channel=""):
    if message is None:
        return None, None
    if hasattr(message, "sender_chat") and message.sender_chat:
        return message.sender_chat.id, f"[{message.sender_chat.title}](t.me/{channel})"
    if hasattr(message, "from_user") and message.from_user:
        return message.from_user.id, message.from_user.mention_html()
    return None, None
    return None

"""
         r.get(f'{message.chat.id}:mute:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockJoin:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockChannels:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockEdit:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockEditM:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockVoice:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockVideo:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockNot:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockPhoto:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockStickers:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockAnimations:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockFiles:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockPersian:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockUrls:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockHashtags:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockMessages:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockTags:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockBots:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockSpam:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockInline:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockForward:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockAudios:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockaddContacts:{Dev_Zaid}')
         r.get(f'{message.chat.id}:lockSHTM:{Dev_Zaid}')
"""

# Converted Pyrogram on_message handler
async def on_zbi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update:
        return

    # Ensure redis client is available
    global r
    if r is None:
        try:
            from config import DummyRedis
            r = DummyRedis()
        except Exception:
            return

    event = update.message or update.callback_query or update.chat_join_request
    if not event:
        return

    message = event
    user = get_event_from_user(update)
    chat = get_event_chat(update)
    name = r.get(f"{Dev_Zaid}:BotName") or NAME
    text = (get_event_text(event) or "").strip()

    if not text:
        return

    # Allow direct name prefix commands, e.g. 'غدغد الاوامر'
    if text.startswith(f"{name} "):
        text = text[len(name) + 1 :].strip()

    # Also support mention by bot username
    if botUsername:
        bot_mention = f"@{botUsername}"
        if text.startswith(f"{bot_mention} "):
            text = text[len(bot_mention) + 1 :]

    if chat and r.get(f"{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}"):
        text = r.get(f"{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}")
    if r.get(f"Custom:{Dev_Zaid}&text={text}"):
        text = r.get(f"Custom:{Dev_Zaid}&text={text}")

    if r.get(f"inDontCheck:{Dev_Zaid}"):
        return

    if user and dev_pls(user.id, chat.id if chat else None):
        return

    if (
        text.startswith("تفعيل ")
        or text.startswith("تعطيل ")
        or text.startswith("قفل ")
        or text.startswith("فتح ")
        or text == "ايدي"
        or text == "الاوامر"
    ):
        if r.get(f"forceChannel:{Dev_Zaid}") and (
            not r.get(f"disableSubscribe:{Dev_Zaid}")
        ):
            username = r.get(f"forceChannel:{Dev_Zaid}").replace("@", "")
            not_member = False
            try:
                if user:
                    member = await context.bot.get_chat_member(username, user.id)
                else:
                    return
            except RetryAfter:
                return
            except BadRequest:
                await message.reply_text(
                    f"- انضم للقناة ( @{username} ) لتستطيع استخدام اوامر البوت",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "اضغط هنا", url="https://t.me/" + username
                                )
                            ]
                        ]
                    ),
                )
                r.set(f"inDontCheck:{Dev_Zaid}", 1, ex=10)
                return
            except Exception as e:
                print(e)
                return

            if member.status in {
                ChatMemberStatus.LEFT,
                ChatMemberStatus.BANNED,
            } or member.status is None:
                not_member = True
            else:
                not_member = False

            if not_member:
                await message.reply_text(
                    f"- انضم للقناة ( @{username} ) لتستطيع استخدام اوامر البوت",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "اضغط هنا", url="https://t.me/" + username
                                )
                            ]
                        ]
                    ),
                )
                r.set(f"inDontCheck:{Dev_Zaid}", ex=10)
                return
            else:
                return

# Converted Pyrogram on_message handler
async def guardLocksResponse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update:
        return

    global r
    if r is None:
        try:
            from config import DummyRedis
            r = DummyRedis()
        except Exception:
            return

    event = update.message or update.callback_query or update.chat_join_request
    if not event:
        return

    message = event
    user = get_event_from_user(update)
    chat = get_event_chat(update)
    k = r.get(f"{Dev_Zaid}:botkey") or "☆"
    channel = r.get(f"{Dev_Zaid}:BotChannel") if r.get(f"{Dev_Zaid}:BotChannel") else "scatteredda"
    try:
        await guardResponseFunction(update, context, k, channel)
    except Exception as _e:
        import logging; logging.getLogger(__name__).error(f"guardResponseFunction error: {_e}", exc_info=True)


# Converted Pyrogram on_edited_message handler
async def guardLocksResponse2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update:
        return

    global r
    if r is None:
        try:
            from config import DummyRedis
            r = DummyRedis()
        except Exception:
            return

    event = update.message or update.callback_query or update.chat_join_request
    if not event:
        return

    message = event
    user = get_event_from_user(update)
    chat = get_event_chat(update)
    k = r.get(f"{Dev_Zaid}:botkey") or "☆"
    channel = r.get(f"{Dev_Zaid}:BotChannel") if r.get(f"{Dev_Zaid}:BotChannel") else "scatteredda"
    try:
        await guardResponseFunction2(update, context, k, channel)
    except Exception as _e:
        import logging; logging.getLogger(__name__).error(f"guardResponseFunction2 error: {_e}", exc_info=True)

async def guardResponseFunction2(update: Update, context: ContextTypes.DEFAULT_TYPE, k, channel):
    if not update:
        return
    event = update.message or update.callback_query or update.chat_join_request
    if not event:
        return
    message = event
    if not r.get(f"{message.chat.id}:enable:{Dev_Zaid}"):
        return
    actor_id, mention = get_message_actor(message, channel)
    if not actor_id:
        return

    warner = """
「 {} 」
{} ممنوع {}
☆
"""
    warn = False
    reason = False

    if (
        r.get(f"{message.chat.id}:lockEdit:{Dev_Zaid}")
        and message.text
        and not pre_pls(actor_id, message.chat.id)
    ):
        await message.delete()
        warn = True
        reason = "التعديل"
        if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}", 1, ex=60)
            return await message.reply_text(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    has_media = bool(
        message.photo or message.video or message.audio or message.document
        or message.sticker or message.animation or message.voice or message.video_note
    )
    if (
        r.get(f"{message.chat.id}:lockEditM:{Dev_Zaid}")
        and has_media
        and not pre_pls(actor_id, message.chat.id)
    ):
        await message.delete()
        warn = True
        reason = "تعديل الميديا"
        if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}", 1, ex=60)
            return await message.reply_text(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

async def guardResponseFunction(update: Update, context: ContextTypes.DEFAULT_TYPE, k, channel):
    if not update:
        return
    message = update.message
    if not message:
        return
    user = update.effective_user
    chat = update.effective_chat
    if not chat or not hasattr(message, "chat") or not message.chat:
        return
    if chat and chat.type not in ("private",) and not r.get(f"{message.chat.id}:enable:{Dev_Zaid}"):
        return
    warner = """
「 {} 」
{} ممنوع {}
☆
"""
    warn = False
    reason = False

    actor_id, mention = get_message_actor(message, channel)
    if not actor_id:
        return

    if r.get(f"{message.chat.id}:lockNot:{Dev_Zaid}") and getattr(message, "service", None):
        await message.delete()

    if (
        r.get(f"{message.chat.id}:lockaddContacts:{Dev_Zaid}")
        and message.from_user
        and getattr(message, "new_chat_members", None)
    ):
        if pre_pls(actor_id, message.chat.id):
            return
        for me in message.new_chat_members:
            if not me.id == actor_id:
                warn = True
                mention = message.from_user.mention_html()
                await context.bot.ban_chat_member(chat.id, me.id)
                reason = "تضيف حد هنا"
                await message.delete()
                if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}"):
                    return await message.reply_text(
                        warner.format(mention, k, reason), disable_web_page_preview=True
                    )

    # print(actor_id)

    file_id = None
    if message.sticker:
        file_id = message.sticker.file_id
    elif message.animation:
        file_id = message.animation.file_id
    elif message.photo:
        file_id = message.photo[-1].file_id
    elif message.video:
        file_id = message.video.file_id
    elif message.voice:
        file_id = message.voice.file_id
    elif message.audio:
        file_id = message.audio.file_id
    elif message.document:
        file_id = message.document.file_id
    if file_id:
        idd = file_id[-6:]
        if r.get(f"{idd}:NotAllow:{message.chat.id}{Dev_Zaid}"):
            if not admin_pls(actor_id, message.chat.id):
                return await message.delete()

    if message.text and r.smembers(f"{message.chat.id}:NotAllowedListText:{Dev_Zaid}"):
        if not admin_pls(actor_id, message.chat.id):
            for word in r.smembers(f"{message.chat.id}:NotAllowedListText:{Dev_Zaid}"):
                if word in message.text:
                    return await message.delete()

    if r.get(f"{actor_id}:mute:{message.chat.id}{Dev_Zaid}") or r.get(f"{actor_id}:mute:{Dev_Zaid}"):
        return False

    if r.get(f"{message.chat.id}:mute:{Dev_Zaid}") and not admin_pls(actor_id, message.chat.id):
        await message.delete()
        return False

    if pre_pls(actor_id, message.chat.id):
        return False

    if r.get(f"{message.chat.id}:lockBots:{Dev_Zaid}") and message.new_chat_members:
        for mem in message.new_chat_members:
            if mem.is_bot:
                return await context.bot.ban_chat_member(chat.id, mem.id)

    if r.get(f"{message.chat.id}:lockJoin:{Dev_Zaid}") and message.new_chat_members:
        for mem in message.new_chat_members:
            if not admin_pls(mem.id, message.chat.id):
                await context.bot.ban_chat_member(chat.id, mem.id)
                await context.bot.unban_chat_member(chat.id, mem.id)
                return False

    if r.get(f"{message.chat.id}:lockChannels:{Dev_Zaid}") and message.sender_chat:
        if not message.sender_chat.id == message.chat.id:
            await context.bot.ban_chat_member(chat.id, message.sender_chat.id)
            return False

    if r.get(f"{message.chat.id}:lockSpam:{Dev_Zaid}"):
        if not r.get(f"{actor_id}in_spam:{message.chat.id}{Dev_Zaid}"):
            r.set(f"{actor_id}in_spam:{message.chat.id}{Dev_Zaid}", 1, ex=10)
        else:
            if int(r.get(f"{actor_id}in_spam:{message.chat.id}{Dev_Zaid}") or 0) == 10:
                if message.from_user:
                    r.set(f"{actor_id}:mute:{message.chat.id}{Dev_Zaid}", 1)
                    r.sadd(f"{message.chat.id}:listMUTE:{Dev_Zaid}", actor_id)
                    r.delete(f"{actor_id}in_spam:{message.chat.id}{Dev_Zaid}")
                    return await message.reply_text(
                        f"「 {mention} 」 \n{k} كتمتك يالبثر عشان تتعلم تكرر\n☆"
                    )

                if message.sender_chat:
                    await context.bot.ban_chat_member(chat.id, message.sender_chat.id)
                    return await message.reply_text(
                        f"「 {mention} 」 {k} حظرتك يالبثر عشان تتعلم تكرر\n☆"
                    )
            else:
                get = int(r.get(f"{id}in_spam:{message.chat.id}{Dev_Zaid}") or 0)
                r.set(f"{id}in_spam:{message.chat.id}{Dev_Zaid}", get + 1, ex=10)

    if r.get(f"{message.chat.id}:lockInline:{Dev_Zaid}") and message.via_bot:
        await message.delete()
        warn = True
        reason = "ترسل انلاين"
        if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}", 1, ex=60)
            return await message.reply_text(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{message.chat.id}:lockForward:{Dev_Zaid}") and message.forward_date:
        await message.delete()
        warn = True
        reason = "ترسل توجيه"
        if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}", 1, ex=60)
            return await message.reply_text(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    """
  if r.get(f'{message.chat.id}:lockForward:{Dev_Zaid}') and message.forward_from_chat:
     await message.delete()
     warn = True
     reason = 'ترسل توجيه'
     if not r.get(f'{message.chat.id}:disableWarn:{Dev_Zaid}') and not r.get(f'{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}'):
        r.set(f'{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}',1,ex=60)
        return await message.reply_text(warner.format(mention,k,reason),disable_web_page_preview=True)
  """

    if r.get(f"{message.chat.id}:lockAudios:{Dev_Zaid}") and message.audio:
        await message.delete()
        warn = True
        reason = "ترسل صوت"
        if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}", 1, ex=60)
            return await message.reply_text(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{message.chat.id}:lockVideo:{Dev_Zaid}") and message.video:
        await message.delete()
        warn = True
        reason = "ترسل فيديوهات"
        if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}", 1, ex=60)
            return await message.reply_text(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{message.chat.id}:lockPhoto:{Dev_Zaid}") and message.photo:
        await message.delete()
        warn = True
        reason = "ترسل صور"
        if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}", 1, ex=60)
            return await message.reply_text(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{message.chat.id}:lockStickers:{Dev_Zaid}") and message.sticker:
        await message.delete()
        warn = True
        reason = "ترسل ملصقات"
        if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}", 1, ex=60)
            return await message.reply_text(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{message.chat.id}:lockAnimations:{Dev_Zaid}") and message.animation:
        await message.delete()
        warn = True
        reason = "ترسل متحركات"
        if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}", 1, ex=60)
            return await message.reply_text(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{message.chat.id}:lockFiles:{Dev_Zaid}") and message.document:
        await message.delete()
        warn = True
        reason = "ترسل ملفات"
        if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}", 1, ex=60)
            return await message.reply_text(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{message.chat.id}:lockPersian:{Dev_Zaid}") and message.text:
        if "ه‍" in message.text or "ی" in message.text or "ک" in message.text or "چ" in message.text:
            await message.delete()
            warn = True
            reason = "ترسل فارسي"
            if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}"):
                return await message.reply_text(
                    warner.format(mention, k, reason), disable_web_page_preview=True
                )

    if r.get(f"{message.chat.id}:lockPersian:{Dev_Zaid}") and message.caption:
        if "ه‍" in message.caption or "ی" in message.caption or "ک" in message.caption or "چ" in message.caption:
            await message.delete()
            warn = True
            reason = "ترسل فارسي"
            if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}"):
                return await message.reply_text(
                    warner.format(mention, k, reason), disable_web_page_preview=True
                )

    if (
        r.get(f"{message.chat.id}:lockUrls:{Dev_Zaid}")
        and message.text
        and len(Find(message.text_html)) > 0
    ):
        await message.delete()
        warn = True
        reason = "ترسل روابط"
        if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}", 1, ex=60)
            return await message.reply_text(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if (
        r.get(f"{message.chat.id}:lockHashtags:{Dev_Zaid}")
        and message.text
        and len(re.findall(r"#(\w+)", message.text)) > 0
    ):
        await message.delete()
        warn = True
        reason = "ترسل هاشتاق"
        if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}", 1, ex=60)
            return await message.reply_text(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{message.chat.id}:lockMessages:{Dev_Zaid}") and message.text and len(message.text) > 150:
        await message.delete()
        warn = True
        reason = "ترسل كلام كثير"
        if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}", 1, ex=60)
            return await message.reply_text(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{message.chat.id}:lockVoice:{Dev_Zaid}") and message.voice:
        await message.delete()
        warn = True
        reason = "ترسل فويس"
        if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}", 1, ex=60)
            return await message.reply_text(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(
        f"{message.chat.id}:lockTags:{Dev_Zaid}"
    ) and '"type": "MessageEntity.MENTION"' in str(m):
        await message.delete()
        warn = True
        reason = "ترسل منشنات"
        if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
            f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}"
        ):
            r.set(f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}", 1, ex=60)
            return await message.reply_text(
                warner.format(mention, k, reason), disable_web_page_preview=True
            )

    if r.get(f"{message.chat.id}:lockSHTM:{Dev_Zaid}") and (message.caption or message.text):
        if message.caption:
            txt = message.caption
        if message.text:
            txt = message.text
        for a in list_UwU:
            if txt == a or f" {a} " in txt or a in txt:
                await message.delete()
                warn = True
                reason = "السب هنا"
                if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}") and not r.get(
                    f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}"
                ):
                    r.set(f"{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}", 1, ex=60)
                    return await message.reply_text(
                        warner.format(mention, k, reason), disable_web_page_preview=True
                    )

    """
  if r.get(f'{message.chat.id}:lockKFR:{Dev_Zaid}') and (message.caption or message.text):
     if message.caption:
         txt = message.caption.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","").replace("ـ","").replace("َ","").replace("ٕ","").replace("ُ","").replace("ِ","").replace("ٰ","").replace("ٖ","").replace("ً","").replace("ّ","").replace("ٌ","").replace("ٍ","").replace("ْ","").replace("ٔ","").replace("'","").replace('"',"")
     if message.text:
         txt = message.text.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","").replace("ـ","").replace("َ","").replace("ٕ","").replace("ُ","").replace("ِ","").replace("ٰ","").replace("ٖ","").replace("ً","").replace("ّ","").replace("ٌ","").replace("ٍ","").replace("ْ","").replace("ٔ","").replace("'","").replace('"',"")
     for kfr in list_Shiaa:
         if kfr in txt:
            await message.delete()
            warn = True
            reason = 'الكفر هنا'
            if not r.get(f'{message.chat.id}:disableWarn:{Dev_Zaid}') and not r.get(f'{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}'):
                 r.set(f'{Dev_Zaid}:inWARN:{actor_id}{message.chat.id}',1,ex=60)
                 return await message.reply_text(warner.format(mention,k,reason),disable_web_page_preview=True)
  """

    if r.get(f"{message.chat.id}:lockJoinPersian:{Dev_Zaid}") and message.new_chat_members:
        if message.from_user.first_name:
            if (
                message.from_user.first_name in persianInformation["names"]
                or actor_id in persianInformation["ids"]
                or "ه‍" in message.from_user.first_name
                or "ی" in message.from_user.first_name
                or "ک" in message.from_user.first_name
                or "چ" in message.from_user.first_name
                or "👙" in message.from_user.first_name
            ) and not pre_pls(actor_id, message.chat.id):
                if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}"):
                    await message.reply_text(
                        """
「 {} 」
{} تم حظره لاشتباهه ببوت إيراني
☆
""".format(message.from_user.mention_html(), k)
                    )
                return await context.bot.ban_chat_member(message.chat.id, actor_id)

        if message.from_user.last_name:
            if (
                message.from_user.last_name in persianInformation["last_names"]
                or actor_id in persianInformation["ids"]
                or "ه‍" in message.from_user.last_name
                or "ی" in message.from_user.last_name
                or "ک" in message.from_user.last_name
                or "چ" in message.from_user.last_name
                or "👙" in message.from_user.last_name
            ) and not pre_pls(actor_id, message.chat.id):
                if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}"):
                    await message.reply_text(
                        """
「 {} 」
{} تم حظره لاشتباهه ببوت إيراني
☆
""".format(message.from_user.mention_html(), k)
                    )
                return await context.bot.ban_chat_member(message.chat.id, actor_id)

    if r.get(f"{message.chat.id}:enableVerify:{Dev_Zaid}") and message.new_chat_members:
        for me in message.new_chat_members:
            if not pre_pls(me.id, message.chat.id):
                await context.bot.restrict_chat_member(
                    message.chat.id, me.id, ChatPermissions(can_send_messages=False)
                )
                get_random = get_for_verify(me)
                question = get_random["question"]
                reply_markup = get_random["key"]
                return await message.reply_text(
                    f"{k} قيدناك عشان نتاكد انك شخص حقيقي مو زومبي\n\n{question}",
                    reply_markup=reply_markup,
                )

    if message.effective_attachment and r.get(f"{message.chat.id}:lockNSFW:{Dev_Zaid}"):
        print("nsfw scanner")
        if not admin_pls(id, message.chat.id):
            if message.sticker:
                id = message.sticker.thumbnail.file_id
            if message.photo:
                id = message.photo[-1].file_id
            if message.video:
                id = message.video.thumbnail.file_id
            if message.animation:
                id = message.animation.thumbnail.file_id
        file = id
        try:
            await scanR(update, context, id, file)
        except Exception as _e:
            import logging; logging.getLogger(__name__).error(f"scanR error: {_e}", exc_info=True)

async def scanR(update: Update, context: ContextTypes.DEFAULT_TYPE, id, file):
    if not update:
        return
    event = update.message or update.callback_query or update.chat_join_request
    if not event:
        return
    message = event
    user = update.effective_user
    chat = update.effective_chat
    await scan4(update, context, id, file)

async def scan4(update: Update, context: ContextTypes.DEFAULT_TYPE, id, file):
    if not update:
        return
    event = update.message or update.callback_query or update.chat_join_request
    if not event:
        return
    if ARQ is None:
        return
    message = event
    user = update.effective_user
    chat = update.effective_chat
    session = ClientSession()
    arq = ARQ(ARQ_API_URL, ARQ_API_KEY, session)
    resp = await arq.nsfw_scan(file=file)
    if resp.result.is_nsfw:
        print("xNSFW")
        await  message.delete()
        k = r.get(f"{Dev_Zaid}:botkey") or "☆"
        await  message.reply_text(
            f"「 {message.from_user.mention_html()} 」\n{k} تم حذف رسالتك لإحتوائها على محتوى إباحي .\n☆"
        )
    os.remove(file)
    await session.close()

def get_for_verify(me):
    for_verify = [
        {
            "question": "ماهو الحيوان الذي ينتهي اسمه بحرف الباء ؟",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("فأر", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("وشق", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("بشار الأسد", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("حمار", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("كلب", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("قطة", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "ماهي عاصمة فرنسا؟",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("دمشق", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الرياض", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("باريس", callback_data=f"yes:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("الكويت", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("القاهرة", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("ماشا والدب", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "نادي يبدأ بحرف الباء :",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("برشلونا", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("الهلال", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("النصر", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("الزمالك", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("ريال مدريد", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("مانشستر", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "دولة يبدأ اسمها بحرف التاء :",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("قطر", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("امريكا", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("سوريا", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("مصر", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الصين", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("تركيا", callback_data=f"yes:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اختر هذا الايموجي - 🤑 -",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🍭", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🤑", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("🏆", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("🌀", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🪨", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("💎", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اختر هذا الايموجي - 🔓 -",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🏆", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("💎", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🙄", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("💸", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("💣", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🔓", callback_data=f"yes:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اختر هذا الايموجي - 🌠 -",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("☄️", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🙈", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🦄", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("🌠", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("🌈", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("🧑‍💻", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "ماهي عاصمة سوريا",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("دمشق", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("دير الزور", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("ادلب", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("ليو ميسي", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الرياض", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("مزة فيلات", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "ماهي عملة الولايات المتحدة الأمريكية",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("الروبية", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الجنيه", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الليرة", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("الدولار", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("الدينار", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("الين", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اسم مذكر يبدأ بحرف ز",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("زيد", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("علي", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("محمد", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("عمر", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("المريخ", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("احمد", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اسم مؤنث ينتهي بحرف ي",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("لورين", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("ماجدة", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("علياء", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("أماني", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("فرح", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("أمل", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "اسم مؤنث يبدأ بحرف أ",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("لورين", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("ماجدة", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("علياء", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("أمل", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("فرح", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("يمنى", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
        {
            "question": "الأسبوع كم يوم؟",
            "key": InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("1", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("2", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("3", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("4", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("5", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("6", callback_data=f"no:{me.id}"),
                    ],
                    [
                        InlineKeyboardButton("7", callback_data=f"yes:{me.id}"),
                        InlineKeyboardButton("8", callback_data=f"no:{me.id}"),
                        InlineKeyboardButton("9", callback_data=f"no:{me.id}"),
                    ],
                ]
            ),
        },
    ]
    return random.choice(for_verify)

# Converted Pyrogram on_chat_join_request handler
async def antiPersian(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update:
        return
    event = update.message or update.callback_query or update.chat_join_request
    if not event:
        return
    message = event
    user = update.effective_user
    chat = update.effective_chat
    if r.get(f"{message.chat.id}:lockJoinPersian:{Dev_Zaid}"):
        k = r.get(f'{Dev_Zaid}:botkey') or '☆'
        if not pre_pls(actor_id, message.chat.id):
            if message.from_user.first_name:
                if (
                    message.from_user.first_name in persianInformation["names"]
                    or actor_id in persianInformation["ids"]
                    or "ه‍" in message.from_user.first_name
                    or "ی" in message.from_user.first_name
                    or "ک" in message.from_user.first_name
                    or "چ" in message.from_user.first_name
                    or "👙" in message.from_user.first_name
                ):
                    await context.bot.decline_chat_join_request(message.chat.id, actor_id)
                    if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}"):
                        await context.bot.send_message(
                            message.chat.id,
                            """
「 {} 」
{} تم رفض طلب انضمامه لاشتباهه ببوت إيراني
☆
""".format(message.from_user.mention_html(), k),
                        )
                    return True
            if message.from_user.last_name:
                if (
                    message.from_user.last_name in persianInformation["last_names"]
                    or actor_id in persianInformation["ids"]
                    or "ه‍" in message.from_user.last_name
                    or "ی" in message.from_user.last_name
                    or "ک" in message.from_user.last_name
                    or "چ" in message.from_user.last_name
                    or "👙" in message.from_user.last_name
                ):
                    await context.bot.decline_chat_join_request(message.chat.id, actor_id)
                    if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}"):
                        await context.bot.send_message(
                            message.chat.id,
                            """
「 {} 」
{} تم رفض طلب انضمامه لاشتباهه ببوت إيراني
☆
""".format(message.from_user.mention_html(), k),
                        )
                    return True

# Converted Pyrogram on_message handler
async def guardCommandsHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update:
        return
    event = update.message or update.callback_query or update.chat_join_request
    if not event:
        return
    message = event
    user = update.effective_user
    chat = update.effective_chat
    k = r.get(f"{Dev_Zaid}:botkey") or "☆"
    channel = (
        r.get(f"{Dev_Zaid}:BotChannel") if r.get(f"{Dev_Zaid}:BotChannel") else "scatteredda"
    )
    try:
        await guardCommands(update, context, k, channel)
    except Exception as _e:
        import logging; logging.getLogger(__name__).error(f"guardCommands error: {_e}", exc_info=True)

async def guardCommands(update: Update, context: ContextTypes.DEFAULT_TYPE, k, channel):
    if not update:
        return
    event = update.message or update.callback_query or update.chat_join_request
    if not event:
        return
    message = event
    user = update.effective_user
    chat = update.effective_chat
    if not user:
        return
    actor_id = user.id
    mention = f"[{user.first_name}](tg://user?id={user.id})"

    if not message.text:
        return

    # ===== مزامنة صلاحيات تيليغرام مع نظام رتب البوت =====
    if chat and chat.type not in ("private",):
        try:
            from telegram.constants import ChatMemberStatus as _CMS
            _tg_member = await context.bot.get_chat_member(chat.id, actor_id)
            if _tg_member.status == _CMS.OWNER:
                # مالك المجموعة → يحصل على رتبة gowner
                if not r.get(f"{chat.id}:rankGOWNER:{actor_id}{Dev_Zaid}"):
                    r.set(f"{chat.id}:rankGOWNER:{actor_id}{Dev_Zaid}", 1)
                    r.sadd(f"{chat.id}:listGOWNER:{Dev_Zaid}", actor_id)
            elif _tg_member.status == _CMS.ADMINISTRATOR:
                # مشرف تيليغرام → يحصل على رتبة admin إذا لم تكن لديه رتبة
                if not admin_pls(actor_id, chat.id):
                    r.set(f"{chat.id}:rankADMIN:{actor_id}{Dev_Zaid}", 1)
                    r.sadd(f"{chat.id}:listADMIN:{Dev_Zaid}", actor_id)
        except Exception:
            pass
    # =================================================================

    # ===== أوامر تفعيل/تعطيل البوت (تعمل حتى لو البوت مو مفعل) =====
    k_val = k or "⇜"
    if message.text.strip() == "تفعيل البوت":
        try:
            from telegram.constants import ChatMemberStatus as CMS
            member = await context.bot.get_chat_member(chat.id, actor_id)
            if member.status == CMS.OWNER or dev_pls(actor_id, chat.id):
                r.set(f"{chat.id}:enable:{Dev_Zaid}", 1)
                return await message.reply_text(f"{k_val} ابشر فعّلت البوت في المجموعة")
            else:
                return await message.reply_text(f"{k_val} هذا الأمر يخص مالك المجموعة فقط")
        except Exception as e:
            return await message.reply_text(f"خطأ: {e}")

    if message.text.strip() == "تعطيل البوت":
        try:
            from telegram.constants import ChatMemberStatus as CMS
            member = await context.bot.get_chat_member(chat.id, actor_id)
            if member.status == CMS.OWNER or dev_pls(actor_id, chat.id):
                r.delete(f"{chat.id}:enable:{Dev_Zaid}")
                return await message.reply_text(f"{k_val} تم تعطيل البوت في المجموعة")
            else:
                return await message.reply_text(f"{k_val} هذا الأمر يخص مالك المجموعة فقط")
        except Exception as e:
            return await message.reply_text(f"خطأ: {e}")
    # ===================================================================

    if chat and chat.type not in ("private",) and not dev_pls(actor_id, chat.id) and not r.get(f"{chat.id}:enable:{Dev_Zaid}"):
        return False
    if r.get(f"{message.chat.id}:mute:{Dev_Zaid}") and not admin_pls(
        actor_id, message.chat.id
    ):
        return False
    if r.get(f"{actor_id}:mute:{message.chat.id}{Dev_Zaid}"):
        return False
    if r.get(f"{actor_id}:mute:{Dev_Zaid}"):
        return False
    if r.get(f"{message.chat.id}:addCustom:{actor_id}{Dev_Zaid}"):
        return False
    if r.get(f"{message.chat.id}addCustomG:{actor_id}{Dev_Zaid}"):
        return False
    if r.get(f"{message.chat.id}:delCustom:{actor_id}{Dev_Zaid}") or r.get(
        f"{message.chat.id}:delCustomG:{actor_id}{Dev_Zaid}"
    ):
        return False
    text = (message.text or "").strip()
    name = r.get(f"{Dev_Zaid}:BotName") or NAME

    if text.startswith(f"{name} "):
        text = text.replace(f"{name} ", "", 1).strip()
    if r.get(f"{message.chat.id}:Custom:{message.chat.id}{Dev_Zaid}&text={text}"):
        text = r.get(f"{message.chat.id}:Custom:{message.chat.id}{Dev_Zaid}&text={text}")
    if r.get(f"Custom:{Dev_Zaid}&text={text}"):
        text = r.get(f"Custom:{Dev_Zaid}&text={text}")
    if isLockCommand(actor_id, message.chat.id, text):
        return
    Open = """
{} من 「 {} 」
{} ابشر فتحت {}
☆
"""
    Openn = """
{} من 「 {} 」
{} {} مفتوح من قبل
☆
"""
    Openn2 = """
{} من 「 {} 」
{} {} مفتوحه من قبل
☆
"""

    lock = """
{} من 「 {} 」
{} ابشر قفلت {}
☆
"""

    lockn = """
{} من 「 {} 」
{} {} مقفل من قبل
☆
"""
    locknn = """
{} من 「 {} 」
{} {} مقفله من قبل
☆
"""

    if text == "الاعدادات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            x1 = "مقفول" if r.get(f"{message.chat.id}:lockAudios:{Dev_Zaid}") else "مفتوح"
            x2 = "مقفول" if r.get(f"{message.chat.id}:lockVideo:{Dev_Zaid}") else "مفتوح"
            x3 = "مقفول" if r.get(f"{message.chat.id}:lockVoice:{Dev_Zaid}") else "مفتوح"
            x4 = "مقفول" if r.get(f"{message.chat.id}:lockPhoto:{Dev_Zaid}") else "مفتوح"
            x5 = "مقفول" if r.get(f"{message.chat.id}:mute:{Dev_Zaid}") else "مفتوح"
            x6 = "مقفول" if r.get(f"{message.chat.id}:lockInline:{Dev_Zaid}") else "مفتوح"
            x7 = "مقفول" if r.get(f"{message.chat.id}:lockForward:{Dev_Zaid}") else "مفتوح"
            x8 = "مقفول" if r.get(f"{message.chat.id}:lockHashtags:{Dev_Zaid}") else "مفتوح"
            x9 = "مقفول" if r.get(f"{message.chat.id}:lockEdit:{Dev_Zaid}") else "مفتوح"
            x10 = "مقفول" if r.get(f"{message.chat.id}:lockStickers:{Dev_Zaid}") else "مفتوح"
            x11 = "مقفول" if r.get(f"{message.chat.id}:lockFiles:{Dev_Zaid}") else "مفتوح"
            x12 = (
                "مقفول" if r.get(f"{message.chat.id}:lockAnimations:{Dev_Zaid}") else "مفتوح"
            )
            x13 = "مقفول" if r.get(f"{message.chat.id}:lockUrls:{Dev_Zaid}") else "مفتوح"
            x14 = "مقفول" if r.get(f"{message.chat.id}:lockBots:{Dev_Zaid}") else "مفتوح"
            x15 = "مقفول" if r.get(f"{message.chat.id}:lockTags:{Dev_Zaid}") else "مفتوح"
            x16 = "مقفول" if r.get(f"{message.chat.id}:lockNot:{Dev_Zaid}") else "مفتوح"
            x17 = (
                "مقفول" if r.get(f"{message.chat.id}:lockaddContacts:{Dev_Zaid}") else "مفتوح"
            )
            x18 = "مقفول" if r.get(f"{message.chat.id}:lockMessages:{Dev_Zaid}") else "مفتوح"
            x19 = "مقفول" if r.get(f"{message.chat.id}:lockSHTM:{Dev_Zaid}") else "مفتوح"
            x20 = "مقفول" if r.get(f"{message.chat.id}:lockSpam:{Dev_Zaid}") else "مفتوح"
            x21 = "مقفول" if r.get(f"{message.chat.id}:lockChannels:{Dev_Zaid}") else "مفتوح"
            x22 = "مقفول" if r.get(f"{message.chat.id}:lockEditM:{Dev_Zaid}") else "مفتوح"
            x23 = "مقفول" if r.get(f"{message.chat.id}:lockJoin:{Dev_Zaid}") else "مفتوح"
            x24 = "مقفول" if r.get(f"{message.chat.id}:lockPersian:{Dev_Zaid}") else "مفتوح"
            x25 = (
                "مقفول" if r.get(f"{message.chat.id}:lockJoinPersian:{Dev_Zaid}") else "مفتوح"
            )
            x26 = "مقفول" if r.get(f"{message.chat.id}:lockNSFW:{Dev_Zaid}") else "مفتوح"
            return await message.reply_text(f"""
اعدادات المجموعة :

{k} الملفات الصوتية ⇠ ( {x1} )
{k} الفيديو ⇠ ( {x2} )
{k} الفويس ⇠ ( {x3} )
{k} الصور ⇠ ( {x4} )

{k} الدردشة ⇠ ( {x5} )
{k} الانلاين ⇠ ( {x6} )
{k} التوجيه ⇠ ( {x7} )
{k} الهشتاق ⇠ ( {x8} )
{k} التعديل ⇠ ( {x9} )
{k} الستيكرات ⇠ ( {x10} )

{k} الملفات ⇠ ( {x11} )
{k} المتحركات ⇠ ( {x12} )
{k} الروابط ⇠ ( {x13} )
{k} البوتات ⇠ ( {x14} )
{k} اليوزرات ⇠ ( {x15} )

{k} الاشعارات ⇠ ( {x16} )
{k} الاضافة ⇠ ( {x17} )

{k} الكلام الكثير ⇠ ( {x18} )
{k} السب ⇠ ( {x19} )
{k} التكرار ⇠ ( {x20} )
{k} القنوات ⇠ ( {x21} )
{k} تعديل الميديا ⇠ ( {x22} )

{k} الدخول ⇠ ( {x23} )
{k} الفارسية ⇠ ( {x24} )
{k} دخول الإيراني ⇠ ( {x25} )
{k} الإباحي ⇠ ( {x26} )

~ @{channel}""")

    if text == "الساعه" or text == "الساعة" or text == "الوقت":
        TIME_ZONE = "Asia/Riyadh"
        ZONE = pytz.timezone(TIME_ZONE)
        TIME = datetime.now(ZONE)
        clock = TIME.strftime("%I:%M %p")
        return await message.reply_text(f"{k} الساعة ( {clock} )")

    if text == "القوانين":
        if r.get(f"{message.chat.id}:CustomRules:{Dev_Zaid}"):
            rules = r.get(f"{message.chat.id}:CustomRules:{Dev_Zaid}")
        else:
            rules = f"""{k} ممنوع نشر الروابط
{k} ممنوع التكلم او نشر صور اباحيه
{k} ممنوع اعاده توجيه
{k} ممنوع العنصرية بكل انواعها
{k} الرجاء احترام المدراء والادمنيه"""
        return await message.reply_text(rules, disable_web_page_preview=True)

    if text == "التاريخ":
        b = Hijri.today().isoformat()
        a = b.split("-")
        year = int(a[0])
        month = int(a[1])
        day = int(a[2])
        hijri = Hijri(year, month, day)
        hijri_date = str(b).replace("-", "/")
        hijri_month = hijri.month_name("ar")

        b = Gregorian.today().isoformat()
        a = b.split("-")
        year = int(a[0])
        month = int(a[1])
        day = int(a[2])
        geo = Gregorian(year, month, day)
        geo_date = str(b).replace("-", "/")
        geo_month = geo.month_name("en")[:3]

        return await message.reply_text(f"""
التاريخ:
{k} هجري ↢ {hijri_date} {hijri_month}
{k} ميلادي ↢ {geo_date} {geo_month}
""")

    if text == "المالك":
        owner = None
        for mm in await context.bot.get_chat_administrators(chat.id):
            if mm.status == ChatMemberStatus.OWNER:
                owner = mm.user
                break
        if owner:
            if owner.is_deleted:
                await message.reply_text("حساب المالك محذوف")
            else:
                owner_username = owner.username if owner.username else str(owner.id)
                owner_name = owner.full_name or owner.first_name or "المالك"
                caption = f"• Owner ☆ ↦ <a href='tg://user?id={owner.id}'>{owner_name}</a>\n\n"
                caption += f"• Owner User ↦ @{owner_username}"
                button = InlineKeyboardMarkup(
                    [[InlineKeyboardButton(owner_name, url=f"tg://user?id={owner.id}")]]
                )
                try:
                    photos = await context.bot.get_user_profile_photos(owner.id, limit=1)
                    if photos and photos.photos:
                        photo_file_id = photos.photos[0][-1].file_id
                        await message.reply_photo(
                            photo=photo_file_id, caption=caption,
                            reply_markup=button, parse_mode="HTML"
                        )
                    else:
                        await message.reply_text(caption, reply_markup=button, parse_mode="HTML")
                except Exception:
                    await message.reply_text(caption, reply_markup=button, parse_mode="HTML")

    if text == "اطردني":
        if r.get(f"{message.chat.id}:enableKickMe:{Dev_Zaid}"):
            get = await context.bot.get_chat_member(message.chat.id, actor_id)
            if get.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
                return await message.reply_text(f"{k} ممنوع طرد الحلوين")
            if admin_pls(actor_id, message.chat.id):
                return await message.reply_text(f"{k} ممنوع طرد الحلوين")
            else:
                await message.reply_text(
                    f"طردتك يانفسية , وارسلت لك الرابط خاص تقدر ترجع متى مابغيت يامعقد"
                )
                await context.bot.ban_chat_member(chat.id, actor_id)
                await asyncio.sleep(0.5)
                await context.bot.unban_chat_member(message.chat.id, actor_id)
                link = context.bot.get_chat(message.chat.id).invite_link
                try:
                    await context.bot.send_message(
                        actor_id,
                        f"{k} حبيبي النفسية رابط القروب الي طردتك منه: {link}",
                    )
                except:
                    pass
                return False

    if text == "الرابط":
        if not r.get(f"{message.chat.id}:disableLINK:{Dev_Zaid}"):
            link = context.bot.get_chat(message.chat.id).invite_link
            return await message.reply_text(f"[{message.chat.title}]({link})", disable_web_page_preview=True)

    if text == "انشاء رابط":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        link = context.bot.get_chat(message.chat.id).invite_link
        context.bot.revoke_chat_invite_link(message.chat.id, link)
        return await message.reply_text(f'{k} ابشر سويت رابط جديد ارسل "الرابط"')

    if text.startswith("@all"):
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        if r.get(f"{message.chat.id}:disableALL:{Dev_Zaid}"):
            return await message.reply_text("المنشن معطل")
        if r.get(f"{message.chat.id}:inMention:{Dev_Zaid}"):
            return False
        if r.get(f"{message.chat.id}:inMentionWAIT:{Dev_Zaid}"):
            get = r.ttl(f"{message.chat.id}:inMentionWAIT:{Dev_Zaid}")
            tm = time.strftime("%M:%S", time.gmtime(get))
            return await message.reply_text(f"{k} سويت منشن من شوي تعال بعد {tm}")
        else:
            if len(text.split()) > 1:
                reason = text.split(None, 1)[1]
            else:
                reason = ""
            users_list = []
            r.set(f"{message.chat.id}:inMention:{Dev_Zaid}", 1)
            await message.reply_text(f"{k} بسوي منشن يحلو ، اذا تبي توقفه ارسل `/Cancel` او `ايقاف`")
            for mm in []:
                if mm.user and not mm.user.is_deleted and not mm.user.is_bot:
                    users_list.append(mm.user.mention_html())
            final_list = [users_list[x : x + 5] for x in range(0, len(users_list), 5)]
            ftext = f"{reason}\n\n"
            for a in final_list:
                for i in a:
                    if not r.get(f"{message.chat.id}:inMention:{Dev_Zaid}"):
                        return False
                    ftext += f"{i} , "
                await context.bot.send_message(message.chat.id, ftext)
                ftext = f"{reason}\n\n"
            r.delete(f"{message.chat.id}:inMention:{Dev_Zaid}")
            r.set(f"{message.chat.id}:inMentionWAIT:{Dev_Zaid}", 1, ex=1200)

    if text.lower() == "/cancel" or text == "ايقاف":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:inMention:{Dev_Zaid}"):
                return await message.reply_text(f"{k} مو قاعده اسوي منشن ركز")
            else:
                r.delete(f"{message.chat.id}:inMention:{Dev_Zaid}")
                return await message.reply_text("ابشر وقفت المنشن")

    if text == "منشن":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        return await message.reply_text("استخدم امر\n@all مع الكلام")

    if text == "تعطيل المنشن":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:disableALL:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} المشن معطل من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:disableALL:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت المنشن\n☆"
                )

    if text == "تفعيل المنشن":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:disableALL:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} المنشن مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:disableALL:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت المنشن\n☆"
                )

    if text == "تعطيل الترحيب":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:disableWelcome:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} الترحيب معطل من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:disableWelcome:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت الترحيب\n☆"
                )

    if text == "تعطيل الترحيب بالصورة" or text == "تعطيل الترحيب بالصوره":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:disableWelcomep:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} الترحيب بالصورة من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:disableWelcomep:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت الترحيب بالصورة\n☆"
                )

    if text == "تفعيل الترحيب بالصورة" or text == "تفعيل الترحيب بالصوره":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:disableWelcomep:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} الترحيب بالصورة مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:disableWelcomep:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت الترحيب بالصورة\n☆"
                )

    if text == "تعطيل الرابط":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:disableLINK:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} الرابط معطل من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:disableLINK:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت الرابط\n☆"
                )

    if text == "تفعيل الرابط":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:disableLINK:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} الرابط مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:disableLINK:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت الرابط\n☆"
                )

    if text == "تعطيل البايو":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:disableBio:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} البايو معطل من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:disableBio:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت البايو\n☆"
                )

    if text == "تفعيل البايو":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:disableBio:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} البايو مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:disableBio:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت البايو\n☆"
                )

    if text == "تعطيل اطردني":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:enableKickMe:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} اطردني معطل من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:enableKickMe:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت اطردني\n☆"
                )

    if text == "تفعيل اطردني":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:enableKickMe:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} اطردني مفعل من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:enableKickMe:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت اطردني\n☆"
                )

    if text == "تعطيل التحقق":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:enableVerify:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} التحقق معطل من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:enableVerify:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت التحقق\n☆"
                )

    if text == "تفعيل التحقق":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:enableVerify:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} التحقق مفعل من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:enableVerify:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت التحقق\n☆"
                )

    if text == "تعطيل انطقي" or text == "تعطيل انطق":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:disableSay:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} انطقي معطل من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:disableSay:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت انطقي\n☆"
                )

    if text == "تفعيل انطقي" or text == "تفعيل انطق":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:disableSay:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} انطقي مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:disableSay:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت انطقي\n☆"
                )

    if text.startswith("انطق "):
        if not r.get(f"{message.chat.id}:disableSay:{Dev_Zaid}"):
            txt = text.split(None, 1)[1]
            if len(txt) > 500:
                return await message.reply_text("توكل مايمدي انطق اكثر من ٥٠٠ حرف بتعب بعدين")
            """
         det = translator.detect(txt).lang.lower()
         if det == 'fa' or det == 'ar':
           lang = 'ar'
         else:
           lang = det
         """
            id = random.randint(999, 10000)
            """
         o = gtts.gTTS(text=txt, lang="ar", slow=False)
         o.save(f'zaid{id}.mp3')
         """
            with open(f"zaid{id}.mp3", "wb") as f:
                try:
                    context.bot.send_chat_action(message.chat.id, ChatAction.RECORD_AUDIO)
                except:
                    pass
                f.write(
                    requests.get(
                        f"https://eduardo-tate.com/AI/voice.php?text={txt}&model=3"
                    ).content
                )
            """
         audio = MP3(f'zaid{id}.mp3')
         duration=int(audio.info.length)
         os.rename(f'zaid{id}.mp3',f'zaid{id}.ogg')
         TelegramBot.send_voice(
         message.chat.id,
         voice,
         caption=f'الكلمة: {txt}',
         duration=duration
         )
         """
            try:
                context.bot.send_chat_action(message.chat.id, ChatAction.RECORD_AUDIO)
            except:
                pass
            os.system(
                f"ffmpeg -i zaid{id}.mp3 -ac 1 -strict -2 -codec:a libopus -b:a 128k -vbr off -ar 24000 zaid{id}.ogg"
            )
            try:
                context.bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_AUDIO)
            except:
                pass
            await message.reply_voice(f"zaid{id}.ogg", caption=f"الكلمة: {txt}")
            """
         voice = open(f'zaid{id}.ogg','rb')
         url = f"https://api.telegram.org/bot{context.bot.bot_token}/sendVoice"
         response=requests.post(url, data={'chat_id': message.chat.id,'caption':f'الكلمة: {txt}','reply_to_message_id':message.message_id}, files={'voice': voice})
         os.remove(f'zaid{id}.ogg')
         """
            os.remove(f"zaid{id}.ogg")
            os.remove(f"zaid{id}.mp3")
            return True

    if text.startswith("انطقي "):
        if not r.get(f"{message.chat.id}:disableSay:{Dev_Zaid}"):
            txt = text.split(None, 1)[1]
            if len(txt) > 500:
                return await message.reply_text("توكل مايمدي انطق اكثر من ٥٠٠ حرف بتعب بعدين")
            """
         det = translator.detect(txt).lang.lower()
         if det == 'fa' or det == 'ar':
           lang = 'ar'
         else:
           lang = det
         """
            id = random.randint(999, 10000)
            """
         o = gtts.gTTS(text=txt, lang="ar", slow=False)
         o.save(f'zaid{id}.mp3')
         """
            with open(f"zaid{id}.mp3", "wb") as f:
                try:
                    context.bot.send_chat_action(message.chat.id, ChatAction.RECORD_AUDIO)
                except:
                    pass
                f.write(
                    requests.get(
                        f"https://eduardo-tate.com/AI/voice.php?text={txt}"
                    ).content
                )
            """
         audio = MP3(f'zaid{id}.mp3')
         duration=int(audio.info.length)
         os.rename(f'zaid{id}.mp3',f'zaid{id}.ogg')
         TelegramBot.send_voice(
         message.chat.id,
         voice,
         caption=f'الكلمة: {txt}',
         duration=duration
         )
         """
            try:
                context.bot.send_chat_action(message.chat.id, ChatAction.RECORD_AUDIO)
            except:
                pass
            os.system(
                f"ffmpeg -i zaid{id}.mp3 -ac 1 -strict -2 -codec:a libopus -b:a 128k -vbr off -ar 24000 zaid{id}.ogg"
            )
            try:
                context.bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_AUDIO)
            except:
                pass
            await message.reply_voice(f"zaid{id}.ogg", caption=f"الكلمة: {txt}")
            """
         voice = open(f'zaid{id}.ogg','rb')
         url = f"https://api.telegram.org/bot{context.bot.bot_token}/sendVoice"
         response=requests.post(url, data={'chat_id': message.chat.id,'caption':f'الكلمة: {txt}','reply_to_message_id':message.message_id}, files={'voice': voice})
         os.remove(f'zaid{id}.ogg')
         """
            os.remove(f"zaid{id}.ogg")
            os.remove(f"zaid{id}.mp3")
            return True

    if (
        (text == "وش يقول" or text == "وش تقول؟")
        and message.reply_to_message
        and message.reply_to_message.voice
    ):
        if message.reply_to_message.voice.file_size > 20971520:
            return await message.reply_text("حجمه اكثر من ٢٠ ميجابايت، توكل")
        id = random.randint(99, 1000)
        voice = message.reply_to_message.download(f"./zaid{id}.wav")
        s = sr.Recognizer()
        sound = AudioSegment.from_ogg(voice)
        wav_file = sound.export(voice, format="wav")
        with sr.AudioFile(wav_file) as src:
            audio_source = s.record(src)
        try:
            text = s.recognize_google(audio_source, language="ar-SA")
        except Exception as e:
            print(e)
            os.remove(f"zaid{id}.wav")
            return await message.reply_text("عجزت افهم وش يقول ")
        os.remove(f"zaid{id}.wav")
        return await message.reply_text(f"يقول : {text}")

    if (
        (text == "zaid" or text == "زوز")
        and message.reply_to_message
        and message.reply_to_message.voice
        and actor_id == 6168217372
    ):
        if message.reply_to_message.voice.file_size > 20971520:
            return await message.reply_text("حجمه اكثر من ٢٠ ميجابايت، توكل")
        id = random.randint(99, 1000)
        voice = message.reply_to_message.download(f"./zaid{id}.wav")
        s = sr.Recognizer()
        sound = AudioSegment.from_ogg(voice)
        wav_file = sound.export(voice, format="wav")
        with sr.AudioFile(wav_file) as src:
            audio_source = s.record(src)
        try:
            text = s.recognize_google(audio_source, language="en-US")
        except Exception as e:
            print(e)
            os.remove(f"zaid{id}.wav")
            return await message.reply_text("عجزت افهم وش يقول ")
        os.remove(f"zaid{id}.wav")
        return await message.reply_text(f"يقول : {text}")

    if text.startswith("منع "):
        if mod_pls(actor_id, message.chat.id):
            noice = text.split(None, 1)[1]
            if r.sismember(f"{message.chat.id}:NotAllowedListText:{Dev_Zaid}", noice):
                return await message.reply_text(
                    f"{k} الكلمة ( {noice} ) موجودة بقائمة المنع",
                    disable_web_page_preview=True,
                )
            else:
                r.sadd(f"{message.chat.id}:NotAllowedListText:{Dev_Zaid}", noice)
                return await message.reply_text(
                    f"{k} الكلمة ( {noice} ) اضفتها الى قائمة المنع",
                    disable_web_page_preview=True,
                )

    if text.startswith("الغاء منع ") and len(text.split()) > 2:
        if mod_pls(actor_id, message.chat.id):
            noice = text.split(None, 2)[2]
            if not r.sismember(f"{message.chat.id}:NotAllowedListText:{Dev_Zaid}", noice):
                return await message.reply_text(
                    f"{k} الكلمة ( {noice} ) مو مضافة بقائمة المنع",
                    disable_web_page_preview=True,
                )
            else:
                r.srem(f"{message.chat.id}:NotAllowedListText:{Dev_Zaid}", noice)
                return await message.reply_text(
                    f"{k} ابشر مسحت ( {noice} ) من قائمة المنع",
                    disable_web_page_preview=True,
                )

    if text == "منع" and message.reply_to_message and message.reply_to_message.effective_attachment:
        if mod_pls(actor_id, message.chat.id):
            rep = message.reply_to_message
            if rep.sticker:
                file_id = rep.sticker.file_id
                type = "sticker"
            if rep.animation:
                file_id = rep.animation.file_id
                type = "animation"
            if rep.photo:
                file_id = rep.photo[-1].file_id
                type = "photo"
            if rep.video:
                file_id = rep.video.file_id
                type = "video"
            if rep.voice:
                file_id = rep.voice.file_id
                type = "voice"
            if rep.audio:
                file_id = rep.audio.file_id
                type = "audio"
            if rep.document:
                file_id = rep.document.file_id
                type = "document"

            id = file_id[-6:]
            if r.get(f"{id}:NotAllow:{message.chat.id}{Dev_Zaid}"):
                return await message.reply_text(f"{k} موجودة بقائمة المنع")
            else:
                r.set(f"{id}:NotAllow:{message.chat.id}{Dev_Zaid}", 1)
                r.sadd(
                    f"{message.chat.id}:NotAllowedList:{Dev_Zaid}",
                    f"file={id}&by={actor_id}&type={type}&file_id={file_id}",
                )
                return await message.reply_text(f"{k} واضفناها لقائمة المنع")

    if text == "الغاء منع" and message.reply_to_message and message.reply_to_message.effective_attachment:
        if mod_pls(actor_id, message.chat.id):
            rep = message.reply_to_message
            if rep.sticker:
                file_id = rep.sticker.file_id
                type = "sticker"
            if rep.animation:
                file_id = rep.animation.file_id
                type = "animation"
            if rep.photo:
                file_id = rep.photo[-1].file_id
                type = "photo"
            if rep.video:
                file_id = rep.video.file_id
                type = "video"
            if rep.voice:
                file_id = rep.voice.file_id
                type = "voice"
            if rep.audio:
                file_id = rep.audio.file_id
                type = "audio"
            if rep.document:
                file_id = rep.document.file_id
                type = "document"

            id = file_id[-6:]
            if not r.get(f"{id}:NotAllow:{message.chat.id}{Dev_Zaid}"):
                return await message.reply_text(f"{k} مو موجودة بقائمة المنع")
            else:
                r.delete(f"{id}:NotAllow:{message.chat.id}{Dev_Zaid}")
                r.srem(
                    f"{message.chat.id}:NotAllowedList:{Dev_Zaid}",
                    f"file={id}&by={actor_id}&type={type}&file_id={file_id}",
                )
                return await message.reply_text(f"{k} ابشر شلتها من قائمه المنع")

    if text == "منع" and message.reply_to_message and not message.reply_to_message.effective_attachment:
        if mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} المنع بالرد فقط للوسائط")

    if text == "قائمه المنع" or text == "قائمة المنع":
        text1 = "الكلمات الممنوعة:\n"
        text2 = "الوسائط الممنوعة:\n"
        count = 1
        count2 = 1
        if mod_pls(actor_id, message.chat.id):
            if not r.smembers(
                f"{message.chat.id}:NotAllowedListText:{Dev_Zaid}"
            ) and not r.smembers(f"{message.chat.id}:NotAllowedList:{Dev_Zaid}"):
                return await message.reply_text(f"{k} مافي شي ممنوع")
            else:
                if not r.smembers(f"{message.chat.id}:NotAllowedListText:{Dev_Zaid}"):
                    text1 += "لايوجد"
                else:
                    for a in r.smembers(f"{message.chat.id}:NotAllowedListText:{Dev_Zaid}"):
                        text1 += f"{count} - {a}\n"
                        count += 1
                if not r.smembers(f"{message.chat.id}:NotAllowedList:{Dev_Zaid}"):
                    text2 += "لايوجد"
                else:
                    for a in r.smembers(f"{message.chat.id}:NotAllowedList:{Dev_Zaid}"):
                        g = a
                        id = g.split("file=")[1].split("&")[0]
                        by = g.split("by=")[1].split("&")[0]
                        type = g.split("type=")[1].split("&")[0]
                        text2 += (
                            f"{count2} - (`{id}`) ࿓ ( [{type}](tg://user?id={by}) )\n"
                        )
                return await message.reply_text(f"{text1}\n{text2}", disable_web_page_preview=True)

    if text == "مسح قائمه المنع" or text == "مسح قائمة المنع":
        if mod_pls(actor_id, message.chat.id):
            if not r.smembers(
                f"{message.chat.id}:NotAllowedListText:{Dev_Zaid}"
            ) and not r.smembers(f"{message.chat.id}:NotAllowedList:{Dev_Zaid}"):
                return await message.reply_text(f"{k} مافي شي ممنوع")
            else:
                if r.smembers(f"{message.chat.id}:NotAllowedListText:{Dev_Zaid}"):
                    r.delete(f"{message.chat.id}:NotAllowedListText:{Dev_Zaid}")
                if r.smembers(f"{message.chat.id}:NotAllowedList:{Dev_Zaid}"):
                    for a in r.smembers(f"{message.chat.id}:NotAllowedList:{Dev_Zaid}"):
                        file_id = a.split("file=")[1].split("&by=")[0]
                        r.delete(f"{file_id}:NotAllow:{message.chat.id}{Dev_Zaid}")
                r.delete(f"{message.chat.id}:NotAllowedList:{Dev_Zaid}")
                return await message.reply_text(f"{k} ابشر مسحت قائمة المنع")

    if text == "قفل الكل":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if (
                r.get(f"{message.chat.id}:mute:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockEdit:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockEditM:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockVoice:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockVideo:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockNot:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockPhoto:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockPersian:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockStickers:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockFiles:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockAnimations:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockUrls:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockHashtags:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockBots:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockTags:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockMessages:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockSpam:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockForward:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockSHTM:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockaddContacts:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockAudios:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockChannels:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockJoin:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockInline:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockNSFW:{Dev_Zaid}")
            ):
                return await message.reply_text(
                    f"{k} من 「 {message.from_user.mention_html()} 」 \n{k} كل شي مقفل يالطيب!\n☆"
                )
            else:
                await message.reply_text(f"{k} من 「 {message.from_user.mention_html()} 」 \n{k} ابشر قفلت كل شي\n☆")
                r.set(f"{message.chat.id}:mute:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockJoin:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockChannels:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockEdit:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockEditM:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockVoice:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockVideo:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockNot:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockPhoto:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockStickers:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockAnimations:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockFiles:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockPersian:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockUrls:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockHashtags:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockMessages:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockTags:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockBots:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockSpam:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockInline:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockForward:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockAudios:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockaddContacts:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockSHTM:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockNSFW:{Dev_Zaid}", 1)
                return False

    if text == "فتح الكل":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if (
                not r.get(f"{message.chat.id}:mute:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockEdit:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockEditM:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockVoice:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockVideo:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockNot:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockPhoto:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockPersian:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockStickers:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockFiles:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockAnimations:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockUrls:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockHashtags:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockBots:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockTags:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockMessages:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockSpam:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockForward:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockSHTM:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockaddContacts:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockAudios:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockChannels:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockJoin:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockInline:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockNSFW:{Dev_Zaid}")
            ):
                return await message.reply_text(
                    f"{k} من 「 {message.from_user.mention_html()} 」 \n{k} كل شي مفتوح يالطيب!\n☆"
                )
            else:
                await message.reply_text(f"{k} من 「 {message.from_user.mention_html()} 」 \n{k} ابشر فتحت كل شي\n☆")
                r.delete(f"{message.chat.id}:mute:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockJoin:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockChannels:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockEdit:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockEditM:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockVoice:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockVideo:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockNot:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockPhoto:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockStickers:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockAnimations:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockFiles:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockPersian:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockUrls:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockHashtags:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockMessages:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockTags:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockBots:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockSpam:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockInline:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockForward:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockAudios:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockaddContacts:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockSHTM:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockKFR:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockNSFW:{Dev_Zaid}")
                return False

    if text == "تفعيل الحماية" or text == "تفعيل الحمايه":
        if not owner_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المالك وفوق ) بس")
        else:
            if (
                r.get(f"{message.chat.id}:lockEditM:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockVoice:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockVideo:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockPhoto:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockPersian:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockStickers:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockFiles:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockAnimations:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockUrls:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockTags:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockMessages:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockSpam:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockForward:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockSHTM:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockAudios:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockChannels:{Dev_Zaid}")
                and r.get(f"{message.chat.id}:lockNSFW:{Dev_Zaid}")
            ):
                return await message.reply_text(
                    f"{k} من 「 {message.from_user.mention_html()} 」 \n{k} الحماية مفعله من قبل\n☆"
                )
            else:
                await message.reply_text(
                    f"{k} من 「 {message.from_user.mention_html()} 」 \n{k} ابشر فعلت الحمايه\n☆"
                )

                r.set(f"{message.chat.id}:lockChannels:{Dev_Zaid}", 1)
                r.delete(f"{message.chat.id}:disableWarn:{Dev_Zaid}")
                r.set(f"{message.chat.id}:lockVoice:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockVideo:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockPhoto:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockStickers:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockAnimations:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockFiles:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockPersian:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockUrls:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockTags:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockSpam:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockForward:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockAudios:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockSHTM:{Dev_Zaid}", 1)
                r.set(f"{message.chat.id}:lockNSFW:{Dev_Zaid}", 1)
                return False

    if text == "تعطيل الحماية" or text == "تعطيل الحمايه":
        if not owner_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المالك وفوق ) بس")
        else:
            if (
                r.get(f"{message.chat.id}:lockEditM:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockVoice:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockVideo:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockPhoto:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockPersian:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockStickers:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockFiles:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockAnimations:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockUrls:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockTags:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockMessages:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockSpam:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockForward:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockSHTM:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockAudios:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockChannels:{Dev_Zaid}")
                and not r.get(f"{message.chat.id}:lockNSFW:{Dev_Zaid}")
            ):
                return await message.reply_text(
                    f"{k} من 「 {message.from_user.mention_html()} 」 \n{k} الحماية معطله من قبل\n☆"
                )
            else:
                await message.reply_text(
                    f"{k} من 「 {message.from_user.mention_html()} 」 \n{k} ابشر عطلت الحمايه\n☆"
                )

                r.delete(f"{message.chat.id}:lockChannels:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockVoice:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockVideo:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockPhoto:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockStickers:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockAnimations:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockFiles:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockPersian:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockUrls:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockTags:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockSpam:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockForward:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockAudios:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockSHTM:{Dev_Zaid}")
                r.delete(f"{message.chat.id}:lockNSFW:{Dev_Zaid}")
                return False

    if text == "قفل الدردشة" or text == "قفل الدردشه" or text == "قفل الشات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:mute:{Dev_Zaid}"):
                return await message.reply_text(lockn.format(k, message.from_user.mention_html(), k, "الشات"))
            else:
                r.set(f"{message.chat.id}:mute:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "الشات"))

    if text == "فتح الدردشة" or text == "فتح الدردشه" or text == "فتح الشات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:mute:{Dev_Zaid}"):
                return await message.reply_text(Openn.format(k, message.from_user.mention_html(), k, "الشات"))
            else:
                r.delete(f"{message.chat.id}:mute:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "الشات"))

    if text == "قفل التعديل":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockEdit:{Dev_Zaid}"):
                return await message.reply_text(lockn.format(k, message.from_user.mention_html(), k, "التعديل"))
            else:
                r.set(f"{message.chat.id}:lockEdit:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "التعديل"))

    if text == "فتح التعديل":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockEdit:{Dev_Zaid}"):
                return await message.reply_text(Openn.format(k, message.from_user.mention_html(), k, "التعديل"))
            else:
                r.delete(f"{message.chat.id}:lockEdit:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "التعديل"))

    if text == "قفل تعديل الميديا":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockEditM:{Dev_Zaid}"):
                return await message.reply_text(lockn.format(k, message.from_user.mention_html(), k, "تعديل الميديا"))
            else:
                r.set(f"{message.chat.id}:lockEditM:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "تعديل الميديا"))

    if text == "فتح تعديل الميديا":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockEditM:{Dev_Zaid}"):
                return await message.reply_text(Openn.format(k, message.from_user.mention_html(), k, "تعديل الميديا"))
            else:
                r.delete(f"{message.chat.id}:lockEditM:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "تعديل الميديا"))

    if text == "قفل الفويسات" or text == "قفل البصمات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockVoice:{Dev_Zaid}"):
                return await message.reply_text(lockn.format(k, message.from_user.mention_html(), k, "الفويس"))
            else:
                r.set(f"{message.chat.id}:lockVoice:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "الفويس"))

    if text == "فتح الفويسات" or text == "فتح البصمات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockVoice:{Dev_Zaid}"):
                return await message.reply_text(Openn.format(k, message.from_user.mention_html(), k, "الفويس"))
            else:
                r.delete(f"{message.chat.id}:lockVoice:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "الفويس"))

    if text == "قفل الفيديو" or text == "قفل الفيديوهات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockVideo:{Dev_Zaid}"):
                return await message.reply_text(lockn.format(k, message.from_user.mention_html(), k, "الفيديو"))
            else:
                r.set(f"{message.chat.id}:lockVideo:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "الفيديو"))

    if text == "فتح الفيديو" or text == "فتح الفيديوهات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockVideo:{Dev_Zaid}"):
                return await message.reply_text(Openn.format(k, message.from_user.mention_html(), k, "الفيديو"))
            else:
                r.delete(f"{message.chat.id}:lockVideo:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "الفيديو"))

    if text == "قفل الاشعارات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockNot:{Dev_Zaid}"):
                return await message.reply_text(locknn.format(k, message.from_user.mention_html(), k, "الاشعارات"))
            else:
                r.set(f"{message.chat.id}:lockNot:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "الاشعارات"))

    if text == "فتح الاشعارات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockNot:{Dev_Zaid}"):
                return await message.reply_text(Openn2.format(k, message.from_user.mention_html(), k, "الاشعارات"))
            else:
                r.delete(f"{message.chat.id}:lockNot:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "الاشعارات"))

    if text == "قفل الصور":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockPhoto:{Dev_Zaid}"):
                return await message.reply_text(locknn.format(k, message.from_user.mention_html(), k, "الصور"))
            else:
                r.set(f"{message.chat.id}:lockPhoto:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "الصور"))

    if text == "فتح الصور":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockPhoto:{Dev_Zaid}"):
                return await message.reply_text(Openn2.format(k, message.from_user.mention_html(), k, "الصور"))
            else:
                r.delete(f"{message.chat.id}:lockPhoto:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "الصور"))

    if text == "قفل الملصقات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockStickers:{Dev_Zaid}"):
                return await message.reply_text(locknn.format(k, message.from_user.mention_html(), k, "الملصقات"))
            else:
                r.set(f"{message.chat.id}:lockStickers:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "الملصقات"))

    if text == "فتح الملصقات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockStickers:{Dev_Zaid}"):
                return await message.reply_text(Openn2.format(k, message.from_user.mention_html(), k, "الملصقات"))
            else:
                r.delete(f"{message.chat.id}:lockStickers:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "الملصقات"))

    if text == "قفل الفارسيه":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockPersian:{Dev_Zaid}"):
                return await message.reply_text(locknn.format(k, message.from_user.mention_html(), k, "الفارسيه"))
            else:
                r.set(f"{message.chat.id}:lockPersian:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "الفارسيه"))

    if text == "فتح الفارسيه":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockPersian:{Dev_Zaid}"):
                return await message.reply_text(Openn2.format(k, message.from_user.mention_html(), k, "الفارسيه"))
            else:
                r.delete(f"{message.chat.id}:lockPersian:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "الفارسيه"))

    if text == "قفل الملفات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockFiles:{Dev_Zaid}"):
                return await message.reply_text(locknn.format(k, message.from_user.mention_html(), k, "الملفات"))
            else:
                r.set(f"{message.chat.id}:lockFiles:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "الملفات"))

    if text == "فتح الملفات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockFiles:{Dev_Zaid}"):
                return await message.reply_text(Openn2.format(k, message.from_user.mention_html(), k, "الملفات"))
            else:
                r.delete(f"{message.chat.id}:lockFiles:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "الملفات"))

    if text == "قفل المتحركات" or text == "قفل المتحركه":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockAnimations:{Dev_Zaid}"):
                return await message.reply_text(locknn.format(k, message.from_user.mention_html(), k, "المتحركات"))
            else:
                r.set(f"{message.chat.id}:lockAnimations:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "المتحركات"))

    if text == "فتح المتحركات" or text == "فتح المتحركه":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockAnimations:{Dev_Zaid}"):
                return await message.reply_text(Openn2.format(k, message.from_user.mention_html(), k, "المتحركات"))
            else:
                r.delete(f"{message.chat.id}:lockAnimations:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "المتحركات"))

    if text == "قفل الروابط":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockUrls:{Dev_Zaid}"):
                return await message.reply_text(locknn.format(k, message.from_user.mention_html(), k, "الروابط"))
            else:
                r.set(f"{message.chat.id}:lockUrls:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "الروابط"))

    if text == "فتح الروابط":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockUrls:{Dev_Zaid}"):
                return await message.reply_text(Openn2.format(k, message.from_user.mention_html(), k, "الروابط"))
            else:
                r.delete(f"{message.chat.id}:lockUrls:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "الروابط"))

    if text == "قفل الهشتاق" or text == "قفل الهاشتاق":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockHashtags:{Dev_Zaid}"):
                return await message.reply_text(lockn.format(k, message.from_user.mention_html(), k, "الهاشتاق"))
            else:
                r.set(f"{message.chat.id}:lockHashtags:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "الهاشتاق"))

    if text == "فتح الهشتاق" or text == "فتح الهاشتاق":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockHashtags:{Dev_Zaid}"):
                return await message.reply_text(Openn.format(k, message.from_user.mention_html(), k, "الهاشتاق"))
            else:
                r.delete(f"{message.chat.id}:lockHashtags:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "الهاشتاق"))

    if text == "قفل البوتات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockBots:{Dev_Zaid}"):
                return await message.reply_text(locknn.format(k, message.from_user.mention_html(), k, "البوتات"))
            else:
                r.set(f"{message.chat.id}:lockBots:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "البوتات"))

    if text == "فتح البوتات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockBots:{Dev_Zaid}"):
                return await message.reply_text(Openn2.format(k, message.from_user.mention_html(), k, "البوتات"))
            else:
                r.delete(f"{message.chat.id}:lockBots:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "البوتات"))

    if text == "قفل اليوزرات" or text == "قفل المنشن":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockTags:{Dev_Zaid}"):
                return await message.reply_text(locknn.format(k, message.from_user.mention_html(), k, "اليوزرات"))
            else:
                r.set(f"{message.chat.id}:lockTags:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "اليوزرات"))

    if text == "فتح اليوزرات" or text == "فتح المنشن":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockTags:{Dev_Zaid}"):
                return await message.reply_text(Openn2.format(k, message.from_user.mention_html(), k, "اليوزرات"))
            else:
                r.delete(f"{message.chat.id}:lockTags:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "اليوزرات"))

    """
   if text == 'قفل الكفر' or text == 'قفل الشيعه' or text == 'قفل الشيعة':
     if not admin_pls(actor_id,message.chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if r.get(f'{message.chat.id}:lockKFR:{Dev_Zaid}'):
         return await message.reply_text(locknn.format(k,message.from_user.mention_html(),k,'الكفر'))
       else:
         r.set(f'{message.chat.id}:lockKFR:{Dev_Zaid}',1)
         return await message.reply_text(lock.format(k,message.from_user.mention_html(),k,'الكفر'))

   if text == 'فتح الكفر' or text == 'فتح الشيعه' or text == 'فتح الشيعة':
     if not admin_pls(actor_id,message.chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.get(f'{message.chat.id}:lockKFR:{Dev_Zaid}'):
         return await message.reply_text(Openn2.format(k,message.from_user.mention_html(),k,'الكفر'))
       else:
         r.delete(f'{message.chat.id}:lockKFR:{Dev_Zaid}')
         return await message.reply_text(Open.format(k,message.from_user.mention_html(),k,'الكفر'))
   """

    if text == "قفل الإباحي" or text == "قفل الاباحي":
        if not owner_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المالك وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockNSFW:{Dev_Zaid}"):
                return await message.reply_text(lockn.format(k, message.from_user.mention_html(), k, "الإباحي"))
            else:
                r.set(f"{message.chat.id}:lockNSFW:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "الإباحي"))

    if text == "فتح الإباحي" or text == "فتح الاباحي":
        if not owner_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المالك وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockNSFW:{Dev_Zaid}"):
                return await message.reply_text(Openn.format(k, message.from_user.mention_html(), k, "االإباحي"))
            else:
                r.delete(f"{message.chat.id}:lockNSFW:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "الإباحي"))

    if text == "قفل الكلام الكثير" or text == "قفل الكلايش":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockMessages:{Dev_Zaid}"):
                return await message.reply_text(lockn.format(k, message.from_user.mention_html(), k, "الكلام الكثير"))
            else:
                r.set(f"{message.chat.id}:lockMessages:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "الكلام الكثير"))

    if text == "فتح الكلام الكثير" or text == "فتح الكلايش":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockMessages:{Dev_Zaid}"):
                return await message.reply_text(Openn.format(k, message.from_user.mention_html(), k, "الكلام الكثير"))
            else:
                r.delete(f"{message.chat.id}:lockMessages:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "الكلام الكثير"))

    if text == "قفل التكرار":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockSpam:{Dev_Zaid}"):
                return await message.reply_text(lockn.format(k, message.from_user.mention_html(), k, "التكرار"))
            else:
                r.set(f"{message.chat.id}:lockSpam:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "التكرار"))

    if text == "فتح التكرار":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockSpam:{Dev_Zaid}"):
                return await message.reply_text(Openn.format(k, message.from_user.mention_html(), k, "التكرار"))
            else:
                r.delete(f"{message.chat.id}:lockSpam:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "التكرار"))

    if text == "قفل التوجيه":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockForward:{Dev_Zaid}"):
                return await message.reply_text(lockn.format(k, message.from_user.mention_html(), k, "التوجيه"))
            else:
                r.set(f"{message.chat.id}:lockForward:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "التوجيه"))

    if text == "فتح التوجيه":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockForward:{Dev_Zaid}"):
                return await message.reply_text(Openn.format(k, message.from_user.mention_html(), k, "التوجيه"))
            else:
                r.delete(f"{message.chat.id}:lockForward:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "التوجيه"))

    if text == "قفل الانلاين":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockInline:{Dev_Zaid}"):
                return await message.reply_text(lockn.format(k, message.from_user.mention_html(), k, "الانلاين"))
            else:
                r.set(f"{message.chat.id}:lockInline:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "الانلاين"))

    if text == "فتح الانلاين":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockInline:{Dev_Zaid}"):
                return await message.reply_text(Openn.format(k, message.from_user.mention_html(), k, "الانلاين"))
            else:
                r.delete(f"{message.chat.id}:lockInline:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "الانلاين"))

    if text == "قفل السب":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockSHTM:{Dev_Zaid}"):
                return await message.reply_text(lockn.format(k, message.from_user.mention_html(), k, "السب"))
            else:
                r.set(f"{message.chat.id}:lockSHTM:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "السب"))

    if text == "فتح السب":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockSHTM:{Dev_Zaid}"):
                return await message.reply_text(Openn.format(k, message.from_user.mention_html(), k, "السب"))
            else:
                r.delete(f"{message.chat.id}:lockSHTM:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "السب"))

    if text == "قفل الاضافه" or text == "قفل الاضافة" or text == "قفل الجهات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockaddContacts:{Dev_Zaid}"):
                return await message.reply_text(locknn.format(k, message.from_user.mention_html(), k, "الاضافه"))
            else:
                r.set(f"{message.chat.id}:lockaddContacts:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "الاضافه"))

    if text == "فتح الاضافه" or text == "فتح الاضافة" or text == "فتح الجهات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockaddContacts:{Dev_Zaid}"):
                return await message.reply_text(Openn2.format(k, message.from_user.mention_html(), k, "الاضافه"))
            else:
                r.delete(f"{message.chat.id}:lockaddContacts:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "الاضافه"))

    if text == "قفل دخول البوتات" or text == "قفل الوهمي" or text == "قفل الايراني":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockJoinPersian:{Dev_Zaid}"):
                return await message.reply_text(locknn.format(k, message.from_user.mention_html(), k, "دخول البوتات"))
            else:
                r.set(f"{message.chat.id}:lockJoinPersian:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "دخول البوتات"))

    if text == "فتح دخول البوتات" or text == "فتح الوهمي" or text == "فتح الايراني":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockJoinPersian:{Dev_Zaid}"):
                return await message.reply_text(Openn2.format(k, message.from_user.mention_html(), k, "دخول البوتات"))
            else:
                r.delete(f"{message.chat.id}:lockJoinPersian:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "دخول البوتات"))

    if text == "قفل الصوت":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockAudios:{Dev_Zaid}"):
                return await message.reply_text(lockn.format(k, message.from_user.mention_html(), k, "الصوت"))
            else:
                r.set(f"{message.chat.id}:lockAudios:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "الصوت"))

    if text == "فتح الصوت":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockAudios:{Dev_Zaid}"):
                return await message.reply_text(Openn.format(k, message.from_user.mention_html(), k, "الصوت"))
            else:
                r.delete(f"{message.chat.id}:lockAudios:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "الصوت"))

    if text == "قفل القنوات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockChannels:{Dev_Zaid}"):
                return await message.reply_text(locknn.format(k, message.from_user.mention_html(), k, "القنوات"))
            else:
                r.set(f"{message.chat.id}:lockChannels:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "القنوات"))

    if text == "فتح القنوات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockChannels:{Dev_Zaid}"):
                return await message.reply_text(Openn2.format(k, message.from_user.mention_html(), k, "القنوات"))
            else:
                r.delete(f"{message.chat.id}:lockChannels:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "القنوات"))

    if text == "قفل الدخول":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:lockJoin:{Dev_Zaid}"):
                return await message.reply_text(lockn.format(k, message.from_user.mention_html(), k, "الدخول"))
            else:
                r.set(f"{message.chat.id}:lockJoin:{Dev_Zaid}", 1)
                return await message.reply_text(lock.format(k, message.from_user.mention_html(), k, "الدخول"))

    if text == "فتح الدخول":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:lockJoin:{Dev_Zaid}"):
                return await message.reply_text(Openn.format(k, message.from_user.mention_html(), k, "الدخول"))
            else:
                r.delete(f"{message.chat.id}:lockJoin:{Dev_Zaid}")
                return await message.reply_text(Open.format(k, message.from_user.mention_html(), k, "الدخول"))

    if text == "تعطيل التحذير":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} التحذير معطل من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:disableWarn:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت التحذير\n☆"
                )

    if text == "تفعيل التحذير":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:disableWarn:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} التحذير مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:disableWarn:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت التحذير\n☆"
                )

    if text == "تعطيل اليوتيوب":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:disableYT:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} اليوتيوب معطل من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:disableYT:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت اليوتيوب\n☆"
                )

    if text == "تفعيل اليوتيوب":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:disableYT:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} اليوتيوب مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:disableYT:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت اليوتيوب\n☆"
                )

    if text == "تعطيل الساوند":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:disableSound:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} الساوند معطل من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:disableSound:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت الساوند\n☆"
                )

    if text == "تفعيل الساوند":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:disableSound:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} الساوند مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:disableSound:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت الساوند\n☆"
                )

    if text == "تعطيل الانستا":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:disableINSTA:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} الانستا معطل من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:disableINSTA:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت الانستا\n☆"
                )

    if text == "تفعيل الانستا":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:disableINSTA:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} الانستا مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:disableINSTA:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت الانستا\n☆"
                )

    if text == "تعطيل اهمس":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:disableWHISPER:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} اهمس معطل من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:disableWHISPER:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت اهمس\n☆"
                )

    if text == "تفعيل اهمس":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:disableWHISPER:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} اهمس مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:disableWHISPER:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت اهمس\n☆"
                )

    if text == "تعطيل التيك":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:disableTik:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} التيك معطل من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:disableTik:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت التيك\n☆"
                )

    if text == "تفعيل التيك":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:disableTik:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} التيك مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:disableTik:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت التيك\n☆"
                )

    if text == "تعطيل شازام":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:disableShazam:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} شازام معطل من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:disableShazam:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت شازام\n☆"
                )

    if text == "تفعيل شازام":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:disableShazam:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} شازام مفعل من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:disableShazam:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت شازام\n☆"
                )

    if text == "تعطيل الالعاب":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:disableGames:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} الالعاب معطله من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:disableGames:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت الالعاب\n☆"
                )

    if text == "تفعيل الالعاب":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:disableGames:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} الالعاب مفعله من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:disableGames:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت الالعاب\n☆"
                )

    if text == "تعطيل الترجمة" or text == "تعطيل الترجمه":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:disableTrans:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} الترجمه معطله من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:disableTrans:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت الترجمه\n☆"
                )

    if text == "تفعيل الترجمة" or text == "تفعيل الترجمه":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:disableTrans:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} الترجمه مفعله من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:disableTrans:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت الترجمه\n☆"
                )

    if text == "تعطيل التسلية" or text == "تعطيل التسليه":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if r.get(f"{message.chat.id}:disableFun:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} التسلية معطله من قبل\n☆"
                )
            else:
                r.set(f"{message.chat.id}:disableFun:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت التسلية\n☆"
                )

    if text == "تفعيل التسلية" or text == "تفعيل التسليه":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
        else:
            if not r.get(f"{message.chat.id}:disableFun:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} التسلية مفعله من قبل\n☆"
                )
            else:
                r.delete(f"{message.chat.id}:disableFun:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت التسلية\n☆"
                )

    if text == "تعطيل الاشتراك":
        if not dev2_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المطور وفوق ) بس")
        else:
            if r.get(f"disableSubscribe:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} الاشتراك الاجباري معطل من قبل\n☆"
                )
            else:
                r.set(f"disableSubscribe:{Dev_Zaid}", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت الاشتراك الاجباري\n☆"
                )

    if text == "قناة الاشتراك":
        if not dev2_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المطور وفوق ) بس")
        ch = r.get(f"forceChannel:{Dev_Zaid}") or "مافي قناة"
        return await message.reply_text(f"{k} قناة الاشتراك هي ( {ch} )")

    if text.startswith("وضع قناة @"):
        if not dev2_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المطور وفوق ) بس")
        username = text.split("@")[1]
        try:
            chat = context.bot.get_chat(username)
        except:
            return await message.reply_text(f"{k} حدث خطأ")
        r.set(f"forceChannel:{Dev_Zaid}", "@" + username)
        return await message.reply_text(f"{k} تم تعيين القناة بنجاح")

    if text == "تفعيل الاشتراك":
        if not dev2_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الامر يخص ( المطور وفوق ) بس")
        else:
            if not r.get(f"disableSubscribe:{Dev_Zaid}"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} الاشتراك الاجباري مفعل من قبل\n☆"
                )
            else:
                r.delete(f"disableSubscribe:{Dev_Zaid}")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت الاشتراك الاجباري\n☆"
                )

    if (
        text == "/ar"
        and message.reply_to_message
        and (message.reply_to_message.text or message.reply_to_message.caption)
    ):
        if not r.get(f"{message.chat.id}:disableTrans:{Dev_Zaid}"):
            text = message.reply_to_message.text or message.reply_to_message.caption
            translation = requests.get(
                f"https://hozory.com/translate/?target=ar&text={text}"
            ).json()["result"]["translate"]
            await message.reply_text(f"`{translation}`")

    if (
        text == "/en"
        and message.reply_to_message
        and (message.reply_to_message.text or message.reply_to_message.caption)
    ):
        if not r.get(f"{message.chat.id}:disableTrans:{Dev_Zaid}"):
            text = message.reply_to_message.text or message.reply_to_message.caption
            translation = requests.get(
                f"https://hozory.com/translate/?target=en&text={text}"
            ).json()["result"]["translate"]
            await message.reply_text(f"`{translation}`")

    if (
        text == "ترجمه"
        and message.reply_to_message
        and (message.reply_to_message.text or message.reply_to_message.caption)
    ):
        if not r.get(f"{message.chat.id}:disableTrans:{Dev_Zaid}"):
            text = message.reply_to_message.text or message.reply_to_message.caption
            en = requests.get(
                f"https://hozory.com/translate/?target=en&text={text}"
            ).json()["result"]["translate"]
            ar = requests.get(
                f"https://hozory.com/translate/?target=ar&text={text}"
            ).json()["result"]["translate"]
            ru = requests.get(
                f"https://hozory.com/translate/?target=ru&text={text}"
            ).json()["result"]["translate"]
            zh = requests.get(
                f"https://hozory.com/translate/?target=zh&text={text}"
            ).json()["result"]["translate"]
            fr = requests.get(
                f"https://hozory.com/translate/?target=fr&text={text}"
            ).json()["result"]["translate"]
            du = requests.get(
                f"https://hozory.com/translate/?target=nl&text={text}"
            ).json()["result"]["translate"]
            tr = requests.get(
                f"https://hozory.com/translate/?target=tr&text={text}"
            ).json()["result"]["translate"]
            txt = f"🇷🇺 : \n {ru}\n\n🇨🇳 : \n {zh}\n\n🇫🇷 :\n {fr}\n\n🇩🇪 :\n {du}\n\n🇹🇷 : \n{tr}"
            return await message.reply_text(txt)

    if (
        text.startswith("ترجمه ")
        and message.reply_to_message
        and (message.reply_to_message.text or message.reply_to_message.caption)
    ):
        if not r.get(f"{message.chat.id}:disableTrans:{Dev_Zaid}"):
            lang = text.split()[1]
            text = message.reply_to_message.text or message.reply_to_message.caption
            translation = requests.get(
                f"https://hozory.com/translate/?target={lang}&text={text}"
            ).json()["result"]["translate"]
            await message.reply_text(f"`{translation}`")

    if text == "ابلاغ" and message.reply_to_message:
        text = f"{k} تم ابلاغ المشرفين"
        cc = 0
        for mm in await context.bot.get_chat_administrators(chat.id):
            if not mm.user.is_deleted and not mm.user.is_bot:
                cc += 1
                text += f"[⁪⁬⁪⁬⁮⁪⁬⁪⁬⁮](tg://user?id={mm.user.id})"
        if cc == 0:
            return False
        return await message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⚠️", callback_data="delAdminMSG")]]
            ),
        )

    if text == "المقيدين":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            co = 0
            cc = 1
            text = "المقيدين:\n\n"
            for mm in []:
                if co == 100:
                    break
                if not mm.user.is_deleted:
                    co += 1
                    user = (
                        f"@{mm.user.username}"
                        if mm.user.username
                        else f"[@{channel}](tg://user?id={mm.user.id})"
                    )
                    text += f"{cc} ➣ {user} ☆ ( `{mm.user.id}` )\n"
                    cc += 1
            text += "☆"
            if co == 0:
                return await message.reply_text(f"{k} مافيه مقيديين")
            else:
                return await message.reply_text(text)

    if text == "مسح المقيدين":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            co = 0
            for mm in []:
                co += 1
                await context.bot.restrict_chat_member(
                    message.chat.id,
                    mm.user.id,
                    ChatPermissions(
                        can_send_messages=True,
                    can_send_audios=True,
                    can_send_documents=True,
                    can_send_photos=True,
                    can_send_videos=True,
                    can_send_video_notes=True,
                    can_send_voice_notes=True,
                        can_send_other_messages=True,
                        can_send_polls=True,
                        can_invite_users=True,
                        can_add_web_page_previews=True,
                        can_change_info=True,
                        can_pin_messages=True,
                    ),
                )
            if co == 0:
                return await message.reply_text(f"{k} مافيه مقيديين")
            else:
                return await message.reply_text(f"{k} ابشر مسحت ( {co} ) من المقيدين")

    if text == "تثبيت" and message.reply_to_message:
        if mod_pls(actor_id, message.chat.id):
            await message.reply_to_message.pin(disable_notification=False)
            await message.reply_text(f"{k} ابشر ثبتت الرسالة ")

    if text == "الغاء التثبيت" and message.reply_to_message:
        if mod_pls(actor_id, message.chat.id):
            await message.reply_to_message.unpin()
            await message.reply_text(f"{k} ابشر لغيت تثبيت الرسالة ")

    if text.startswith("تقييد ") and len(text.split()) == 2:
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            try:
                user = int(text.split()[1])
            except:
                user = text.split()[1].replace("@", "")
            try:
                get = await context.bot.get_chat_member(message.chat.id, user)
                if actor_id == get.user.id:
                    return await message.reply_text("شفيك تبي تنزل نفسك")
                if pre_pls(get.user.id, message.chat.id):
                    rank = get_rank(get.user.id, message.chat.id)
                    return await message.reply_text(f"{k} هييه مايمديك تقييد {rank} ياورع!")
                if get.status == ChatMemberStatus.RESTRICTED:
                    return await message.reply_text(f"「 {get.user.mention_html()} 」 \n{k} مقيد من قبل\n☆")
            except:
                return await message.reply_text(f"{k} مافي عضو بهذا اليوزر")
            await context.bot.restrict_chat_member(
                message.chat.id, get.user.id, ChatPermissions(can_send_messages=False)
            )
            return await message.reply_text(f"「 {get.user.mention_html()} 」 \n{k} قييدته\n☆")

    if text == "تقييد" and message.reply_to_message and message.reply_to_message.from_user:
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            if actor_id == message.reply_to_message.from_user.id:
                return await message.reply_text("شفيك تبي تنزل نفسك")
            get = await context.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            if pre_pls(message.reply_to_message.from_user.id, message.chat.id):
                rank = get_rank(message.reply_to_message.from_user.id, message.chat.id)
                return await message.reply_text(f"{k} هييه مايمديك تقييد {rank} ياورع!")
            if get.status == ChatMemberStatus.RESTRICTED:
                return await message.reply_text(
                    f"「 {message.reply_to_message.from_user.mention_html()} 」 \n{k} مقيد من قبل\n☆"
                )
            await context.bot.restrict_chat_member(
                message.chat.id,
                message.reply_to_message.from_user.id,
                ChatPermissions(can_send_messages=False),
            )
            return await message.reply_text(
                f"「 {message.reply_to_message.from_user.mention_html()} 」 \n{k} قييدته\n☆"
            )

    if (
        text.startswith("الغاء تقييد ")
        or text.startswith("الغاء التقييد ")
        and len(text.split()) == 3
    ):
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( الادمن وفوق ) بس")
        else:
            try:
                user = int(text.split()[2])
            except:
                user = text.split()[2].replace("@", "")
            try:
                get = await context.bot.get_chat_member(message.chat.id, user)
                if not get.status == ChatMemberStatus.RESTRICTED:
                    return await message.reply_text(f"「 {get.user.mention_html()} 」 \n{k} مو مقيد من قبل\n☆")
            except:
                return await message.reply_text(f"{k} مافي عضو بهذا اليوزر")
            await context.bot.restrict_chat_member(
                message.chat.id,
                get.user.id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_polls=True,
                    can_invite_users=True,
                    can_change_info=True,
                    can_pin_messages=True,
                    can_send_audios=True,
                    can_send_documents=True,
                    can_send_photos=True,
                    can_send_videos=True,
                    can_send_video_notes=True,
                    can_send_voice_notes=True,
                ),
            )
            return await message.reply_text(f"「 {get.user.mention_html()} 」 \n{k} ابشر الغيت تقييده\n☆")

    if (
        text == "الغاء تقييد"
        or text == "الغاء التقييد"
        and message.reply_to_message
        and message.reply_to_message.from_user
    ):
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( الادمن وفوق ) بس")
        else:
            get = await context.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            if not get.status == ChatMemberStatus.RESTRICTED:
                return await message.reply_text(
                    f"「 {message.reply_to_message.from_user.mention_html()} 」 \n{k} مو مقيد من قبل\n☆"
                )
            await context.bot.restrict_chat_member(
                message.chat.id,
                message.reply_to_message.from_user.id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_polls=True,
                    can_invite_users=True,
                    can_change_info=True,
                    can_pin_messages=True,
                    can_send_audios=True,
                    can_send_documents=True,
                    can_send_photos=True,
                    can_send_videos=True,
                    can_send_video_notes=True,
                    can_send_voice_notes=True,
                ),
            )
            return await message.reply_text(
                f"「 {message.reply_to_message.from_user.mention_html()} 」 \n{k} ابشر الغيت تقييده\n☆"
            )

    if text == "المحظورين":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            co = 0
            cc = 1
            text = "المحظورين:\n\n"
            for mm in []:
                if co == 100:
                    break
                if mm.user:
                    if not mm.user.is_deleted:
                        co += 1
                        user = (
                            f"@{mm.user.username}"
                            if mm.user.username
                            else f"[@{channel}](tg://user?id={mm.user.id})"
                        )
                        text += f"{cc} ➣ {user} ☆ ( `{mm.user.id}` )\n"
                        cc += 1
                if mm.chat:
                    co += 1
                    user = f"@{mm.chat.username}"
                    text += f"{cc} ➣ {user} ☆ (`{mm.chat.id}`)\n"
                    cc += 1
            text += "☆"
            if co == 0:
                return await message.reply_text(f"{k} مافيه محظورين")
            else:
                return await message.reply_text(text)

    if text == "مسح المحظورين":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( الادمن وفوق ) بس")
        else:
            co = 0
            for mm in []:
                if mm.user:
                    co += 1
                    await context.bot.unban_chat_member(message.chat.id, mm.user.id)
                if mm.chat:
                    co += 1
                    await context.bot.unban_chat_member(message.chat.id, mm.chat.id)
            if co == 0:
                return await message.reply_text(f"{k} مافيه محظورين")
            else:
                return await message.reply_text(f"{k} ابشر مسحت ( {co} ) من المحظورين")

    if text.startswith("حظر ") and len(text.split()) == 2:
        if not "@" in text and not re.findall("[0-9]+", text):
            return
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            try:
                user = int(text.split()[1])
            except:
                user = text.split()[1].replace("@", "")
            try:
                get = await context.bot.get_chat_member(message.chat.id, user)
                if actor_id == get.user.id:
                    return await message.reply_text("شفيك تبي تنزل نفسك")
                if pre_pls(get.user.id, message.chat.id):
                    rank = get_rank(get.user.id, message.chat.id)
                    return await message.reply_text(f"{k} هييه مايمديك تحظر {rank} ياورع!")
                if get.status == ChatMemberStatus.BANNED:
                    return await message.reply_text(f"「 {get.user.mention_html()} 」 \n{k} محظور من قبل\n☆")
            except:
                return await message.reply_text(f"{k} مافي عضو بهذا اليوزر")
            await context.bot.ban_chat_member(chat.id, get.user.id)
            return await message.reply_text(f"「 {get.user.mention_html()} 」 \n{k} حظرته\n☆")

    if text == "حظر" and message.reply_to_message and message.reply_to_message.from_user:
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            if actor_id == message.reply_to_message.from_user.id:
                return await message.reply_text("شفيك تبي تنزل نفسك")
            get = await context.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            if pre_pls(message.reply_to_message.from_user.id, message.chat.id):
                rank = get_rank(message.reply_to_message.from_user.id, message.chat.id)
                return await message.reply_text(f"{k} هييه مايمديك تحظر {rank} ياورع!")
            if get.status == ChatMemberStatus.BANNED:
                return await message.reply_text(
                    f"「 {message.reply_to_message.from_user.mention_html()} 」 \n{k} محظور من قبل\n☆"
                )
            await context.bot.ban_chat_member(chat.id, message.reply_to_message.from_user.id)
            return await message.reply_text(
                f"「 {message.reply_to_message.from_user.mention_html()} 」 \n{k} حظرته\n☆"
            )

    if text == "طرد البوتات":
        if not owner_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المالك وفوق ) بس")
        else:
            co = 0
            for mm in []:
                try:
                    await context.bot.ban_chat_member(chat.id, mm.user.id)
                    co += 1
                except:
                    pass
            if co == 0:
                return await message.reply_text(f"{k} مافيه بوتات")
            else:
                return await message.reply_text(f"{k} ابشر حظر ( {co} ) بوت")

    if text.startswith("طرد ") and len(text.split()) == 2:
        if not "@" in text and not re.findall("[0-9]+", text):
            return
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( الادمن وفوق ) بس")
        else:
            try:
                user = int(text.split()[1])
            except:
                user = text.split()[1].replace("@", "")
            try:
                get = await context.bot.get_chat_member(message.chat.id, user)
                if actor_id == get.user.id:
                    return await message.reply_text("شفيك تبي تنزل نفسك")
                if pre_pls(get.user.id, message.chat.id):
                    rank = get_rank(get.user.id, message.chat.id)
                    return await message.reply_text(f"{k} هييه مايمديك تطرد {rank} ياورع!")
                if get.status == ChatMemberStatus.BANNED:
                    return await message.reply_text(f"「 {get.user.mention_html()} 」 \n{k} مطرود من قبل\n☆")
            except:
                return await message.reply_text(f"{k} مافي عضو بهذا اليوزر")
            await context.bot.ban_chat_member(chat.id, get.user.id)
            await context.bot.unban_chat_member(chat.id, get.user.id)
            return await message.reply_text(f"「 {get.user.mention_html()} 」 \n{k} طردته\n☆")

    if text == "اهمس" and message.reply_to_message and message.reply_to_message.from_user:
        if r.get(f"{message.chat.id}:disableWHISPER:{Dev_Zaid}"):
            return await message.reply_text(f"{k} امر اهمس معطل")
        user_id = message.reply_to_message.from_user.id
        if user_id == actor_id:
            return await message.reply_text(f"{k} مافيك تهمس لنفسك ياغبي")
        else:
            import uuid

            id = str(uuid.uuid4())[:6]
            a = await message.reply_text(
                f"{k} تم تحديد الهمسة الى [ {message.reply_to_message.from_user.mention_html()} ]",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                f"اهمس الى [ {message.reply_to_message.from_user.first_name[:25]} ]",
                                url=f"https://t.me/{context.bot.username}?start=hmsa{id}",
                            )
                        ]
                    ]
                ),
            )
            data = {
                "from": actor_id,
                "to": user_id,
                "chat": message.chat.id,
                "id": a.message_id,
            }
            # wsdb.set(str(id), data)
            wsdb.setex(key=id, ttl=3600, value=data)
            return True

    if text == "تعطيل التنظيف":
        if not gowner_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المالك الاساسي وفوق ) بس")
        else:
            if not r.hget(Dev_Zaid + str(message.chat.id), "ena-clean"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} التنظيف معطل من قبل\n☆"
                )
            else:
                r.hdel(Dev_Zaid + str(message.chat.id), "ena-clean")
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر عطلت التنظيف\n☆"
                )

    if text == "تفعيل التنظيف":
        if not gowner_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المالك الاساسي وفوق ) بس")
        else:
            if r.hget(Dev_Zaid + str(message.chat.id), "ena-clean"):
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} التنظيف مفعل من قبل\n☆"
                )
            else:
                r.hset(Dev_Zaid + str(message.chat.id), "ena-clean", 1)
                return await message.reply_text(
                    f"{k} من「 {message.from_user.mention_html()} 」\n{k} ابشر فعلت التنظيف\n☆"
                )

    if re.search("^وضع وقت التنظيف [0-9]+$", text):
        if not gowner_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المالك الاساسي وفوق ) بس")
        else:
            secs = int(text.split()[3])
            if secs > 3600 or secs < 60:
                return await message.reply_text(
                    f"{k} عليك تحديد وقت التنظيف بالثواني من 60 الى 3600 ثانية"
                )
            else:
                r.hset(Dev_Zaid + str(message.chat.id), "clean-secs", secs)
                return await message.reply_text(f"{k} تم تعيين وقت التنظيف ( {secs} ) ثانية")

    if text == "وقت التنظيف":
        if not gowner_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المالك الاساسي وفوق ) بس")
        else:
            secs = r.hget(Dev_Zaid + str(message.chat.id), "clean-secs") or "60"
            return await message.reply_text(f"`{secs}`")

    if text == "طرد" and message.reply_to_message and message.reply_to_message.from_user:
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            try:
                if actor_id == message.reply_to_message.from_user.id:
                    return await message.reply_text("شفيك تبي تنزل نفسك")
                get = await context.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                if pre_pls(message.reply_to_message.from_user.id, message.chat.id):
                    rank = get_rank(message.reply_to_message.from_user.id, message.chat.id)
                    return await message.reply_text(f"{k} هييه مايمديك تطرد {rank} ياورع!")
                if get.status == ChatMemberStatus.BANNED:
                    return await message.reply_text(
                        f"「 {message.reply_to_message.from_user.mention_html()} 」 \n{k} مطرود من قبل\n☆"
                    )
                await context.bot.ban_chat_member(chat.id, message.reply_to_message.from_user.id)
                await message.reply_text(f"「 {message.reply_to_message.from_user.mention_html()} 」 \n{k} طردته\n☆")
                return await context.bot.unban_chat_member(chat.id, message.reply_to_message.from_user.id)
            except:
                return await message.reply_text(f"{k} العضو مو بالمجموعة")

    if (
        text.startswith("رفع الحظر ")
        or text.startswith("الغاء الحظر ")
        and len(text.split()) == 3
    ):
        if not "@" in text and not re.findall("[0-9]+", text):
            return
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            try:
                user = int(text.split()[2])
            except:
                user = text.split()[2].replace("@", "")
            try:
                get = await context.bot.get_chat_member(message.chat.id, user)
                if not get.status == ChatMemberStatus.BANNED:
                    return await message.reply_text(f"「 {get.user.mention_html()} 」 \n{k} مو محظور من قبل\n☆")
            except:
                return await message.reply_text(f"{k} مافي عضو بهذا اليوزر")
            await context.bot.unban_chat_member(chat.id, get.user.id)
            return await message.reply_text(f"「 {get.user.mention_html()} 」 \n{k} ابشر الغيت حظره\n☆")

    if (
        text == "رفع الحظر"
        or text == "الغاء الحظر"
        and message.reply_to_message
        and message.reply_to_message.from_user
    ):
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            try:
                get = await context.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                if not get.status == ChatMemberStatus.BANNED:
                    return await message.reply_text(
                        f"「 {message.reply_to_message.from_user.mention_html()} 」 \n{k} مو محظور من قبل\n☆"
                    )
                await context.bot.unban_chat_member(chat.id, message.reply_to_message.from_user.id)
                return await message.reply_text(
                    f"「 {message.reply_to_message.from_user.mention_html()} 」 \n{k} ابشر الغيت حظره\n☆"
                )
            except:
                return await message.reply_text(f"{k} العضو مو بالمجموعة")

    if text.startswith("رفع القيود ") and len(text.split()) == 3:
        if not "@" in text and not re.findall("[0-9]+", text):
            return
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            try:
                user = int(text.split()[2])
            except:
                user = text.split()[2].replace("@", "")
            co = 0
            text = ""
            try:
                get = await context.bot.get_chat_member(message.chat.id, user)
                if get.status == ChatMemberStatus.BANNED:
                    await context.bot.unban_chat_member(chat.id, get.user.id)
                    text += "حظر\n"
                    co += 1
                if get.status == ChatMemberStatus.RESTRICTED:
                    await context.bot.restrict_chat_member(
                        message.chat.id,
                        get.user.id,
                        ChatPermissions(
                            can_send_messages=True,
                    can_send_audios=True,
                    can_send_documents=True,
                    can_send_photos=True,
                    can_send_videos=True,
                    can_send_video_notes=True,
                    can_send_voice_notes=True,
                            can_send_other_messages=True,
                            can_send_polls=True,
                            can_invite_users=True,
                            can_add_web_page_previews=True,
                            can_change_info=True,
                            can_pin_messages=True,
                        ),
                    )
                    text += "تقييد\n"
                    co += 1
                if r.get(f"{get.user.id}:mute:{message.chat.id}{Dev_Zaid}"):
                    r.delete(f"{get.user.id}:mute:{message.chat.id}{Dev_Zaid}")
                    r.srem(f"{message.chat.id}:listMUTE:{Dev_Zaid}", get.user.id)
                    text += "كتم\n"
                    co += 1
                if co > 0:
                    return await message.reply_text(f"رفعت القيود التالية:\n{text}\n☆")
                else:
                    return await message.reply_text(f"「 {get.user.mention_html()} 」\n{k} ماله قيود من قبل\n☆")

            except:
                return await message.reply_text(f"{k} مافي عضو بهذا اليوزر")
            await context.bot.unban_chat_member(chat.id, get.user.id)
            return await message.reply_text(f"「 {get.user.mention_html()} 」 \n{k} ابشر الغيت حظره\n☆")

    if text == "رفع القيود" and message.reply_to_message and message.reply_to_message.from_user:
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            try:
                text = ""
                co = 0
                get = await context.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
                if get.status == ChatMemberStatus.BANNED:
                    await context.bot.unban_chat_member(chat.id, get.user.id)
                    text += "حظر\n"
                    co += 1
                if get.status == ChatMemberStatus.RESTRICTED:
                    await context.bot.restrict_chat_member(
                        message.chat.id,
                        get.user.id,
                        ChatPermissions(
                            can_send_messages=True,
                    can_send_audios=True,
                    can_send_documents=True,
                    can_send_photos=True,
                    can_send_videos=True,
                    can_send_video_notes=True,
                    can_send_voice_notes=True,
                            can_send_other_messages=True,
                            can_send_polls=True,
                            can_invite_users=True,
                            can_add_web_page_previews=True,
                            can_change_info=True,
                            can_pin_messages=True,
                        ),
                    )
                    text += "تقييد\n"
                    co += 1
                if r.get(f"{get.user.id}:mute:{message.chat.id}{Dev_Zaid}"):
                    r.delete(f"{get.user.id}:mute:{message.chat.id}{Dev_Zaid}")
                    r.srem(f"{message.chat.id}:listMUTE:{Dev_Zaid}", get.user.id)
                    text += "كتم\n"
                    co += 1
                if co > 0:
                    return await message.reply_text(f"رفعت القيود التالية:\n{text}\n☆")
                else:
                    return await message.reply_text(f"「 {get.user.mention_html()} 」\n{k} ماله قيود من قبل\n☆")
            except:
                return await message.reply_text(f"{k} العضو مو بالمجموعة")

    if text == "كشف البوتات":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            co = 0
            text = "بوتات المجموعة:\n\n"
            cc = 1
            for mm in []:
                if co == 100:
                    break
                text += f"{cc}) {mm.user.mention_html()}"
                if mm.status == ChatMemberStatus.ADMINISTRATOR:
                    text += "👑"
                text += "\n"
                cc += 1
                co += 1
            text += "☆"
            if co == 0:
                return await message.reply_text(f"{k} مافيه بوتات")
            else:
                return await message.reply_text(text)

    if text == "مين ضافني":
        get = await context.bot.get_chat_member(message.chat.id, actor_id).invited_by
        if not get:
            return await message.reply_text(f"{k} محد ضافك")
        else:
            return await message.reply_text(get.user.mention_html())

    if text == "بايو عشوائي":
        return await message.reply_text(f"{k} تحت الصيانة")

    if text == "مسح" and message.reply_to_message:
        if admin_pls(actor_id, message.chat.id):
            await message.reply_to_message.delete()
            await message.delete()
        else:
            await message.delete()

    if (
        text.startswith("مسح ")
        and len(text.split()) == 2
        and re.findall("[0-9]+", text)
    ):
        count = int(re.findall("[0-9]+", text)[0])
        if not admin_pls(actor_id, message.chat.id):
            return await message.delete()
        else:
            if count > 400:
                return await message.reply_text(f"{k} اختار من 1 الى 400")
            else:
                for msg in range(message.message_id, message.message_id - count, -1):
                    try:
                        await context.bot.delete_message(message.chat.id, msg)
                    except:
                        pass

    if text == "تنزيل مشرف" and message.reply_to_message and message.reply_to_message.from_user:
        if not owner_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المالك وفوق ) بس")
        else:
            try:
                await context.bot.promote_chat_member(
                    message.chat.id,
                    message.reply_to_message.from_user.id,
                    can_manage_chat=False,
                    can_delete_messages=False,
                    can_manage_video_chats=False,
                    can_restrict_members=False,
                    can_promote_members=False,
                    can_pin_messages=False,
                    can_change_info=False,
                    can_invite_users=False,
                )
                return await message.reply_text(
                    f"「 {message.reply_to_message.from_user.mention_html()} 」\n{k} نزلته من الاشراف"
                )
            except:
                return await message.reply_text(
                    f"「 {message.reply_to_message.from_user.mention_html()} 」\n{k} مو انا الي رفعته او ماعندي صلاحيات"
                )

    if text == "رفع مشرف" and message.reply_to_message and message.reply_to_message.from_user:
        if not owner_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المالك وفوق ) بس")
        else:
            get = await context.bot.get_chat_member(message.chat.id, context.bot.id)
            if (
                not getattr(get, "can_manage_chat", False)
                or not getattr(get, "can_delete_messages", False)
                or not getattr(get, "can_restrict_members", False)
                or not getattr(get, "can_pin_messages", False)
                or not getattr(get, "can_invite_users", False)
                or not getattr(get, "can_change_info", False)
                or not getattr(get, "can_promote_members", False)
            ):
                return await message.reply_text("هات كل الصلاحيات بعدين سولف")
            else:
                r.set(
                    f"{actor_id}:promote:{message.chat.id}",
                    message.reply_to_message.from_user.id,
                    ex=600,
                )
                return await message.reply_text(
                    """
⇜ تمام الحين ارسل صلاحيات المشرف

* ⇠ لرفع كل الصلاحيات ما عدا رفع المشرفين
** ⇠ لرفع كل الصلاحيات مع رفع المشرفين

⇜ يمديك تختار الصلاحيات وتعيين لقب للمشرف في سطر واحد

مثال: ** الهطف
☆""",
                    reply_markup=ForceReply(selective=True),
                    parse_mode=ParseMode.HTML,
                )

    if r.get(f"{actor_id}:promote:{message.chat.id}") and owner_pls(
        actor_id, message.chat.id
    ):
        id = int(r.get(f"{actor_id}:promote:{message.chat.id}") or 0)
        if text.startswith("*"):
            r.delete(f"{actor_id}:promote:{message.chat.id}")
            if text.startswith("**"):
                can_promote_members = True
                type = 1
            else:
                can_promote_members = False
                type = 0
            if len(text.split()) > 1:
                title = text.split(None, 1)[1][:15:]
            else:
                title = None
            await context.bot.promote_chat_member(
                message.chat.id,
                id,
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_promote_members=can_promote_members,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
            )
            if title:
                try:
                    await context.bot.set_chat_administrator_custom_title(message.chat.id, id, title)
                except:
                    pass
            get = await context.bot.get_chat_member(message.chat.id, id)
            if type == 1:
                r.set(f"{message.chat.id}:rankADMIN:{get.user.id}{Dev_Zaid}", 1)
                r.sadd(f"{message.chat.id}:listADMIN:{Dev_Zaid}", get.user.id)
                return await message.reply_text(
                    f"الحلو 「 {get.user.mention_html()} 」\n{k} رفعته مشرف بكل صلاحيات "
                )
            else:
                r.set(f"{message.chat.id}:rankADMIN:{get.user.id}{Dev_Zaid}", 1)
                r.sadd(f"{message.chat.id}:listADMIN:{Dev_Zaid}", get.user.id)
                return await message.reply_text(
                    f"الحلو 「 {get.user.mention_html()} 」\n{k} رفعته مشرف بكل الصلاحيات عدا رفع المشرفين"
                )

    if text == "مسح قائمة التثبيت":
        if not mod_pls(actor_id, message.chat.id):
            return await message.reply_text(f"{k} هذا الأمر يخص ( المدير وفوق ) بس")
        else:
            context.bot.unpin_all_chat_messages(message.chat.id)
            return await message.reply_text(f"{k} ابشر مسحت قائمة التثبيت")

    if (
        text == "الاوامر"
        or text.lower() == "/commands"
        or text.lower() == f"/commands@{botUsername.lower()}"
    ):
        if admin_pls(actor_id, message.chat.id):
            channel = (
                r.get(f"{Dev_Zaid}:BotChannel")
                if r.get(f"{Dev_Zaid}:BotChannel")
                else "scatteredda"
            )
            return await message.reply_text(
                f"{k} اهلين فيك باوامر البوت\n\nللاستفسار - @{channel}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "م1", callback_data=f"commands1:{actor_id}"
                            ),
                            InlineKeyboardButton(
                                "م2", callback_data=f"commands2:{actor_id}"
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                "م3", callback_data=f"commands3:{actor_id}"
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                "الالعاب", callback_data=f"commands4:{actor_id}"
                            ),
                            InlineKeyboardButton(
                                "التسليه", callback_data=f"commands5:{actor_id}"
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                "اليوتيوب", callback_data=f"commands6:{actor_id}"
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                "البنك", callback_data=f"commands7:{actor_id}"
                            ),
                            InlineKeyboardButton(
                                "زواج", callback_data=f"commands8:{actor_id}"
                            ),
                        ],
                    ]
                ),
            )
        else:
            return await message.reply_text(f"{k} هذا الأمر يخص ( الادمن وفوق ) بس")

# Converted Pyrogram on_callback_query handler
async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update or not update.callback_query:
        return
    callback = update.callback_query
    channel = (
        r.get(f"{Dev_Zaid}:BotChannel") if r.get(f"{Dev_Zaid}:BotChannel") else "scatteredda"
    )
    try:
        await callback.answer()
    except Exception:
        pass
    await CallbackQueryResponse(callback, context, channel)

async def CallbackQueryResponse(update, context: ContextTypes.DEFAULT_TYPE, channel):
    if not update:
        return
    if hasattr(update, "data") and hasattr(update, "message"):
        callback = update
        message = callback.message
        data = callback.data
        user = callback.from_user
        sender_id = user.id
        sender_first_name = user.first_name or ""
        sender_username = user.username or ""
        chat = callback.message.chat if callback.message else None
    else:
        event = update.message or update.chat_join_request
        if not event:
            return
        message = event
        data = getattr(message, "text", "")
        user = update.effective_user
        sender_id = user.id
        sender_first_name = user.first_name or ""
        sender_username = user.username or ""
        chat = update.effective_chat
    k = r.get(f"{Dev_Zaid}:botkey") or "☆"
    if data == f"commands1:{user.id}":
        await message.edit_text(
            f"""
للاستفسار - @{channel}

❨ اوامر الرفع والتنزيل ❩

⌯ رفع ↣ ↢ تنزيل مشرف
⌯ رفع ↣ ↢ تنزيل مالك اساسي
⌯ رفع ↣ ↢ تنزيل مالك
⌯ رفع ↣ ↢ تنزيل مدير
⌯ رفع ↣ ↢ تنزيل ادمن
⌯ رفع ↣ ↢ تنزيل مميز
⌯ تنزيل الكل  ↢ بالرد  ↢ لتنزيل الشخص من جميع رتبه
⌯ مسح الكل  ↢ بدون رد  ↢ لتنزيل كل رتب المجموعة

❨ اوامر المسح ❩

⌯ مسح المالكيين
⌯ مسح المدراء
⌯ مسح الادمنيه
⌯ مسح المميزين
⌯ مسح المحظورين
⌯ مسح المكتومين
⌯ مسح قائمة المنع
⌯ مسح رتبه
⌯ مسح الرتب
⌯ مسح الردود
⌯ مسح الاوامر
⌯ مسح + العدد
⌯ مسح بالرد
⌯ مسح الترحيب
⌯ مسح قائمة التثبيت

❨ اوامر الطرد الحظر الكتم ❩

⌯ حظر ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ طرد ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ كتم ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ تقيد ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ الغاء الحظر ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ الغاء الكتم ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ الغاء التقييد ↢ ❨ بالرد،بالمعرف،بالايدي ❩
⌯ رفع القيود ↢ لحذف الكتم,الحظر,التقييد
⌯ منع الكلمة
⌯ منع بالرد على قيف او ستيكر
⌯ الغاء منع الكلمة
⌯ طرد البوتات
⌯ كشف البوتات

❨ اوامر النطق ❩

⌯ انطقي + الكلمة
⌯ وش يقول؟ + بالرد على فويس لترجمه المحتوى

❨ اوامر اخرى ❩

⌯ الرابط
⌯ معلومات الرابط
⌯ انشاء رابط
⌯ بايو
⌯ بايو عشوائي
⌯ ايدي
⌯ الانشاء
⌯ مجموعاتي
⌯ ابلاغ
⌯ نقل ملكية
⌯ صوره
⌯ افتاري
⌯ افتار + باليوزر او الرد
⌯ مين ضافني؟
⌯ شازام، قرآن، سورة + اسم السورة
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("م1 ‣", callback_data="None"),
                        InlineKeyboardButton(
                            "م2", callback_data=f"commands2:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "م3", callback_data=f"commands3:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "الالعاب", callback_data=f"commands4:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "التسليه", callback_data=f"commands5:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "اليوتيوب", callback_data=f"commands6:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "البنك", callback_data=f"commands7:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "زواج", callback_data=f"commands8:{sender_id}"
                        ),
                    ],
                ]
            ),
        )
        return

    if data == f"commands2:{sender_id}":
        await message.edit_text(
            f"""
للاستفسار - @{channel}

❨ اوامر الوضع ❩

⌯ وضع ترحيب
⌯ وضع قوانين
⌯ تغيير رتبه
⌯ تغيير امر

❨ اوامر رؤية الاعدادات ❩

⌯ المطورين
⌯ المالكيين الاساسيين
⌯ المالكيين
⌯ الادمنيه
⌯ المدراء
⌯ المشرفين
⌯ المميزين
⌯ القوانين
⌯ قائمه المنع
⌯ المكتومين
⌯ المطور
⌯ معلوماتي
⌯ الاعدادت
⌯ المجموعه
⌯ الساعه
⌯ التاريخ
⌯ صلاحياتي
⌯ لقبي
⌯ صلاحياته + بالرد
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "م1", callback_data=f"commands1:{sender_id}"
                        ),
                        InlineKeyboardButton("م2 ‣", callback_data="None"),
                    ],
                    [
                        InlineKeyboardButton(
                            "م3", callback_data=f"commands3:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "الالعاب", callback_data=f"commands4:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "التسليه", callback_data=f"commands5:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "اليوتيوب", callback_data=f"commands6:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "البنك", callback_data=f"commands7:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "زواج", callback_data=f"commands8:{sender_id}"
                        ),
                    ],
                ]
            ),
        )
        return

    if data == f"commands3:{sender_id}":
        await message.edit_text(
            f"""
للاستفسار - @{channel}

❨ اوامر الردود ❩

⌯ الردود ↢ تشوف كل الردود المضافه
⌯ الردود المتعدده ↢ تشوف كل الردود المتعدده المضافه
⌯ اضف رد ↢ عشان تضيف رد
⌯ اضف رد متعدد ↢ عشان تضيف أكثر من رد
⌯ اضف رد متعدد ↢ خاص بالاعضاء
⌯ مسح رد ↢ عشان تمسح الرد
⌯ مسح رد متعدد ↢ عشان تمسح رد متعدد
⌯ مسح ردي ↢ عشان تمسح ردك اذا كان بردود الأعضاء
⌯ مسح الردود ↢ تمسح كل الردود
⌯ مسح الردود المتعدده ↢ عشان تمسح كل الردود المتعدده
⌯ الرد + كلمة الرد
-

❨ اوامر القفل والفتح بالمسح ❩

⌯ قفل ↣ ↢ فتح  التعديل
⌯ قفل ↣ ↢ فتح  الفويسات
⌯ قفل ↣ ↢ فتح  الفيديو
⌯ قفل ↣ ↢ فتح  الـصــور
⌯ قفل ↣ ↢ فتح  الملصقات
⌯ قفل ↣ ↢ فتح  الدخول
⌯ قفل ↣ ↢ فتح  الفارسية
⌯ قفل ↣ ↢ فتح  الملفات
⌯ قفل ↣ ↢ فتح  المتحركات
⌯ قفل ↣ ↢ فتح  تعديل الميديا
⌯ قفل ↣ ↢ فتح  تعديل الميديا بالتقييد
⌯ قفل ↣ ↢ فتح  الدردشه
⌯ قفل ↣ ↢ فتح  الروابط
⌯ قفل ↣ ↢ فتح  الهشتاق
⌯ قفل ↣ ↢ فتح  البوتات
⌯ قفل ↣ ↢ فتح  اليوزرات
⌯ قفل ↣ ↢ فتح  الاشعارات
⌯ قفل ↣ ↢ فتح  الكلام الكثير
⌯ قفل ↣ ↢ فتح  التكرار
⌯ قفل ↣ ↢ فتح  التوجيه
⌯ قفل ↣ ↢ فتح  الانلاين
⌯ قفل ↣ ↢ فتح  الجهات
⌯ قفل ↣ ↢ فتح  الــكـــل
⌯ قفل ↣ ↢ فتح  السب
⌯ قفل ↣ ↢ فتح  الاضافه
⌯ قفل ↣ ↢ فتح  الصوت
⌯ قفل ↣ ↢ فتح  القنوات
⌯ قفل ↣ ↢ فتح الايراني
⌯ قفل ↣ ↢ فتح الإباحي

❨ اوامر التفعيل والتعطيل ❩

⌯ تفعيل ↣ ↢ تعطيل الترحيب
⌯ تفعيل ↣ ↢ تعطيل الترحيب بالصورة
⌯ تفعيل ↣ ↢ تعطيل الردود
⌯ تفعيل ↣ ↢ تعطيل ردود الاعضاء
⌯ تفعيل ↣ ↢ تعطيل الايدي
⌯ تفعيل ↣ ↢ تعطيل الرابط
⌯ تفعيل ↣ ↢ تعطيل اطردني
⌯ تفعيل ↣ ↢ تعطيل الحماية
⌯ تفعيل ↣ ↢ تعطيل المنشن
⌯ تفعيل ↣ ↢ تعطيل التحقق
⌯ تفعيل ↣ ↢ تعطيل ردود المطور
⌯ تفعيل ↣ ↢ تعطيل التحذير
⌯ تفعيل ↣ ↢ تعطيل البايو
⌯ تفعيل ↣ ↢ تعطيل انطقي
⌯ تفعيل ↣ ↢ تعطيل شازام
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "م1", callback_data=f"commands1:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "م2", callback_data=f"commands2:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton("م3 ‣", callback_data="None"),
                    ],
                    [
                        InlineKeyboardButton(
                            "الالعاب", callback_data=f"commands4:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "التسليه", callback_data=f"commands5:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "اليوتيوب", callback_data=f"commands6:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "البنك", callback_data=f"commands7:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "زواج", callback_data=f"commands8:{sender_id}"
                        ),
                    ],
                ]
            ),
        )
        return

    if data == f"commands4:{sender_id}":
        await message.edit_text(
            """
☤ تفعيل الالعاب
☤ تعطيل الالعاب
    ╼╾
✽ جمل
✽ كلمات
✽ اغاني
✽ دين
✽ عربي
✽ اكمل
✽ صور
✽ كت تويت
✽ مؤقت
✽ اعلام
✽ معاني
✽ تخمين
✽ احكام
✽ ارقام
✽ احسب
✽ خواتم
✽ انقليزي
✽ ترتيب
✽ انمي
✽ تركيب
✽ تفكيك
✽ عواصم
✽ روليت
✽ سيارات
✽ ايموجي
✽ حجره
✽ تشفير
✽ كره قدم
✽ ديمون
╼╾
❖ فلوسي ↼ عشان تشوف فلوسك
❖ بيع فلوسي + العدد ↼ للأستبدال
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "م1", callback_data=f"commands1:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "م2", callback_data=f"commands2:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "م3", callback_data=f"commands3:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton("الالعاب ‣", callback_data="None"),
                        InlineKeyboardButton(
                            "التسليه", callback_data=f"commands5:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "اليوتيوب", callback_data=f"commands6:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "البنك", callback_data=f"commands7:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "زواج", callback_data=f"commands8:{sender_id}"
                        ),
                    ],
                ]
            ),
        )
        return

    if data == f"commands5:{sender_id}":
        await message.edit_text(
            f"""
للاستفسار - @{channel}

🍰 ⌯ رفع ↣ ↢ تنزيل كيكه
🍯 ⌯ رفع ↣ ↢ تنزيل عسل
💩 ⌯ رفع ↣ ↢ تنزيل زق
🦓 ⌯ رفع ↣ ↢ تنزيل حمار
🐄 ⌯ رفع ↣ ↢ تنزيل بقره
🐩 ⌯ رفع ↣ ↢ تنزيل كلب
🐒 ⌯ رفع ↣ ↢ تنزيل قرد
🐐 ⌯ رفع ↣ ↢ تنزيل تيس
🐂 ⌯ رفع ↣ ↢ تنزيل ثور
🏅 ⌯ رفع ↣ ↢ تنزيل هكر
🐓 ⌯ رفع ↣ ↢ تنزيل دجاجه
🧱 ⌯ رفع ↣ ↢ تنزيل ملكه
🔫 ⌯ رفع ↣ ↢ تنزيل صياد
🐏 ⌯ رفع ↣ ↢ تنزيل خاروف
❤️ ⌯ رفع لقلبي ↣ ↢ تنزيل من قلبي

⌯ قائمة الكيك
⌯ قائمة العسل
⌯ قائمة الزق
⌯ قائمة الحمير
⌯ قائمة البقر
⌯ قائمة الكلاب
⌯ قائمة القرود
⌯ قائمة التيس
⌯ قائمة الثور
⌯ قائمة الهكر
⌯ قائمة الدجاج
⌯ قائمة الهطوف
⌯ قائمة الصيادين
⌯ قائمة الخرفان
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "م1", callback_data=f"commands1:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "م2", callback_data=f"commands2:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "م3", callback_data=f"commands3:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "الالعاب", callback_data=f"commands4:{sender_id}"
                        ),
                        InlineKeyboardButton("التسليه ‣", callback_data="None"),
                    ],
                    [
                        InlineKeyboardButton(
                            "اليوتيوب", callback_data=f"commands6:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "البنك", callback_data=f"commands7:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "زواج", callback_data=f"commands8:{sender_id}"
                        ),
                    ],
                ]
            ),
        )
        return

    if data == f"commands6:{sender_id}":
        await message.edit_text(
            """
⚘ اليـوتيوب

تفعيل اليوتيوب
تعطيل اليوتيوب

❋ البـحث عن اغنية ↓

بحث اسم الاغنية

يوت اسم الاغنية
⚘ الساوند كلاود

تفعيل الساوند
تعطيل الساوند

❋ البـحث عن اغنية ↓

رابط الاغنية أو ساوند + اسم الاغنية

⚘ التيك توك

تفعيل التيك
تعطيل للتيك

❋ للتحميل من التيك ↓

تيك ورابط المقطع
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "م1", callback_data=f"commands1:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "م2", callback_data=f"commands2:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "م3", callback_data=f"commands3:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "الالعاب", callback_data=f"commands4:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "التسليه", callback_data=f"commands5:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton("اليوتيوب ‣", callback_data="None"),
                    ],
                    [
                        InlineKeyboardButton(
                            "البنك", callback_data=f"commands7:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "زواج", callback_data=f"commands8:{sender_id}"
                        ),
                    ],
                ]
            ),
        )
        return

    if data == f"commands7:{sender_id}":
        await message.edit_text(
            """
✜ اوامر البنك

⌯ انشاء حساب بنكي  ↢ تسوي حساب وتقدر تحول فلوس مع مزايا ثانيه

⌯ مسح حساب بنكي  ↢ تلغي حسابك البنكي

⌯ تحويل ↢ تطلب رقم حساب الشخص وتحول له فلوس

⌯ حسابي  ↢ يطلع لك رقم حسابك عشان تعطيه للشخص اللي بيحول لك

⌯ فلوسي ↢ يعلمك كم فلوسك

⌯ راتب ↢ يعطيك راتبك كل ٥ دقيقة

⌯ بخشيش ↢ يعطيك بخشيش كل ٥ دقايق

⌯ زرف ↢ تزرف فلوس اشخاص كل ٥ دقايق

⌯ كنز ↢ يعطيك كنز كل ١٠ دقايق

⌯ استثمار ↢ تستثمر بالمبلغ اللي تبيه مع نسبة ربح مضمونه من ١٪؜ الى ١٥٪؜ ( او استثمار فلوسي )

⌯ حظ ↢ تلعبها بأي مبلغ ياتدبله ياتخسره انت وحظك ( او حظ فلوسي )

⌯ عجله ↢ تلعب عجله الحظ ولو تشابهو ال ٣ ايموجيات تكسب من ١٠٠ الف لحد ٣٠٠ الف انت وحظك

⌯ توب الفلوس ↢ يطلع توب اكثر ناس معهم فلوس بكل القروبات

⌯ توب الحراميه ↢ يطلع لك اكثر ناس زرفوا
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "م1", callback_data=f"commands1:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "م2", callback_data=f"commands2:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "م3", callback_data=f"commands3:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "الالعاب", callback_data=f"commands4:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "التسليه", callback_data=f"commands5:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "اليوتيوب", callback_data=f"commands6:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton("البنك ‣", callback_data="None"),
                        InlineKeyboardButton(
                            "زواج", callback_data=f"commands8:{sender_id}"
                        ),
                    ],
                ]
            ),
        )
        return

    if data == f"commands8:{sender_id}":
        await message.edit_text(
            """
✜ اوامر الزواج

⌯ زواج  ↢ تكتبه بالرد على رسالة شخص مع المهر ويزوجك

⌯ زواجي  ↢ يطلع وثيقة زواجك اذا متزوج

⌯ طلاق ↢ يطلقك اذا متزوج

⌯ خلع  ↢ يخلع زوجك ويرجع له المهر

⌯ زواجات ↢ يطلع اغلى الزواجات بالقروب
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "م1", callback_data=f"commands1:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "م2", callback_data=f"commands2:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "م3", callback_data=f"commands3:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "الالعاب", callback_data=f"commands4:{sender_id}"
                        ),
                        InlineKeyboardButton(
                            "التسليه", callback_data=f"commands5:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "اليوتيوب", callback_data=f"commands6:{sender_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "البنك", callback_data=f"commands7:{sender_id}"
                        ),
                        InlineKeyboardButton("زواج ‣", callback_data="None"),
                    ],
                ]
            ),
        )
        return

    if data == "delAdminMSG":
        if message.text and str(sender_id) in message.text:
            return await message.delete()

    if data == f"yes:{sender_id}":
        try:
            await context.bot.restrict_chat_member(
                message.chat.id,
                sender_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_polls=True,
                    can_invite_users=True,
                    can_change_info=True,
                    can_pin_messages=True,
                    can_send_audios=True,
                    can_send_documents=True,
                    can_send_photos=True,
                    can_send_videos=True,
                    can_send_video_notes=True,
                    can_send_voice_notes=True,
                ),
            )
        except:
            return False
        await message.edit_text(
            f"""
{k} تم التحقق منك وطلعت مو زومبي
{k} الحين تقدر تسولف بالقروب
☆
""",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            ),
        )

    if data == f"no:{sender_id}":
        return await message.edit_text(
            f"""
{k} للأسف طلعت زومبي 🧟‍♀️
{k} مالك غير تنطر حد من المشرفين يجي يتوسطلك
☆
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "رفع التقييد والسماح",
                            callback_data=f"yesVER:{sender_id}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "طرد", callback_data=f"noVER:{sender_id}"
                        )
                    ],
                ]
            ),
        )

    if data.startswith("yesVER"):
        user_id = int(data.split(":")[1])
        if not admin_pls(sender_id, message.chat.id):
            return await message.answer(f"{k} هذا الزر يخص ( الادمن وفوق ) بس", show_alert=True)
        else:
            await message.edit_text(f"{k} توسطلك واحد من الادمن ورفعت عنك القيود")
            try:
                await context.bot.restrict_chat_member(
                    message.chat.id,
                    user_id,
                    ChatPermissions(
                        can_send_messages=True,
                    can_send_audios=True,
                    can_send_documents=True,
                    can_send_photos=True,
                    can_send_videos=True,
                    can_send_video_notes=True,
                    can_send_voice_notes=True,
                        can_send_other_messages=True,
                        can_send_polls=True,
                        can_invite_users=True,
                        can_add_web_page_previews=True,
                        can_change_info=True,
                        can_pin_messages=True,
                    ),
                )
            except:
                return False

    if data.startswith("noVER"):
        user_id = int(data.split(":")[1])
        if not admin_pls(sender_id, message.chat.id):
            return await message.answer(f"{k} هذا الزر يخص ( الادمن وفوق ) بس", show_alert=True)
        else:
            await message.edit_text(f"{k} انقلع برا القروب يلا")
            try:
                await context.bot.ban_chat_member(chat.id, user_id)
                await context.bot.unban_chat_member(chat.id, user_id)
            except:
                pass

    if data == "yes:del:bank":
        if not devp_pls(sender_id, message.chat.id):
            return await message.answer("تعجبني ثقتك")
        else:
            await message.edit_text("ابشر صفرت البنك")
            keys = r.keys("*:Floos")
            for a in keys:
                r.delete(a)
            for a in r.keys("*:BankWait"):
                r.delete(a)
            for a in r.keys("*:BankWaitB5"):
                r.delete(a)
            for a in r.keys("*:BankWaitZRF"):
                r.delete(a)
            for a in r.keys("*:BankWaitEST"):
                r.delete(a)
            for a in r.keys("*:BankWaitHZ"):
                r.delete(a)
            for a in r.keys("*:BankWait3JL"):
                r.delete(a)
            for a in r.keys("*:Zrf"):
                r.delete(a)
            r.delete("BankTop")
            r.delete("BankTopZRF")
            return True

    if data == "no:del:bank":
        if not devp_pls(sender_id, message.chat.id):
            return await message.answer("تعجبني ثقتك")
        else:
            await message.delete()

    if data == f"topfloos:{sender_id}":
        if not r.smembers("BankList"):
            return await message.answer(f"{k} مافيه حسابات بالبنك", show_alert=True)
        else:
            rep = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("‣ 💸", callback_data="None"),
                        InlineKeyboardButton(
                            "توب الحرامية 💰", callback_data=f"topzrf:{sender_id}"
                        ),
                    ],
                    [InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")],
                ]
            )
            if r.get("BankTop"):
                text = r.get("BankTop")
                if not r.get(f"{sender_id}:Floos"):
                    floos = 0
                else:
                    floos = int(r.get(f"{sender_id}:Floos") or 0)
                get = r.ttl("BankTop")
                wait = time.strftime("%M:%S", time.gmtime(get))
                text += "\n━━━━━━━━━"
                text += f"\n# You ) {floos:,} 💸 l {sender_first_name}"
                text += f"\n\n[قوانين التُوب](https://t.me/{botUsername}?start=rules)"
                text += f"\n\nالقائمة تتحدث بعد {wait} دقيقة"
                return await message.edit_text(
                    text, disable_web_page_preview=True, reply_markup=rep
                )
            else:
                users = []
                ccc = 0
                for user in r.smembers("BankList"):
                    ccc += 1
                    id = int(user)
                    if r.get(f"{id}:bankName"):
                        name = r.get(f"{id}:bankName")[:10]
                    else:
                        try:
                            name = context.bot.get_chat(id).first_name
                            r.set(f"{id}:bankName", name)
                        except:
                            name = "INVALID_NAME"
                            r.set(f"{id}:bankName", name)
                    if not r.get(f"{id}:Floos"):
                        floos = 0
                    else:
                        floos = int(r.get(f"{id}:Floos") or 0)
                    users.append({"name": name, "money": floos})
                top = get_top(users)
                text = "توب 20 اغنى اشخاص:\n\n"
                count = 0
                for user in top:
                    count += 1
                    if count == 21:
                        break
                    emoji = get_emoji_bank(count)
                    floos = user["money"]
                    name = user["name"]
                    text += f'**{emoji}{floos:,}** 💸 l {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}\n'
                r.set("BankTop", text, ex=300)
                if not r.get(f"{sender_id}:Floos"):
                    floos_from_user = 0
                else:
                    floos_from_user = int(r.get(f"{sender_id}:Floos") or 0)
                text += "\n━━━━━━━━━"
                text += f"\n# You ) {floos_from_user:,} 💸 l {sender_first_name}"
                text += f"\n\n[قوانين التُوب](https://t.me/{botUsername}?start=rules)"
                get = r.ttl("BankTop")
                wait = time.strftime("%M:%S", time.gmtime(get))
                text += f"\n\nالقائمة تتحدث بعد {wait} دقيقة"
                await message.edit_text(
                    text, disable_web_page_preview=True, reply_markup=rep
                )

    if data == f"topzrf:{sender_id}":
        if not r.smembers("BankList"):
            return await message.answer(f"{k} مافيه حسابات بالبنك", show_alert=True)
        else:
            rep = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "توب الفلوس 💸", callback_data=f"topfloos:{sender_id}"
                        ),
                        InlineKeyboardButton("‣ 💰", callback_data="None"),
                    ],
                    [InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")],
                ]
            )
            if r.get("BankTopZRF"):
                text = r.get("BankTopZRF")
                if not r.get(f"{sender_id}:Zrf"):
                    zrf = 0
                else:
                    zrf = int(r.get(f"{sender_id}:Zrf") or 0)
                get = r.ttl("BankTopZRF")
                wait = time.strftime("%M:%S", time.gmtime(get))
                text += "\n━━━━━━━━━"
                text += f"\n# You ) {zrf:,} 💰 l {sender_first_name}"
                text += f"\n\n[قوانين التُوب](https://t.me/{botUsername}?start=rules)"
                text += f"\n\nالقائمة تتحدث بعد {wait} دقيقة"
                return await message.edit_text(
                    text, disable_web_page_preview=True, reply_markup=rep
                )
            else:
                users = []
                ccc = 0
                for user in r.smembers("BankList"):
                    ccc += 1
                    id = int(user)
                    if r.get(f"{id}:bankName"):
                        name = r.get(f"{id}:bankName")[:10]
                    else:
                        try:
                            name = context.bot.get_chat(id).first_name
                            r.set(f"{id}:bankName", name)
                        except:
                            name = "INVALID_NAME"
                            r.set(f"{id}:bankName", name)
                    if not r.get(f"{id}:Zrf"):
                        pass
                    else:
                        zrf = int(r.get(f"{id}:Zrf") or 0)
                        users.append({"name": name, "money": zrf})
                top = get_top(users)
                text = "توب 20 اكثر الحراميه زرفًا:\n\n"
                count = 0
                for user in top:
                    count += 1
                    if count == 21:
                        break
                    emoji = get_emoji_bank(count)
                    floos = user["money"]
                    name = user["name"]
                    text += f'**{emoji}{floos}** 💰 l {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}\n'
                r.set("BankTopZRF", text, ex=300)
                if not r.get(f"{sender_id}:Zrf"):
                    floos_from_user = 0
                else:
                    floos_from_user = int(r.get(f"{sender_id}:Zrf") or 0)
                text += "\n━━━━━━━━━"
                text += f"\n# You ) {floos_from_user} 💰 l {sender_first_name}"
                text += f"\n\n[قوانين التُوب](https://t.me/{botUsername}?start=rules)"
                get = r.ttl("BankTopZRF")
                wait = time.strftime("%M:%S", time.gmtime(get))
                text += f"\n\nالقائمة تتحدث بعد {wait} دقيقة"
                await message.edit_text(
                    text, disable_web_page_preview=True, reply_markup=rep
                )

    """
   if data == f'toplast:{sender_id}':
     if not r.get(f'BankTopLast') and not r.get(f'BankTopLastZrf'):
       return await message.answer(f'{k} مافي توب اسبوع الي فات',show_alert=True)
     else:
       text = 'توب أوائل الأسبوع الي راح:\n'
       text += r.get(f'BankTopLast')
       text += '\n\nتوب حرامية الاسبوع اللي راح:\n'
       text += r.get(f'BankTopLastZrf')
       text += '\n༄'
       rep = InlineKeyboardMarkup (
         [[InlineKeyboardButton ('🧚‍♀️', url=f't.me/{channel}')]]
       )
       await message.edit_text(text, disable_web_page_preview=True,reply_markup=rep)
   """

    name = r.get(f'{Dev_Zaid}:BotName') or NAME
    if data == f"RPS:rock++{sender_id}":
        RPS = ["paper", "scissors", "rock"]
        kk = random.choice(RPS)
        if kk == "scissors":
            if r.get(f"{sender_id}:Floos"):
                get = int(r.get(f"{sender_id}:Floos") or 0)
                r.set(f"{sender_id}:Floos", get + 1)
            else:
                r.set(f"{sender_id}:Floos", 1)
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await message.edit_text(
                f"""
أنت: 🪨
أنا: ✂️

النتيجة: ⁪⁬⁪⁬ 🏆 {sender_first_name}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )

        if kk == "paper":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await message.edit_text(
                f"""
أنت: 🪨
أنا: 📃

النتيجة: ⁪⁬⁪⁬ 🏆️ {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )
        if kk == "rock":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await message.edit_text(
                f"""
أنت: 🪨
أنا: 🪨

النتيجة: ⁪⁬⁪⁬ ⚖️ {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )

    if data == f"gowner+{sender_id}":
        if not gowner_pls(sender_id, message.chat.id):
            message.answer("هذا الامر للمالك الاساسي و فوق بس", show_alert=True)
            return await message.delete()
        else:
            command = message.reply_to_message.text.split(None, 2)[2]
            r.hset(Dev_Zaid + f"locks-{message.chat.id}", command, 0)
            return await message.edit_text(
                f"- تم تعيين الامر ( {command} ) للمالك الاساسي وفوق فقط"
            )

    if data == f"owner+{sender_id}":
        if not gowner_pls(sender_id, message.chat.id):
            message.answer("هذا الامر للمالك الاساسي و فوق بس", show_alert=True)
            return await message.delete()
        else:
            command = message.reply_to_message.text.split(None, 2)[2]
            r.hset(Dev_Zaid + f"locks-{message.chat.id}", command, 1)
            return await message.edit_text(
                f"- تم تعيين الامر ( {command} ) للمالك وفوق فقط"
            )

    if data == f"mod+{sender_id}":
        if not gowner_pls(sender_id, message.chat.id):
            message.answer("هذا الامر للمالك الاساسي و فوق بس", show_alert=True)
            return await message.delete()
        else:
            command = message.reply_to_message.text.split(None, 2)[2]
            r.hset(Dev_Zaid + f"locks-{message.chat.id}", command, 2)
            return await message.edit_text(
                f"- تم تعيين الامر ( {command} ) للمدير وفوق فقط"
            )

    if data == f"admin+{sender_id}":
        if not gowner_pls(sender_id, message.chat.id):
            message.answer("هذا الامر للمالك الاساسي و فوق بس", show_alert=True)
            return await message.delete()
        else:
            command = message.reply_to_message.text.split(None, 2)[2]
            r.hset(Dev_Zaid + f"locks-{message.chat.id}", command, 3)
            return await message.edit_text(
                f"- تم تعيين الامر ( {command} ) للادمن وفوق فقط"
            )

    if data == f"pre+{sender_id}":
        if not gowner_pls(sender_id, message.chat.id):
            message.answer("هذا الامر للمالك الاساسي و فوق بس", show_alert=True)
            return await message.delete()
        else:
            command = message.reply_to_message.text.split(None, 2)[2]
            r.hset(Dev_Zaid + f"locks-{message.chat.id}", command, 4)
            return await message.edit_text(
                f"- تم تعيين الامر ( {command} ) للمميز وفوق فقط"
            )

    if data == f"RPS:paper++{sender_id}":
        RPS = ["paper", "scissors", "rock"]
        kk = random.choice(RPS)
        if kk == "rock":
            if r.get(f"{sender_id}:Floos"):
                get = int(r.get(f"{sender_id}:Floos") or 0)
                r.set(f"{sender_id}:Floos", get + 1)
            else:
                r.set(f"{sender_id}:Floos", 1)
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await message.edit_text(
                f"""
أنت: 📃
أنا: 🪨

النتيجة: ⁪⁬⁪⁬ 🏆 {sender_first_name}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )

        if kk == "scissors":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await message.edit_text(
                f"""
أنت: 📃
أنا: ✂️

النتيجة: ⁪⁬⁪⁬ 🏆️ {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )
        if kk == "paper":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await message.edit_text(
                f"""
أنت: 📃
أنا: 📃

النتيجة: ⁪⁬⁪⁬ ⚖️ {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )

    if data == f"RPS:scissors++{sender_id}":
        RPS = ["paper", "scissors", "rock"]
        kk = random.choice(RPS)
        if kk == "paper":
            if r.get(f"{sender_id}:Floos"):
                get = int(r.get(f"{sender_id}:Floos") or 0)
                r.set(f"{sender_id}:Floos", get + 1)
            else:
                r.set(f"{sender_id}:Floos", 1)
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await message.edit_text(
                f"""
أنت: ✂️
أنا: 📃

النتيجة: ⁪⁬⁪⁬ 🏆 {sender_first_name}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )

        if kk == "rock":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await message.edit_text(
                f"""
أنت: ✂️
أنا: 🪨

النتيجة: ⁪⁬⁪⁬ 🏆️ {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )
        if kk == "scissors":
            rep = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🧚‍♀️", url=f"t.me/{channel}")]]
            )
            await message.edit_text(
                f"""
أنت: ✂️
أنا: ✂️

النتيجة: ⁪⁬⁪⁬ ⚖️ {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}
""",
                disable_web_page_preview=True,
                reply_markup=rep,
            )

# ==================== تسجيل المعالجات ====================

def register(app):
    """Register handlers from all.py into the Application."""
    app.add_handler(
        MessageHandler(
            filters.ALL
            & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
            on_zbi,
        ),
        group=2,
    )
    app.add_handler(
        MessageHandler(
            filters.ALL
            & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
            guardLocksResponse,
        ),
        group=0,
    )
    app.add_handler(
        MessageHandler(
            filters.ALL
            & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
            guardLocksResponse2,
        ),
        group=1,
    )
    app.add_handler(ChatJoinRequestHandler(antiPersian))
    app.add_handler(
        MessageHandler(
            filters.TEXT
            & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
            guardCommandsHandler,
        ),
        group=3,
    )
    app.add_handler(CallbackQueryHandler(callback_query_handler))
