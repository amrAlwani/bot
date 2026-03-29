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

import random, re, time, os, sys




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


async def replaceCode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'scatteredda'
    await raplaceCodefunc(update, context, k, channel)
    
async def raplaceCodefunc(update, context, k, channel):
    
   message = update.message
    
   chat = update.effective_chat
    
   user = update.effective_user
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
       
   '''
   if text == 'الملفات':
     if user.id == 6168217372:
        text = '——— ملفات السورس ———'
        a = os.listdir('Plugins')
        a.sort()
        count = 1
        for file in a:
          if file.endswith('.py'):
            text += f'\n{count}) `{file}`'
            count += 1
        text += f'\n——— @{channel} ———'
        return await message.reply_text(text, disable_web_page_preview=True)
   '''
   if r.get(f'{chat.id}:replace:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:replace2:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:replace3:{user.id}{Dev_Zaid}'):
     if text == 'الغاء':
       r.delete(f'{chat.id}:replace:{user.id}{Dev_Zaid}')
       r.delete(f'{chat.id}:replace2:{user.id}{Dev_Zaid}')
       r.delete(f'{chat.id}:replace3:{user.id}{Dev_Zaid}')
       return await message.reply_text(f'{k} من عيوني لغيت استبدال كلمة ')
      
   if text == 'استبدال كلمه' or text == 'استبدال كلمة':
      if not devp_pls(user.id,chat.id):
         return await message.reply_text(f'{k} هذا الأمر يخص ( مبرمج السورس ) بس')
      else:
         r.set(f'{chat.id}:replace:{user.id}{Dev_Zaid}',1,ex=600)
         return await message.reply_text(f'{k} ارسل الكلمة القديمة الآن')
   
   if r.get(f'{chat.id}:replace:{user.id}{Dev_Zaid}') and devp_pls(user.id,chat.id):
      r.set(f'{chat.id}:replace2:{user.id}{Dev_Zaid}',message.text,ex=600)
      r.delete(f'{chat.id}:replace:{user.id}{Dev_Zaid}')
      return await message.reply_text(f'{k} ارسل الكلمة الجديدة الحين')
   
   if r.get(f'{chat.id}:replace2:{user.id}{Dev_Zaid}') and devp_pls(user.id,chat.id):
      txt = r.get(f'{chat.id}:replace2:{user.id}{Dev_Zaid}')
      r.delete(f'{chat.id}:replace2:{user.id}{Dev_Zaid}')
      r.set(f'{chat.id}:replace3:{user.id}{Dev_Zaid}',f'{txt}&&new&&{message.text}',ex=600)
      a = os.listdir('Plugins')
      a.sort()
      txt = f'{k} ارسل اسم الملف الي تبي تعدل فيه الحين:'
      count = 1
      txt += '\n\n——— ملفات السورس ———'
      for file in a:
          if file.endswith('.py'):
            txt += f'\n{count}) `{file}`'
            count += 1
      txt += f'\n——— @{channel} ———'
      return await message.reply_text(txt)
   
   if r.get(f'{chat.id}:replace3:{user.id}{Dev_Zaid}') and devp_pls(user.id,chat.id) and message.text in os.listdir('Plugins'):
      mm = await message.reply_text(f'{k} جاريع تعديل الملف')
      get = r.get(f'{chat.id}:replace3:{user.id}{Dev_Zaid}')
      old = get.split('&&new&&')[0]
      new = get.split('&&new&&')[1]
      r.delete(f'{chat.id}:replace3:{user.id}{Dev_Zaid}')
      with open(f'Plugins/{message.text}','r') as Read:
         old_confing = Read.read()
         mmessage.edit(f'{k} تم فتح الملف وقرائته')
      with open(f'Plugins/{message.text}','w+') as Write:
         mmessage.edit(f'{k} تم فتح الملف جاري كتابة الكود مع استبدال الكلمة')
         Write.write(old_confing.replace(old,new))
      mmessage.edit(f'{k} تم فتح الملف `{message.text}` وتعديله\n{k} تم استبدال الكلمة القديمة ( {old} ) بالكلمة الجديدة ( {new} )')
      python = sys.executable
      os.execl(python, python, *sys.argv)
      
      
      
      
      
   

def register(app):
    """Register replace handlers."""
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(
        filters.TEXT & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
        replaceCode
    ), group=14)
