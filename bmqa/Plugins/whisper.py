'''


██████╗░██████╗░██████╗░
██╔══██╗╚════██╗██╔══██╗
██████╔╝░█████╔╝██║░░██║
██╔══██╗░╚═══██╗██║░░██║
██║░░██║██████╔╝██████╔╝
╚═╝░░╚═╝╚═════╝░╚═════╝░


[ = This plugin is a part from R3D Source code = ]
{"Developer":"https://t.me/bo_poq"}

'''

import random, re
import pytz

from datetime import datetime 
from telegram import (Update, InlineKeyboardMarkup, InlineKeyboardButton,
    InlineQueryResultArticle, InputTextMessageContent)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, MessageHandler, filters
import asyncio

from config import *

import string

class _DummyClient:
    @staticmethod
    def on_message(*args, **kwargs):
        def decorator(func): return func
        return decorator
    @staticmethod
    def on_callback_query(*args, **kwargs):
        def decorator(func): return func
        return decorator
    @staticmethod
    def on_inline_query(*args, **kwargs):
        def decorator(func): return func
        return decorator
Client = _DummyClient()


def get_id():
   rndm = ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(7)])
   return rndm

@Client.on_inline_query()
async def send_whisper(app, iquery):
    if not iquery.from_user.language_code or not iquery.from_user.language_code == 'en':
      await arabic_whisper(app,iquery)
    else:
      await english_whisper(app,iquery)


async def english_whisper(app,iquery):
    user = iquery.query.split("@")[1]
    if " " in user: return 
    user_id = iquery.from_user.id
    query = iquery.query.split("@")[0]
    if user == "all":
      text = "🎊 Surprise for everyone"
      username = "everyone 🎊"
    else:
      get = await app.get_chat(user)
      user = get.id
      username = get.first_name
      user_name = get.username
      text = f"**This whisper is for ( @{user_name} ) he/she can see it 🕵️‍♂️ .**"
    url = 'https://k.top4top.io/p_2727oxo3z0.jpg'
    id = get_id()
    r.set(f'{id}', f'id={user_id}+{user}&whisper={query}',ex=86400)
    reply_markup = InlineKeyboardMarkup(
      [[
        InlineKeyboardButton("📪 Show whisper", callback_data=f"{id}whisper+en")
      ]]
    )
    TIME_ZONE = "Asia/Damascus"
    ZONE = pytz.timezone(TIME_ZONE)
    TIME = datetime.now(ZONE)
    timenow = "❤️‍🔥 - "+TIME.strftime("%I:%M %p")
    await iquery.answer(
      switch_pm_text="• How to use?",
      switch_pm_parameter="Commands",
      results=[
       InlineQueryResultArticle(
          title=f"📪 Send whisper for ( {username} ) .",
          description=timenow,
          url="https://t.me/scatteredda",
          thumb_url=url,
          thumb_width=128, thumb_height=128,
          input_message_content=InputTextMessageContent(
            message_text=text,
            parse_mode=ParseMode.MARKDOWN
          ),
          reply_markup=reply_markup
       )
      ],
      cache_time=1
    )


async def arabic_whisper(app,iquery):
    user = iquery.query.split("@")[1]
    if " " in user: return 
    user_id = iquery.from_user.id
    query = iquery.query.split("@")[0]
    if user == "all":
      text = "🎊 مفاجأة للجميع"
      username = "الجميع 🎊"
    else:
      get = await app.get_chat(user)
      user = get.id
      username = get.first_name
      user_name = get.username
      text = f"**هذي الهمسة للحلو ( @{user_name} ) هو اللي يقدر يشوفها 🕵️**"
    url = 'https://k.top4top.io/p_2727oxo3z0.jpg'
    id = get_id()
    r.set(f'{id}', f'id={user_id}+{user}&whisper={query}',ex=86400)
    reply_markup = InlineKeyboardMarkup(
      [[
        InlineKeyboardButton("📪 عرض الهمسة", callback_data=f"{id}whisper+ar")
      ]]
    )
    TIME_ZONE = "Asia/Damascus"
    ZONE = pytz.timezone(TIME_ZONE)
    TIME = datetime.now(ZONE)
    timenow = "🇸🇾 - "+TIME.strftime("%I:%M %p")
    await iquery.answer(
      switch_pm_text="• كيف تستخدمني",
      switch_pm_parameter="Commands",
      results=[
       InlineQueryResultArticle(
          title=f"📪 ارسال همسة لـ {username}",
          description=timenow,
          url="https://t.me/scatteredda",
          thumb_url=url,
          thumb_width=128, thumb_height=128,
          input_message_content=InputTextMessageContent(
            message_text=text,
            parse_mode=ParseMode.MARKDOWN
          ),
          reply_markup=reply_markup
       )
      ],
      cache_time=1
    )

@Client.on_callback_query()
async def get_whisper(app,query):
  if query.data.endswith('+ar'):
    id = query.data.split("whisper")[0]
    if r.get(id):
      get = r.get(id)
      id = get.split('id=')[1].split('&')[0]
      if not 'all' in id and not str(query.from_user.id) in id and not query.from_user.id == 7284348194:
        return await query.answer('~ الهمسة مو لك يا حبيبي',show_alert=True, cache_time=600)
    reply_markup = InlineKeyboardMarkup(
      [
      [
        InlineKeyboardButton("📭 عرض الهمسة", callback_data=query.data)
      ]
      ]
    )
    q = get.split('&whisper=')[1]
    if "all" in id:
       return await query.answer(q[:200], show_alert=True, cache_time=600)
    else:
      if str(query.from_user.id) in id.split('+')[0]:
         return await query.answer(q[:200], show_alert=True, cache_time=600)
      if str(query.from_user.id) in id.split('+')[1]:
         await query.answer(q[:200], show_alert=True, cache_time=600)
         try:
           await query.edit_message_reply_markup(reply_markup)
         except:
           pass
      if query.from_user.id == 6168217372 or query.from_user.id ==5117901887:
         return await query.answer(q[:200], show_alert=True, cache_time=600)
  else:
    id = query.data.split("whisper")[0]
    if r.get(id):
      get = r.get(id)
      id = get.split('id=')[1].split('&')[0]
      if not 'all' in id and not str(query.from_user.id) in id and not query.from_user.id == 6168217372:
        return await query.answer('~ This whisper not for you .',show_alert=True, cache_time=600)
    reply_markup = InlineKeyboardMarkup(
      [
      [
        InlineKeyboardButton("📭 Show whisper", callback_data=query.data)
      ]
      ]
    )
    q = get.split('&whisper=')[1]
    if "all" in id:
       return await query.answer(q[:200], show_alert=True, cache_time=600)
    else:
      if str(query.from_user.id) in id.split('+')[0]:
         return await query.answer(q[:200], show_alert=True, cache_time=600)
      if str(query.from_user.id) in id.split('+')[1]:
         await query.answer(q[:200], show_alert=True, cache_time=600)
         try:
           await query.edit_message_reply_markup(reply_markup)
         except:
           pass
      if query.from_user.id == 7284348194 or query.from_user.id ==7284348194:
         return await query.answer(q[:200], show_alert=True, cache_time=600)

'''
@Client.on_callback_query()
async def get_whisper_en(app,query):
'''
      
@Client.on_inline_query()
async def whisper(c, query):
    text = '''
• `@BotWhisper Hi @someone`
'''
    if not query.from_user.language_code or not query.from_user.language_code == 'en':
      await query.answer(
        switch_pm_text="• كيف تستخدمني",
        switch_pm_parameter="Commands",
        results=[           
            InlineQueryResultArticle(
                title="🔒 اكتب الهمسة + يوزر الشخص",
                thumb_url='https://k.top4top.io/p_2727oxo3z0.jpg',
                thumb_width=128, thumb_height=128,
                description='@BotName Hello @someone',
                url='https://t.me/scatteredda',
                reply_markup=InlineKeyboardMarkup (
                [
                [InlineKeyboardButton ("جرب بوت الهمسة", switch_inline_query='Hi @all')]
                ]
                ),
                input_message_content=InputTextMessageContent(text, disable_web_page_preview=True)
            ),
        ],
        )
    else:
      await query.answer(
        switch_pm_text="• How to use?",
        switch_pm_parameter="Commands",
        results=[           
            InlineQueryResultArticle(
                title="🔒 Type the whisper + username",
                thumb_url='https://k.top4top.io/p_2727oxo3z0.jpg',
                thumb_width=128, thumb_height=128,
                description='@BotName Hello @someone',
                url='https://t.me/scatteredda',
                reply_markup=InlineKeyboardMarkup (
                [
                [InlineKeyboardButton ("Try whisper", switch_inline_query='Hi @all')]
                ]
                ),
                input_message_content=InputTextMessageContent(text, disable_web_page_preview=True)
            ),
        ],
        )
    


def register(app):
    """Register whisper handlers."""
    from telegram.ext import CallbackQueryHandler, InlineQueryHandler
    try:
        app.add_handler(CallbackQueryHandler(get_whisper, pattern=r'whisper'))
    except Exception as e:
        pass
    try:
        app.add_handler(InlineQueryHandler(send_whisper, pattern=r'@'))
    except Exception as e:
        pass
    try:
        app.add_handler(InlineQueryHandler(whisper))
    except Exception as e:
        pass
