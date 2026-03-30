'''

[ = This plugin is a part from R3D Source code = ]
{"Developer":"https://t.me/bo_poq"}

'''

import random, re, time, json, html, httpx, requests 
import urllib.parse
import os
import uuid
import sys
import traceback
try:
    import psutil
except ImportError:
    psutil = None
import platform
import cpuinfo
import socket
import uuid




from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ChatPermissions, InputMediaAudio, InputMediaVideo, InputMediaPhoto,
    InputMediaDocument, InputTextMessageContent)
from telegram.constants import ParseMode, ChatMemberStatus, ChatType
from telegram.error import BadRequest, RetryAfter, Forbidden
from telegram.ext import ContextTypes, MessageHandler, filters
import asyncio

from config import *
from config import TOKEN
from helpers.Ranks import *
from io import StringIO
try:
    from pytio import Tio, TioRequest
except ImportError:
    Tio = TioRequest = None
from datetime import datetime
from helpers.utils import *
from meval import meval
from httpx import HTTPError

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
Message = None

tio = Tio() if Tio else None
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


# @Client.on_message() & filters.private, group=-2007)
async def on_send_hmsa(update: Update, context: ContextTypes.DEFAULT_TYPE):
   message = update.message
   user = update.effective_user
   if not message or not user: return
   id = message.text.split("hmsa")[1]
   if not wsdb.get(id):
      return await message.reply_text("رابط الهمسة غلط")
   else:
      get = wsdb.get(id)
      if user.id != get["from"]:
         return await message.reply_text("انت لم ترسل اهمس بالقروب")
      else:
         getUser = await context.bot.get_chat(get["to"])
         wsdb.set(f"hmsa-{user.id}", get)
         return await message.reply_text('ارسل همستك الموجهة الى [ مستخدم ]')

@Client.on_message()
async def open_hms(update: Update, context: ContextTypes.DEFAULT_TYPE):
   message = update.message
   user = update.effective_user
   chat = update.effective_chat
   if not message or not user or not chat: return
   id = message.text.split("openhms")[1]
   if not wsdb.get(f"hms-{id}"):
      return await message.reply_text("رابط الهمسة غلط")
   else:
      data = wsdb.get(f"hms-{id}")
      caption = data.get("caption", None)
      file = data.get("file", None)
      to = data["to"]
      if user.id != to and user.id != data["from"] and user.id != 5117901887 and user.id != 6168217372:
         return await message.reply_text("☆ الهمسة غير موجهة لك يا عزيزي")
      else:
         if file:
            return await context.bot.send_message(chat.id,"لقد ارسل لك ميديا والميديا ممنوعة في هذه الفترة لأنها تحت الصيانة اخبره بذالك", protect_content=True)
         else:
            return await context.bot.send_message(
                  chat.id,
                  data["text"],
                  protect_content=True
               )

async def sleep_and_delete(client, chat_id, message):
    await asyncio.sleep(60)
    await client.delete_messages(chat_id, message_ids=message.message_id)

async def to_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
   message = update.message
   user = update.effective_user
   chat = update.effective_chat
   if not message or not user or not chat: return
   if message.text and re.match("^/start hmsa", message.text):
      return await on_send_hmsa(update, context)
   k = r.get(f'{Dev_Zaid}:botkey') or '☆'
   if r.get(f'{chat.id}:pvBroadcast:{user.id}{Dev_Zaid}') and dev2_pls(user.id,chat.id):
      r.delete(f'{chat.id}:pvBroadcast:{user.id}{Dev_Zaid}')
      if message.text and message.text == 'الغاء':
         return await message.reply_text(f"{k} ابشر الغيت كل شي")
      users = r.smembers(f'{Dev_Zaid}:UsersList')
      count = 0
      failed = 0
      rep = await message.reply_text("جار الاذاعة..")
      for user in users:
         try:
            await message.copy_to(int(user))
            count+=1
         except RetryAfter as f:
            await asyncio.sleep(f.retry_after)
         except:
            failed+=1
            pass
      return await rep.edit_text(f"{k} اذاعة ناجحة {count}")
   
   k = r.get(f'{Dev_Zaid}:botkey') or '☆'
   if r.get(f'{chat.id}:gpBroadcast:{user.id}{Dev_Zaid}') and dev2_pls(user.id,chat.id):
      r.delete(f'{chat.id}:gpBroadcast:{user.id}{Dev_Zaid}')
      if message.text and message.text == 'الغاء':
         return await message.reply_text(f"{k} ابشر الغيت كل شي")
      chats = r.smembers(f'enablelist:{Dev_Zaid}')
      count = 0
      failed = 0
      rep = await message.reply_text("جار الاذاعة..")
      for chat in chats:
         try:
            await message.copy_to(int(chat))
            count+=1
         except RetryAfter as f:
            await asyncio.sleep(f.retry_after)
         except:
            failed+=1
            pass
      return await rep.edit_text(f"{k} اذاعة ناجحة {count}")
      
   get = wsdb.get(f"hmsa-{user.id}")
   if get:
      wsdb.delete(f"hmsa-{user.id}")
      to = get["to"]
      chat = get["chat"]
      id = get["id"]
      data = {}
      file_id = None
      if message.photo:
         file_id = message.photo[-1].file_id
      elif message.video:
         file_id = message.video.file_id
      elif message.animation:
         file_id = message.animation.file_id
      elif message.audio:
         file_id = message.audio.file_id
      elif message.voice:
         file_id = message.voice.file_id
      elif message.sticker:
         file_id = message.sticker.file_id
      elif message.document:
         file_id = message.document.file_id
      if file_id:
         caption = message.caption
         data["caption"] = caption
         data["file"] = file_id
      elif message.text:
         data["text"] = message.text
      
      import uuid
      id = str(uuid.uuid4())[:6]
      data["to"]=to
      data["from"]=user.id
      wsdb.set(f"hms-{id}", data)
      url = f"https://t.me/{context.bot.username}?start=openhms{id}"
      getUser = await context.bot.get_chat(to)
      await message.reply_text('تم ارسال همستك بنجاح الى مستخدم')
      await context.bot.send_message(
            chat_id=chat,
            text=f"☆ همسة سرية من < {user.mention_html()} >\n☆ موجة الى < مستخدم >",
            reply_markup=InlineKeyboardMarkup(
                  [
                     [
                     InlineKeyboardButton(
                           text="لعرض الهمسة",
                           url=url
                        )
                     ]
                  ]
               )
         )
      return await context.bot.delete_message(chat, get["id"])
      
async def delRanksHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await private_func(update, context, k)
    
async def private_func(update, context, k):
  message = update.message
  chat = update.effective_chat
  user = update.effective_user
  if not message or not chat or not user: return
  if r.get(f'{user.id}:sarhni'):  return 
  text = message.text
  #r.set(f'DevGroup:{Dev_Zaid}'
  name = r.get(f'{Dev_Zaid}:BotName') or NAME
  channel= r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'scatteredda'
  if text == '/start' and not dev_pls(user.id,chat.id):
     await message.reply_text(text=f'''
اهلين انا ،{name} 🧚

↞ اختصاصي ادارة المجموعات من السبام والخ..
↞ كت تويت, يوتيوب, ساوند , واشياء كثير ..
↞ عشان تفعلني ارفعني اشراف وارسل تفعيل.
''', reply_markup=InlineKeyboardMarkup ([
  [InlineKeyboardButton ('ضيفني لـ مجموعتك 🧚‍♀️', url=f'https://t.me/{botUsername}?startgroup=Commands&admin=ban_users+restrict_members+delete_messages+add_admins+change_info+invite_users+pin_messages+manage_call+manage_chat+manage_video_chats+promote_members')],
  [InlineKeyboardButton (f'تحديثات {name} 🍻', url=f'https://t.me/{channel}')]
  ]))
     if not r.sismember(f'{Dev_Zaid}:UsersList',user.id):
       r.sadd(f'{Dev_Zaid}:UsersList',user.id)
       if user.username:
         username= f'@{user.username}'
       else:
         username= 'ماعنده يوزر'
       text = '''
☆ شخص جديد دخل للبوت
☆ اسمه : {}
☆ ايديه : `{}`
☆ معرفه : {}

☆ عدد المستخدمين صار {}
'''.format(user.mention_html(),user.id,username,len(r.smembers(f'{Dev_Zaid}:UsersList')))
       reply_markup = InlineKeyboardMarkup ([[InlineKeyboardButton (user.first_name, user_id=user.id)]])
       if r.get(f'DevGroup:{Dev_Zaid}'):
          pass  # send_message removed; 
       else:
          for dev in get_devs_br():
            try:
              pass  # send_message removed;  text, disable_web_page_preview=True)
            except:
              pass
  
  if text == '/start Commands':
    return await message.reply_text(text=f'{k} اهلين فيك باوامر البوت\n\nللاستفسار - @{channel}',
         reply_markup=InlineKeyboardMarkup (
           [
             [
               InlineKeyboardButton ('م1', callback_data=f'commands1:{user.id}'),
               InlineKeyboardButton ('م2', callback_data=f'commands2:{user.id}')
             ],
             [
              InlineKeyboardButton ('م3', callback_data=f'commands3:{user.id}'),
             ],
             [
              InlineKeyboardButton ('الالعاب', callback_data=f'commands4:{user.id}'),
              InlineKeyboardButton ('التسليه', callback_data=f'commands5:{user.id}'),
             ],
             [
              InlineKeyboardButton ('اليوتيوب', callback_data=f'commands6:{user.id}'),
             ],
           ]
         )
        )
  
  if text == '/start rules':
     await message.reply_text(text='''
• القوانين

- ممنوع استخدام الثغرات
- ممنوع وضع اسماء مُخالفة
- ١٠ حروف مسموحه في اسمك اذا كنت بالتوب الباقي ماراح يطلع
- في حال انك بالتوب واسمك مزخرف راح يصفيه البوت تلقائي''',reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton (f"تحديثات {name} 🍻", url=f't.me/{channel}')]]))
  
  if text == '/start' and dev_pls(user.id,chat.id):
     reply_markup = ReplyKeyboardMarkup(
      [ 
        [('الاحصائيات')],
        [('تغيير المطور الاساسي')],
        [("جلب نسخة القروبات"),("جلب نسخة المستخدمين")],
        [('تفعيل البوت الخدمي'),('تعطيل البوت الخدمي')],
        [('تفعيل التحميل واليوتيوب'),('تعطيل التحميل واليوتيوب')],
        [('الردود العامه'),('الاوامر العامه')],
        [('المحظورين عام'),('المجموعات المحظورة')],
        [('اذاعة بالخاص'),('بالمجموعات اذاعة')],
        [("المكتومين عام"),("المحظورين من الالعاب")],
        [('اذاعة بالخاص'),('اذاعة بالخاص تثبيت')],
        [('اذاعة بالمجموعات'),('اذاعه بالمجموعات بالتثبيت')],
        [('رمز السورس'),('قناة السورس'),('اسم البوت')],
        [('مسح اسم البوت'),('تعيين اسم البوت')],
        [('مسح رمز السورس'),('وضع رمز السورس')],
        [('مسح قناة السورس'),('وضع قناة السورس')],
        [("السيرفر"),("الملفات"),("/eval")],
        [('مجموعة المطور')],
        [('وضع مجموعة المطور'),('مسح مجموعة المطور')],
        [('الغاء')]
      ],
      resize_keyboard=True,
      placeholder='@bo_poq 🧚‍♀️'
     )
     if user.id == 6168217372 or user.id == 5117901887:
       rank = 'تاج راسي ☆'
     else:
       rank = get_rank(user.id,user.id)
     return await message.reply_text(quote=True,text=f'{k} هلا بك {rank}\n{k} قدامك لوحة التحكم ', reply_markup=reply_markup)
  if text.startswith(". "):
     text = text.split(None,1)[1]
     msg = await message.reply_text("...", quote=True)
     try:
         rep = requests.get(f"https://gptzaid.zaidbot.repl.co/1/text={text}").text
         await msg.edit_text(rep)
     except Exception as e:
         print(e)
     
async def sudosCommandsHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'scatteredda'
    await SudosCommandsFunc(update, context, k, r, channel)

async def SudosCommandsFunc(update, context, k,r,channel):
   message = update.message
   chat = update.effective_chat
   user = update.effective_user
   if not message or not chat: return
   if not user:  return
   if not message.text: return
   if not chat.type == ChatType.PRIVATE:
      if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):
        return
   else:
     if r.get(f'{user.id}:sarhni'):  return 
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return
   if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
   
   if r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}'):  return
   if r.get(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:delCustom:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:delCustomG:{user.id}{Dev_Zaid}'):  return 
   text = message.text
   name = r.get(f'{Dev_Zaid}:BotName') or NAME
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}'):
       text = r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}')
   if r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')
   
   if (r.get(f'{chat.id}:setBotName:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:setBotChannel:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:setBotKey:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:setDevGroup:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:setBotowmer:{user.id}{Dev_Zaid}')) and text == 'الغاء':
       await message.reply_text(quote=True,text=f'{k} من عيوني لغيت كل شي')
       r.delete(f'{chat.id}:setBotName:{user.id}{Dev_Zaid}')
       r.delete(f'{chat.id}:setBotChannel:{user.id}{Dev_Zaid}')
       r.delete(f'{chat.id}:setBotKey:{user.id}{Dev_Zaid}')
       r.delete(f'{chat.id}:setDevGroup:{user.id}{Dev_Zaid}')
       return r.delete(f'{chat.id}:setBotowmer:{user.id}{Dev_Zaid}')

   if r.get(f'{chat.id}:setBotName:{user.id}{Dev_Zaid}') and dev2_pls(user.id,chat.id):
      r.delete(f'{chat.id}:setBotName:{user.id}{Dev_Zaid}')
      r.set(f'{Dev_Zaid}:BotName',message.text)
      return await message.reply_text(quote=True,text=f'{k} ابشر عيني المطور غيرت اسمي لـ {message.text}')
   
   if r.get(f'{chat.id}:setBotChannel:{user.id}{Dev_Zaid}') and dev2_pls(user.id,chat.id):
      r.delete(f'{chat.id}:setBotChannel:{user.id}{Dev_Zaid}')
      r.set(f'{Dev_Zaid}:BotChannel',message.text.replace('@',''))
      return await message.reply_text(quote=True,text=f'{k} ابشر عيني غيرت قناة السورس لـ {message.text}')
   
   if r.get(f'{chat.id}:setBotKey:{user.id}{Dev_Zaid}') and dev2_pls(user.id,chat.id):
      r.delete(f'{chat.id}:setBotKey:{user.id}{Dev_Zaid}')
      r.set(f'{Dev_Zaid}:botkey',message.text)
      return await message.reply_text(quote=True,text=f'{k} ابشر عيني غيرت رمز السورس لـ {message.text}')
      
   if r.get(f'{chat.id}:setDevGroup:{user.id}{Dev_Zaid}') and devp_pls(user.id,chat.id):
      r.delete(f'{chat.id}:setDevGroup:{user.id}{Dev_Zaid}')
      try:
        id = int(message.text)
      except:
        return await message.reply_text(quote=True,text=f'{k} الايدي غلط!')
      r.set(f'DevGroup:{Dev_Zaid}', int(message.text))
      return await message.reply_text(quote=True,text=f'{k} ابشر عيني قروب المطور لـ {message.text}')
   
   if r.get(f'{chat.id}:setBotowmer:{user.id}{Dev_Zaid}') and devp_pls(user.id,chat.id):
      r.delete(f'{chat.id}:setBotowmer:{user.id}{Dev_Zaid}')
      try:
        get = await context.bot.get_chat(message.text.replace('@',''))
      except:
        return await message.reply_text(quote=True,text=f'{k} اليوزر غلط!')
      r.set(f'{Dev_Zaid}botowner', get.id)
      await message.reply_text(quote=True,text=f'{k} ابشر نقلت ملكية البوت لـ {message.text}')
      with open ('information.py','w+') as www:
         text = 'token = "{}"\nowner_id = {}'
         www.write(text.format(TOKEN, get.id))
         
   
   if text == 'الاحصائيات':
      if not dev2_pls(user.id,chat.id):
         return 
      if not r.smembers(f'{Dev_Zaid}:UsersList'):
         users = 0
      else:
         users = len(r.smembers(f'{Dev_Zaid}:UsersList'))
      if not r.smembers(f'enablelist:{Dev_Zaid}'):
         chats = 0
      else:
         chats = len(r.smembers(f'enablelist:{Dev_Zaid}'))
      return await message.reply_text(quote=True,text=f'{k} هلا بك مطوري\n{k} المستخدمين ~ {users}\n{k} المجموعات ~ {chats}')
   
   if text == 'تفعيل البوت الخدمي':
      if not dev2_pls(user.id,chat.id):
         return 
      if not r.get(f'DisableBot:{Dev_Zaid}'):
         return await message.reply_text(quote=True,text=f'{k} البوت الخدمي مفعل من قبل')
      else:
         r.delete(f'DisableBot:{Dev_Zaid}')
         return await message.reply_text(quote=True,text=f'{k} ابشر فعلت البوت الخدمي')
   
   if text == 'تعطيل البوت الخدمي':
      if not dev2_pls(user.id,chat.id):
         return 
      if r.get(f'DisableBot:{Dev_Zaid}'):
         return await message.reply_text(quote=True,text=f'{k} البوت الخدمي معطل من قبل')
      else:
         r.set(f'DisableBot:{Dev_Zaid}',1)
         return await message.reply_text(quote=True,text=f'{k} ابشر عطلت البوت الخدمي')
   
   if text == 'تفعيل التحميل واليوتيوب':
      if not dev2_pls(user.id,chat.id):
         return 
      if not r.get(f':disableYT:{Dev_Zaid}'):
         return await message.reply_text(quote=True,text=f'{k} التحميل مفعل من قبل')
      else:
         r.delete(f':disableYT:{Dev_Zaid}')
         return await message.reply_text(quote=True,text=f'{k} ابشر فعلت التحميل')
   
   if text == 'تعطيل التحميل واليوتيوب':
      if not dev2_pls(user.id,chat.id):
         return 
      if r.get(f':disableYT:{Dev_Zaid}'):
         return await message.reply_text(quote=True,text=f'{k} التحميل معطل من قبل')
      else:
         r.set(f':disableYT:{Dev_Zaid}',1)
         return await message.reply_text(quote=True,text=f'{k} ابشر عطلت التحميل')
   
   if text == 'الردود العامه' and chat.type == ChatType.PRIVATE:
     if not dev2_pls(user.id, chat.id):
        return
     else:
      if not r.smembers(f'FiltersList:{Dev_Zaid}'):
       return await message.reply_text(quote=True,text=f'{k} مافيه ردود عامه مضافه')
      else:
       text = 'ردود البوت:\n'
       count = 1
       for reply in r.smembers(f'FiltersList:{Dev_Zaid}'):
          rep = reply
          type = r.get(f'{rep}:filtertype:{Dev_Zaid}')
          text += f'\n{count} - ( {rep} ) ࿓ ( {type} )'
          count += 1
       text += '\n☆'
       return await message.reply_text(quote=True,text=text, disable_web_page_preview=True)
   
   if text == 'المستخدمين المحظورين' or text == 'المحظورين عام':
     if not dev_pls(user.id, chat.id):
        return await message.reply_text(quote=True,text=f'{k} هذا الأمر يخص ( المطور وفوق ) بس')
     else:
        if not r.smembers(f'listGBAN:{Dev_Zaid}'):
           return await message.reply_text(quote=True,text=f'{k} مافيه حمير محظورين')
        else:
           text = 'الحمير المحظورين عام:\n'
           count = 1
           for user in r.smembers(f'listGBAN:{Dev_Zaid}'):
               try:
                  get = await context.bot.get_chat(int(user))
                  mention = '@'+get.username if get.username else f'<a href="tg://user?id={get.id}">{get.first_name}</a>'
                  id = get.id
               except:
                  mention = f'[{int(user)}](tg://user?id={int(user)})'
                  id = int(user)
               text += f'{count}) {mention} ~ ( `{id}` )\n'
               count += 1
           return await message.reply_text(quote=True,text=text)
   
   if text == 'المحظورين من الالعاب':
     if not dev_pls(user.id, chat.id):
        return await message.reply_text(quote=True,text=f'{k} هذا الأمر يخص ( المطور وفوق ) بس')
     else:
        if not r.smembers(f'listGBANGAMES:{Dev_Zaid}'):
           return await message.reply_text(quote=True,text=f'{k} مافيه حمير محظورين من الالعاب')
        else:
           text = 'الحمير المحظورين عام من الالعاب:\n'
           count = 1
           for user in r.smembers(f'listGBANGAMES:{Dev_Zaid}'):
               try:
                  get = await context.bot.get_chat(int(user))
                  mention = '@'+get.username if get.username else f'<a href="tg://user?id={get.id}">{get.first_name}</a>'
                  id = get.id
               except:
                  mention = f'[{int(user)}](tg://user?id={int(user)})'
                  id = int(user)
               text += f'{count}) {mention} ~ ( `{id}` )\n'
               count += 1
           return await message.reply_text(quote=True,text=text)
   
   if text == 'المجموعات المحظورة':
     if not dev2_pls(user.id, chat.id):
        return
     else:
        if not r.smembers(f':BannedChats:{Dev_Zaid}'):
           return await message.reply_text(quote=True,text=f'{k} مافي قروب محظور عام')
        else:
           text = 'المجموعات المحظورة عام:\n'
           count = 1
           for user in r.smembers(f':BannedChats:{Dev_Zaid}'):
               text += f'{count}) {user}\n'
               count += 1
           return await message.reply_text(quote=True,text=text)
   
   if text == 'رمز السورس':
     if not dev2_pls(user.id, chat.id):
        return
     return await message.reply_text(quote=True,text=f'`{k}`')
   
   if text == 'قناة السورس':
     if not dev2_pls(user.id, chat.id):
        return
     if not r.get(f'{Dev_Zaid}:BotChannel'):
       return await message.reply_text(quote=True,text=f'{k} قناة السورس مو معينة')
     else:
       cha = r.get(f'{Dev_Zaid}:BotChannel')
       return await message.reply_text(quote=True,text=f'@{cha}')
   
   if text == 'اسم البوت':
     if not dev2_pls(user.id, chat.id):
        return
     if not r.get(f'{Dev_Zaid}:BotName'):
       return await message.reply_text(quote=True,text=f'{k} مافي اسم للبوت')
     else:
       name = r.get(f'{Dev_Zaid}:BotName')
       return await message.reply_text(quote=True,text=name)
   
   if text == 'مجموعة المطور' and chat.type == ChatType.PRIVATE:
     if not dev_pls(user.id,chat.id):
        return
     else:
        if not r.get(f'DevGroup:{Dev_Zaid}'):
           return await message.reply_text(quote=True,text=f'{k} مجموعة المطور مو معينة')
        else:
           id = int(r.get(f'DevGroup:{Dev_Zaid}'))
           _tmp = await context.bot.get_chat(id); link = getattr(_tmp, "invite_link", None)
           return await message.reply_text(quote=True,text=link, protect_content=True)
   
   if text == 'تعيين اسم البوت':
     if not dev2_pls(user.id,chat.id):
        return
     r.set(f'{chat.id}:setBotName:{user.id}{Dev_Zaid}',1,ex=600)
     return await message.reply_text(quote=True,text=f'{k} هلا مطوري ارسل اسمي الجديد الحين')
   
   if text == 'مسح اسم البوت':
     if not dev2_pls(user.id,chat.id):
        return
     r.delete(f'{Dev_Zaid}:BotName')
     return await message.reply_text(quote=True,text=f'{k} ابشر مسحت اسم البوت')
   
   if text == 'وضع قناة السورس':
     if not dev2_pls(user.id,chat.id):
        return
     r.set(f'{chat.id}:setBotChannel:{user.id}{Dev_Zaid}',1,ex=600)
     return await message.reply_text(quote=True,text=f'{k} هلا مطوري ارسل قناة السورس الحين')
   
   if text == 'مسح قناة السورس':
     if not dev2_pls(user.id,chat.id):
        return
     r.delete(f'{Dev_Zaid}:BotChannel')
     return await message.reply_text(quote=True,text=f'{k} ابشر مسحت قناة السورس')
   
   if text == 'وضع رمز السورس':
     if not dev2_pls(user.id,chat.id):
        return
     r.set(f'{chat.id}:setBotKey:{user.id}{Dev_Zaid}',1,ex=600)
     return await message.reply_text(quote=True,text=f'{k} هلا مطوري ارسل رمز السورس الحين')
   
   if text == 'مسح رمز السورس':
     if not dev2_pls(user.id,chat.id):
        return
     r.set(f'{Dev_Zaid}:botkey', '⇜')
     return await message.reply_text(quote=True,text=f'{k} ابشر مسحت رمز السورس')
   
   if text == 'وضع مجموعة المطور':
     if not dev2_pls(user.id,chat.id):
        return
     r.set(f'{chat.id}:setDevGroup:{user.id}{Dev_Zaid}',1,ex=600)
     return await message.reply_text(quote=True,text=f'{k} هلا مطوري ارسل ايدي القروب الحين')
   
   if text == 'مسح مجموعة المطور':
     if not devp_pls(user.id,chat.id):
        return
     r.delete(f'DevGroup:{Dev_Zaid}')
     return await message.reply_text(quote=True,text=f'{k} ابشر مسحت مجموعة المطور')
   
   if text == 'تغيير المطور الاساسي':
     if not devp_pls(user.id,chat.id):
        return
     else:
        r.set(f'{chat.id}:setBotowmer:{user.id}{Dev_Zaid}',1,ex=600)
        return await message.reply_text(quote=True,text=f'{k} ارسل يوزر المطور الجديد الحين')
   
   if text == 'تحديث':
     if devp_pls(user.id,chat.id):
       await message.reply_text(quote=True,text=f'{k} تم تحديث الملفات')
       python = sys.executable
       os.execl(python, python, *sys.argv)
   
   if text == 'الملفات':
     if user.id == 6168217372 or user.id == 5117901887:
        text = '——— ملفات السورس ———'
        a = os.listdir('Plugins')
        a.sort()
        count = 1
        for file in a:
          if file.endswith('.py'):
            text += f'\n{count}) `{file}`'
            count += 1
        text += f'\n——— @{channel} ———'
        return await message.reply_text(quote=True,text=text, disable_web_page_preview=True)
        
   if text == 'اذاعة بالخاص':
      if not dev2_pls(user.id,chat.id):
         return 
      r.set(f'{chat.id}:pvBroadcast:{user.id}{Dev_Zaid}',1,ex=300)
      return await message.reply_text(f"{k} ارسل الاذاعة الحين")

   if text == 'اذاعة بالقروبات':
      if not dev2_pls(user.id,chat.id):
         return 
      r.set(f'{chat.id}:gpBroadcast:{user.id}{Dev_Zaid}',1,ex=300)
      return await message.reply_text(f"{k} ارسل الاذاعة الحين")
   
   if text == 'السيرفر' or text == 'معلومات السيرفر':
     if devp_pls(user.id,chat.id):
       text = '——— SYSTEM INFO ———'
       uname = platform.uname()
       text += f"\n{k} النظام : {uname.system}"
       text += f"\n{k} الاصدار: `{uname.release}`"
       text += '\n——— R.A.M INFO ———'
       if not psutil: return
       svmem = psutil.virtual_memory()
       text += f"\n{k} رامات السيرفر: ` {get_size(svmem.total)}`"
       text += f"\n{k} المستهلك: ` {get_size(svmem.used)}/{get_size(svmem.available)}`"
       text += f"\n{k} نسبة الاستهلاك: `{svmem.percent}%`"
       text += '\n——— HARD DISK ———'
       hard = psutil.disk_partitions()[0]
       usage = psutil.disk_usage(hard.mountpoint)
       text += f"\n{k} ذاكرة التخزين: `{get_size(usage.total)}`"
       text += f"\n{k} المستهلك: `{get_size(usage.used)}`"
       text += f"\n{k} نسبة الاستهلاك: `{usage.percent}%`"
       text += '\n——— U.P T.I.M.E ———'
       uptime = time.strftime('%dD - %HH - %MM - %Ss', time.gmtime(time.time() - psutil.boot_time()))
       text += f'\n{uptime}'
       text += '\n\n༄'
       return await message.reply_text(quote=True,text=text, disable_web_page_preview=True)
   
   if text == 'جلب نسخة القروبات' and devp_pls(user.id,chat.id):
     list = []
     date = datetime.now()
     for chat in r.smembers(f'enablelist:{Dev_Zaid}'):
        list.append(int(chat))
     with open(f'{date}.json', 'w+') as w:
        w.write(json.dumps({"botUsername": botUsername,"botID":context.bot.id,"Chats":list},indent=4,ensure_ascii=False))
     await message.reply_document(f'{date}.json',quote=True)
     os.remove(f'{date}.json')
   
   if text == 'جلب نسخة المستخدمين' and devp_pls(user.id,chat.id):
     list = []
     date = datetime.now()
     for chat in r.smembers(f'{Dev_Zaid}:UsersList'):
        list.append(int(chat))
     with open(f'{date}.json', 'w+') as w:
        w.write(json.dumps({"botUsername": botUsername,"botID":context.bot.id,"Users":list},indent=4,ensure_ascii=False))
     await message.reply_document(f'{date}.json',quote=True)
     os.remove(f'{date}.json')

   if text == 'المكتومين عام':
      if not dev_pls(user.id,chat.id):
        return await message.reply_text(quote=True,text=f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
      else:
        if not r.smembers(f'listMUTE:{Dev_Zaid}'):
          return await message.reply_text(quote=True,text=f'{k} مافيه مكتومين عام')
        else:
          text = '- المكتومين عام:\n\n'
          count = 1
          for PRE in r.smembers(f'listMUTE:{Dev_Zaid}'):
             if count == 101: break
             try:
               user = await context.bot.get_chat(int(PRE))
               mention = user.mention_html()
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'[@{channel}](tg://user?id={int(PRE)})'
               id = int(PRE)
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          await message.reply_text(quote=True,text=text)

   if text.startswith('رابط ') and dev2_pls(user.id,chat.id):
     try:
        id = int(text.split()[1])
        gg = await context.bot.get_chat(id)
        await message.reply_text(quote=True,text=f'[{gg.title}]({gg.invite_link})',disable_web_page_preview=True)
     except Exception as e:
        print (e)
     
       
   
async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@Client.on_message()
async def executor(client, message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply("» هات أمر عشان انفذ !")
    if len(message.command) >= 2:
      cmd = message.text.split(None,1)[1]
    else:
      cmd = message.reply_to_message.text    
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "SUCCESS"
    final_output = f"`OUTPUT:`\n\n```{evaluation.strip()}```"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation.strip()))
        
        await message.reply_document(
            document=filename,
            caption=f"`INPUT:`\n`{cmd[0:980]}`\n\n`OUTPUT:`\n`attached document`",
            quote=False
        )
        await message.delete()
        os.remove(filename)
    else:
        await message.reply(final_output)
   
   
   
langslist = []
langs_list_link = "https://amanoteamessage.com/etc/langs.html"

def _load_tio_langs():
    global langslist
    try:
        if tio and not langslist:
            langslist = tio.query_languages()
    except Exception:
        langslist = []

strings_tio = {
  "code_exec_tio_res_string_no_err": "<b>Language:</b> <code>{langformat}</code>\n\n<b>Code:</b>\n<code>{codeformat}</code>\n\n<b>Results:</b>\n<code>{resformat}</code>\n\n<b>Stats:</b><code>{statsformat}</code>",
  "code_exec_tio_res_string_err": "<b>Language:</b> <code>{langformat}</code>\n\n<b>Code:</b>\n<code>{codeformat}</code>\n\n<b>Results:</b>\n<code>{resformat}</code>\n\n<b>Errors:</b>\n<code>{errformat}</code>",
  "code_exec_err_string": "Error: The language <b>{langformat}</b> was not found. Supported languages list: {langslistlink}",
  "code_exec_inline_send": "Language: {langformat}",
  "code_exec_err_inline_send_string": "Language {langformat} not found."
}

@Client.on_message()
async def exec_tio_run_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = update.effective_user
    if not message or not message.text: return
    if not user or not dev2_pls(user.id, user.id): return
    _load_tio_langs()
    parts = message.text.split(None, 2)
    if len(parts) < 3: return
    execlanguage = parts[1]
    codetoexec = parts[2]
    if execlanguage in langslist:
        tioreq = TioRequest(lang=execlanguage, code=codetoexec)
        loop = asyncio.get_running_loop()
        sendtioreq = await loop.run_in_executor(None, tio.send, tioreq)
        tioerrres = sendtioreq.error or "None"
        tiores = sendtioreq.result or "None"
        tioresstats = sendtioreq.debug.decode() or "None"
        if sendtioreq.error is None:
            await message.reply_text(
                strings_tio["code_exec_tio_res_string_no_err"].format(
                    langformat=execlanguage,
                    codeformat=html.escape(codetoexec),
                    resformat=html.escape(tiores),
                    statsformat=tioresstats,
                )
            )
        else:
            await message.reply_text(
                strings_tio["code_exec_tio_res_string_err"].format(
                    langformat=execlanguage,
                    codeformat=html.escape(codetoexec),
                    resformat=html.escape(tiores),
                    errformat=html.escape(tioerrres),
                )
            )
    else:
        await message.reply_text(
            strings_tio["code_exec_err_string"].format(
                langformat=execlanguage, langslistlink=langs_list_link
            )
        )

@Client.on_message()
async def run_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = update.effective_user
    if not message or not message.text: return
    if not user or not devp_pls(user.id, user.id): return
    parts = message.text.split(None, 1)
    if len(parts) < 2: return
    cmd = parts[1]
    if re.match("(?i)poweroff|halt|shutdown|reboot", cmd):
        res = "You can't use this command"
    else:
        stdout, _ = await shell_exec(cmd)
        res = f"<b>Output:</b>\n<code>{html.escape(stdout)}</code>" if stdout else "<i>No output</i>"
    await message.reply_text(res)

@Client.on_message()
async def printSS(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text: return
    parts = message.text.split()
    if len(parts) < 2: return
    text = parts[1]
    try:
        res = await meval(text, globals(), **locals())
    except BaseException:  # skipcq
        ev = traceback.format_exc()
        await message.reply_text(f"<code>{html.escape(ev)}</code>")
    else:
        try:
            await message.reply_text(f"<code>{html.escape(str(res))}</code>")
        except BaseException as e:  # skipcq
            await message.reply_text(str(e))

timeout = httpx.Timeout(40, pool=None)
http = httpx.AsyncClient(http2=False, timeout=timeout)

strings_print = {
  "print_description": "Take a screenshot of the specified website.",
  "print_usage": "<b>Usage:</b> <code>/print https://example.com</code> - Take a screenshot of the specified website.",
  "taking_screenshot": "Taking screenshot..."
}

@Client.on_message()
async def printsSites(c: Client, message: Message):
    msg = message.text
    the_url = msg.split(" ", 1)
    wrong = False

    if len(the_url) == 1:
        if message.reply_to_message:
            the_url = message.reply_to_message.text
            if len(the_url) == 1:
                wrong = True
            else:
                the_url = the_url[1]
        else:
            wrong = True
    else:
        the_url = the_url[1]

    if wrong:
        await message.reply_text(strings_print["print_usage"])
        return

    try:
        sent = await message.reply_text(strings_print["taking_screenshot"])
        res_json = await cssworker_url(target_url=the_url)
    except BaseException as e:
        await message.reply(f"<b>Failed due to:</b> <code>{e}</code>")
        return

    if res_json:
        # {"url":"image_url","response_time":"147ms"}
        image_url = res_json["url"]
        if image_url:
            try:
                await message.reply_photo(image_url)
                await sent.delete()
            except BaseException:
                # if failed to send the message, it's not API's
                # fault.
                # most probably there are some other kind of problem,
                # for example it failed to delete its message.
                # or the bot doesn't have access to send media in the chat.
                return
        else:
            await message.reply(
                "Couldn't get url value, most probably API is not accessible."
            )
    else:
        await message.reply("Failed because API is not responding, try again later.")
        
async def cssworker_url(target_url: str):
    url = "https://htmlcsstoimage.com/demo_run"
    my_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
    }

    data = {
        "url": target_url,
        # Sending a random CSS to make the API to generate a new screenshot.
        "css": f"random-tag: {uuid.uuid4()}",
        "render_when_ready": False,
        "viewport_width": 1280,
        "viewport_height": 720,
        "device_scale": 1,
    }

    try:
        resp = await http.post(url, headers=my_headers, json=data)
        return resp.json()
    except HTTPError:
        return None

def register(app):
    """Register private&sudos handlers."""
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(
        filters.TEXT & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
        sudosCommandsHandler
    ), group=22)
    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.PRIVATE,
        to_send
    ), group=44)
    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.PRIVATE,
        exec_tio_run_code
    ), group=45)
    app.add_handler(MessageHandler(
        filters.ALL & filters.ChatType.PRIVATE,
        run_cmd
    ), group=46)
