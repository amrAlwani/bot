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

import random, re, time, os, sys, pytz, string 




from datetime import datetime 
from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ChatPermissions, InputMediaAudio, InputMediaVideo, InputMediaPhoto,
    InputMediaDocument, InputTextMessageContent, InlineQueryResultArticle,
    InlineQueryResultAudio)
from telegram.constants import ParseMode, ChatMemberStatus, ChatType
from telegram.error import BadRequest, RetryAfter, Forbidden
from telegram.ext import ContextTypes, MessageHandler, filters
import asyncio

from config import *
from helpers.Ranks import *
from helpers.Ranks import isLockCommand

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
    @staticmethod
    def on_edited_message(*args, **kwargs):
        def decorator(func): return func
        return decorator
    @staticmethod
    def on_chat_member_updated(*args, **kwargs):
        def decorator(func): return func
        return decorator

Client = _DummyClient()


def get_sarhni_id():
   rndm = ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(10)])
   return rndm
   
async def sarhniHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await sarhniFunc(update, context, k)
    
async def sarhniFunc(update, context, k):
   message = update.message
   chat = update.effective_chat
   user = update.effective_user
   if not message or not chat or not user:
       return
   if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}'):  return
   if r.get(f'{chat.id}:delCustom:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:delCustomG:{user.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return  
   if r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}'):  return 
   text = message.text
   name = r.get(f'{Dev_Zaid}:BotName') or NAME
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}'):
       text = r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}')
   if r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')
   
   if text == 'صارحني':
     if not r.get(f'{user.id}:sar7ni:{Dev_Zaid}'):
       id = get_sarhni_id()
       r.set(f'{user.id}:sar7ni:{Dev_Zaid}',id)
       r.set(f'{id}:sarhni:{Dev_Zaid}',user.id)
     else:
       id = r.get(f'{user.id}:sar7ni:{Dev_Zaid}')
     r.set(f'{user.id}:sarhniname', user.first_name)
     return await message.reply_text(f'{k} أهلين عيني「 ⁪⁬⁪⁬{user.mention_html()} 」\n{k} هذا رابط صارحني الخاص فيك', reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ('📩',url=f't.me/{botUsername}?start=sarhni{id}')]]))

async def sarhniHandlerP(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'scatteredda'
    await sarhniFuncP(update, context, k, channel)

async def sarhniFuncP(update, context, k, channel):

   message = update.message

   chat = update.effective_chat

   user = update.effective_user
   if message.text:
      text = message.text
      if text.startswith('/start sarhni'):
        id = text.split('sarhni')[1]
        if not r.get(f'{id}:sarhni:{Dev_Zaid}'):
          return await message.reply_text(f'{k} رابط صارحني غلط')
        else:
          user_id = int(r.get(f'{id}:sarhni:{Dev_Zaid}'))
          if user.id == user_id:
            return await message.reply_text('انت هطف تدخل رابط صراحة حقك؟')
          get = await context.bot.get_chat(user_id)
          r.set(f'{user.id}:sarhni',get.id,ex=300)
          a = await message.reply_text(f'{k} دخلت الحين رابط صارحني مع 「 ⁪⁬⁪⁬{get.first_name} 」\n{k} اي رسالة ترسلها لي راح احولها له بسرية تامة بدون مايعرفك\n༄',reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ('الغاء', callback_data='sarhni:bye')],[InlineKeyboardButton ('🧚‍♀️',url=f't.me/{channel}')]]),quote=True)
          return a.pin(both_sides=True)
      
      if r.get(f'{user.id}:sarhni') and len(text) < 1000:
        user_id = int(r.get(f'{user.id}:sarhni'))
        name = r.get(f'{user_id}:sarhniname')
        TIME_ZONE = "Asia/Riyadh"
        ZONE = pytz.timezone(TIME_ZONE)
        TIME = datetime.now(ZONE)
        clock = TIME.strftime("%I:%M %p")
        date = TIME.strftime("%d/%m/%Y")
        txt = f'{k} وصلتك رسالة مصارحة جديدة\n{k} التاريخ : {date}\n{k} الساعة : {clock}\n\n{k} الرسالة :\n\n{text}\n☆'
        try:
          await context.bot.send_message(user_id, txt, disable_web_page_preview=True,reply_markup=InlineKeyboardMarkup ([
            [
              InlineKeyboardButton ('رد', callback_data=f'sarhni+rep{user.id}'),
            ],
            [
              InlineKeyboardButton ('🧚‍♀️',url=f't.me/{channel}')
            ]
          ]))
          return await message.reply_text(f'{k} ابشر ارسلت رسالتك بسرية تامة لـ {name}',quote=True)
        except Exception as e:  
          print(e)
          return await message.reply_text('مقدر ارسله شيء يمكن حاظرني',quote=True)
   
   if r.get(f'{user.id}:sarhni'):
     user_id = int(r.get(f'{user.id}:sarhni'))
     name = r.get(f'{user_id}:sarhniname')
     TIME_ZONE = "Asia/Riyadh"
     ZONE = pytz.timezone(TIME_ZONE)
     TIME = datetime.now(ZONE)
     clock = TIME.strftime("%I:%M %p")
     date = TIME.strftime("%d/%m/%Y")
     txt = f'{k} وصلتك رسالة مصارحة جديدة\n{k} التاريخ : {date}\n{k} الساعة : {clock}\n\n{k} الرسالة :'
     try:
       await context.bot.send_message(user_id, txt, disable_web_page_preview=True)
       message.copy(user_id,
       reply_markup=InlineKeyboardMarkup ([
            [
              InlineKeyboardButton ('رد', callback_data=f'sarhni+rep{user.id}'),
            ],
            [
              InlineKeyboardButton ('🧚‍♀️',url=f't.me/{channel}')
            ]
          ])
       )
       return await message.reply_text(f'{k} ابشر ارسلت رسالتك بسرية تامة لـ {name}',quote=True)
     except Exception as e:
       print(e)
       return await message.reply_text('مقدر ارسله شيء يمكن حاظرني',quote=True)
   
   if r.get(f'{user.id}:sarhnirep'):
     user_id = int(r.get(f'{user.id}:sarhnirep'))
     r.delete(f'{user.id}:sarhnirep')
     await message.reply_text(f'{k} ابشر ارسلت له ردك',quote=True)
     await context.bot.forward_message(user_id, message.chat.id, message.message_id)

@Client.on_callback_query()
async def sarhni_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
   query = update.callback_query
   if not query: return
   message = query
   user = update.effective_user
   chat = update.effective_chat
   if message.data == 'sarhni:bye':
     r.delete(f'{user.id}:sarhni')
     await message.message.delete()
     return await message.answer('ابشر طلعتك من كل جلسة صارحني', show_alert=True)
   
   if message.data.startswith('sarhni+rep'):
     user_id = int(message.data.split('rep')[1])
     if not r.get(f'{user_id}:sarhni'):
       return await message.answer('مايمدي ترد عليه لأنه طلع من جلسة صارحني', show_alert=True)
     if not int(r.get(f'{user_id}:sarhni')) == user.id:
       return await message.answer('مايمدي ترد عليه لأنه طلع من جلسة صارحني', show_alert=True)
     else:
       r.set(f'{user.id}:sarhnirep', user_id,ex=300)
       return await context.bot.send_message(user.id, 'ارسل الرد الحين')
       
     


   
   
   
   

def register(app):
    """Register sarhni handlers."""
    from telegram.ext import MessageHandler, CallbackQueryHandler, filters
    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.GROUPS,
        sarhniHandler
    ), group=19)
    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.PRIVATE,
        sarhniHandlerP
    ), group=42)
    app.add_handler(CallbackQueryHandler(sarhni_callback, pattern=r'^sarhni'))
