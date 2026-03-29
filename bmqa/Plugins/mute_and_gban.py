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
import random, re, time




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


async def mutesHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await mute_func(update, context, k)
    
    
async def mute_func(update, context, k):
   message = update.message
   chat = update.effective_chat
   user = update.effective_user
   if not message or not chat or not user:
       return
   if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return 
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:delCustom:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:delCustomG:{user.id}{Dev_Zaid}'):  return 
   text = message.text or ''
   name = r.get(f'{Dev_Zaid}:BotName') or NAME
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}'):
       text = r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}')
   if r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')
   
   if isLockCommand(user.id, chat.id, text): return

   if text == 'كتم' and message.reply_to_message and message.reply_to_message.from_user:
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if not mod_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الامر يخص ( المدير وفوق ) بس')
        if id == user.id:
           return await message.reply_text('شفيك تبي تنزل نفسك')
        if pre_pls(id, chat.id):
           rank = get_rank(id,chat.id)
           return await message.reply_text(f'{k} هييه مايمديك تكتم {rank} يورع!')
        if r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مكتوم من قبل\n☆')
        else:
          r.set(f'{id}:mute:{chat.id}{Dev_Zaid}', 1)
          r.sadd(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} كتمته\n☆')
   
   if re.match("^كتم عام (.*?)$", text) and len(text.split()) ==  3:
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not dev_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الامر يخص ( المطور وفوق ) بس')      
      user = text.split()[2]
      try:
        id = int(user)
      except:
        id = user.replace('@','')
      try:
         get = None
         mention = f'[{get.first_name}](tg://user?id={get.id})'
         id = get.id
      except:
         return await message.reply_text(f'{k} مافيه يوزر كذا')
      if dev_pls(id, chat.id):
         rank = get_rank(id,chat.id)
         return await message.reply_text(f'{k} هييه مايمديك تكتم {rank} يورع!')
      if r.get(f'{id}:mute:{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مكتوم عام من قبل\n☆')
      else:
          r.set(f'{id}:mute:{Dev_Zaid}', 1)
          r.sadd(f'listMUTE:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} كتمته عام\n☆')

   if re.match("^كتم (.*?)$", text) and len(text.split()) == 2:
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not admin_pls(user.id,chat.id):
         return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
      user = text.split()[1]
      try:
        id = int(user)
      except:
        id = user.replace('@','')
      try:
         get = None
         mention = f'[{get.first_name}](tg://user?id={get.id})'
         id = get.id
      except:
         return await message.reply_text(f'{k} مافيه يوزر كذا')
      if id == user.id:
        return await message.reply_text('شفيك تبي تنزل نفسك')
      if r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
         return await message.reply_text(f'「 {mention} 」\n{k} مكتوم من قبل\n☆')
      if pre_pls(id, chat.id):
         rank = get_rank(id,chat.id)
         return await message.reply_text(f'{k} هييه مايمديك تكتم {rank} يورع!')
      r.set(f'{id}:mute:{chat.id}{Dev_Zaid}', 1)
      r.sadd(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
      return await message.reply_text(f'「 {mention} 」\n{k} كتمته\n☆')
   
   if text == 'الغاء الكتم' and message.reply_to_message and message.reply_to_message.from_user:
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if not admin_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
        if not r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو مكتوم قبل\n☆')
        else:
          r.delete(f'{id}:mute:{chat.id}{Dev_Zaid}')
          r.srem(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} ابشر الغيت كتمه\n༄')
   
   if re.match("^الغاء الكتم العام (.*?)$", text) and len(text.split()) ==  4:
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not dev_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
      user = text.split()[3]
      try:
        id = int(user)
      except:
        id = user.replace('@','')
      try:
         get = None
         mention = f'[{get.first_name}](tg://user?id={get.id})'
         id = get.id
      except:
         id = re.findall('[0-9]+', text)[0] if re.findall('[0-9]+', text) else None
         if not id:  return await message.reply_text(f"{k} مافيه مستخدم كذا")
         mention = f'[{id}](tg://user?id={id})'
      if not r.get(f'{id}:mute:{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو مكتوم عام من قبل\n☆')
      else:
          r.delete(f'{id}:mute:{Dev_Zaid}')
          r.srem(f'listMUTE:{Dev_Zaid}',id)
          return await message.reply_text(f'「 {mention} 」\n{k} لغيت كتمته عام\n☆')

   if re.match("^الغاء الكتم (.*?)$", text) and len(text.split()) ==  3:
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not mod_pls(user.id,chat.id):
         return await message.reply_text(f'{k} هذا الامر يخص ( المدير وفوق ) بس')
      user = text.split()[2]
      try:
        id = int(user)
      except:
        id = user.replace('@','')
      try:
         get = None
         mention = f'[{get.first_name}](tg://user?id={get.id})'
         id = get.id
      except:
         id = re.findall('[0-9]+', text)[0] if re.findall('[0-9]+', text) else None
         if not id:  return await message.reply_text(f"{k} مافيه مستخدم كذا")
         mention = f'[{id}](tg://user?id={id})'
      if not r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
         return await message.reply_text(f'「 {mention} 」\n{k} مو مكتوم من قبل\n☆')
      r.delete(f'{id}:mute:{chat.id}{Dev_Zaid}')
      r.srem(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
      return await message.reply_text(f'「 {mention} 」\n{k} أبشر الغيت كتمه\n☆')
   
   if re.match("^حظر عام (.*?)$", text) and len(text.split()) ==  3:
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not dev_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الامر يخص ( المطور وفوق ) بس')      
      user = text.split()[2]
      try:
        id = int(user)
      except:
        id = user.replace('@','')
      try:
         get = None
         mention = f'[{get.first_name}](tg://user?id={get.id})'
         id = get.id
      except:
         return await message.reply_text(f'{k} مافيه يوزر كذا')
      if dev_pls(id, chat.id):
         rank = get_rank(id,chat.id)
         return await message.reply_text(f'{k} هييه مايمديك تحظر {rank} يورع!')
      if r.get(f'{id}:gban:{Dev_Zaid}'):
          return await message.reply_text(f'{k} الحمار「 {mention} 」\n{k} محظور عام من قبل\n☆')
      else:
          r.set(f'{id}:gban:{Dev_Zaid}', 1)
          r.sadd(f'listGBAN:{Dev_Zaid}', id)
          return await message.reply_text(f'{k} الحمار「 {mention} 」\n{k} حظرته عام\n☆')
   
   if re.match("^حظر عام من الالعاب (.*?)$", text) and len(text.split()) ==  5:
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not dev_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
      user = text.split()[4]
      try:
        id = int(user)
      except:
        id = user.replace('@','')
      try:
         get = None
         mention = f'[{get.first_name}](tg://user?id={get.id})'
         id = get.id
      except:
         return await message.reply_text(f'{k} مافيه يوزر كذا')
      if dev_pls(id, chat.id):
         rank = get_rank(id,chat.id)
         return await message.reply_text(f'{k} هييه مايمديك تحظر {rank} يورع!')
      if r.get(f'{id}:gbangames:{Dev_Zaid}'):
          return await message.reply_text(f'{k} الحمار「 {mention} 」\n{k} محظور من الالعاب من قبل\n☆')
      else:
          r.set(f'{id}:gbangames:{Dev_Zaid}', 1)
          r.sadd(f'listGBANGAMES:{Dev_Zaid}', id)
          r.delete(f'{id}:Floos')
          r.srem("BankList",id)
          return await message.reply_text(f'{k} الحمار「 {mention} 」\n{k} حظرته عام من الالعاب\n☆')
   
   if re.match("^الغاء الحظر العام من الالعاب (.*?)$", text) and len(text.split()) ==  6:
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not dev_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
      user = text.split()[5]
      try:
        id = int(user)
      except:
        id = user.replace('@','')
      try:
         get = None
         mention = f'[{get.first_name}](tg://user?id={get.id})'
         id = get.id
      except:
         id = re.findall('[0-9]+', text)[0] if re.findall('[0-9]+', text) else None
         if not id:  return await message.reply_text(f"{k} مافيه مستخدم كذا")
         mention = f'[{id}](tg://user?id={id})'
      if not r.get(f'{id}:gbangames:{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو محظور من الالعاب من قبل\n☆')
      else:
          r.delete(f'{id}:gbangames:{Dev_Zaid}')
          r.srem(f'listGBANGAMES:{Dev_Zaid}',id)
          return await message.reply_text(f'「 {mention} 」\n{k} لغيت حظره من الالعاب عام\n☆')

   if re.match("^الغاء الحظر العام (.*?)$", text) and len(text.split()) ==  4:
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not dev_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
      user = text.split()[3]
      try:
        id = int(user)
      except:
        id = user.replace('@','')
      try:
         get = None
         mention = f'[{get.first_name}](tg://user?id={get.id})'
         id = get.id
      except:
         id = re.findall('[0-9]+', text)[0] if re.findall('[0-9]+', text) else None
         if not id:  return await message.reply_text(f"{k} مافيه مستخدم كذا")
         mention = f'[{id}](tg://user?id={id})'
      if not r.get(f'{id}:gban:{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو محظور عام من قبل\n☆')
      else:
          r.delete(f'{id}:gban:{Dev_Zaid}')
          r.srem(f'listGBAN:{Dev_Zaid}',id)
          return await message.reply_text(f'「 {mention} 」\n{k} لغيت حظره عام\n☆')

async def muteResponse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await del_formutes(update, context)
    
async def del_formutes(update: Update, context: ContextTypes.DEFAULT_TYPE):
   message = update.message
   chat = update.effective_chat
   user = update.effective_user
   if not message or not chat or not user:
       return
   if r.get(f'{user.id}:gban:{Dev_Zaid}'):
     try:
        await context.bot.ban_chat_member(chat.id, user.id)
     except:
        try: await message.delete()
        except: pass
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}') or r.get(f'{user.id}:mute:{Dev_Zaid}'):
     try:
       await message.delete()
     except Exception:
       pass




async def mutesHandlerG(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await mute_funcg(update, context, k)
    
    
async def mute_funcg(update, context, k):
   message = update.message
   chat = update.effective_chat
   user = update.effective_user
   if not message or not chat or not user:
       return
   if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return 
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:delCustom:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:delCustomG:{user.id}{Dev_Zaid}'):  return 
   text = message.text or ''
   name = r.get(f'{Dev_Zaid}:BotName') or NAME
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}'):
       text = r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}')
   if r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')
       
   if text == 'كتم عام' and message.reply_to_message and message.reply_to_message.from_user:
        if not dev_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if dev_pls(id, chat.id):
           rank = get_rank(id,chat.id)
           return await message.reply_text(f'{k} هييه مايمديك تكتم {rank} يورع!')
        if r.get(f'{id}:mute:{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مكتوم عام من قبل\n☆')
        else:
          r.set(f'{id}:mute:{Dev_Zaid}', 1)
          r.sadd(f'listMUTE:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} كتمته عام\n☆')
      
   if text == 'حظر عام' and message.reply_to_message and message.reply_to_message.from_user:
        if not dev_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if dev_pls(id, chat.id):
           rank = get_rank(id,chat.id)
           return await message.reply_text(f'{k} هييه مايمديك تحظر {rank} يورع!')
        if r.get(f'{id}:gban:{Dev_Zaid}'):
          return await message.reply_text(f'{k} الحمار「 {mention} 」\n{k} محظور عام من قبل\n☆')
        else:
          r.set(f'{id}:gban:{Dev_Zaid}', 1)
          r.sadd(f'listGBAN:{Dev_Zaid}', id)
          return await message.reply_text(f'{k} الحمار「 {mention} 」\n{k} حظرته عام\n☆')
   
   if text == 'حظر عام من الالعاب' and message.reply_to_message and message.reply_to_message.from_user:
        if not dev_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص ( المطور وفوق ) بس')
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if dev_pls(id, chat.id):
           rank = get_rank(id,chat.id)
           return await message.reply_text(f'{k} هييه مايمديك تحظر {rank} يورع!')
        if r.get(f'{id}:gbangames:{Dev_Zaid}'):
          return await message.reply_text(f'{k} الحمار「 {mention} 」\n{k} محظور من الالعاب من قبل\n☆')
        else:
          r.set(f'{id}:gbangames:{Dev_Zaid}', 1)
          r.sadd(f'listGBANGAMES:{Dev_Zaid}', id)
          r.delete(f'{id}:Floos')
          r.srem("BankList",id)
          return await message.reply_text(f'{k} الحمار「 {mention} 」\n{k} حظرته عام من الالعاب\n☆')

   if text == 'الغاء الكتم العام' and message.reply_to_message and message.reply_to_message.from_user:
        if not dev_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص ( المطور وفوق ) بس')
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if dev_pls(id, chat.id):
           rank = get_rank(id,chat.id)
           return await message.reply_text(f'{k} هييه مايمديك تكتم {rank} يورع!')
        if not r.get(f'{id}:mute:{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو مكتوم عام من قبل\n☆')
        else:
          r.delete(f'{id}:mute:{Dev_Zaid}')
          r.srem(f'listMUTE:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} لغيت كتمته عام\n☆')
   
   if text == 'الغاء الحظر العام من الالعاب' and message.reply_to_message and message.reply_to_message.from_user:
        if not dev_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if dev_pls(id, chat.id):
           rank = get_rank(id,chat.id)
           return await message.reply_text(f'{k} هييه مايمديك تكتم {rank} يورع!')
        if not r.get(f'{id}:gbangames:{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو محظور من الالعاب من قبل\n☆')
        else:
          r.delete(f'{id}:gbangames:{Dev_Zaid}')
          r.srem(f'listGBANGAMES:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} لغيت حظره من الالعاب\n☆')

   if text == 'الغاء الحظر العام' and message.reply_to_message and message.reply_to_message.from_user:
        if not dev_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if dev_pls(id, chat.id):
           rank = get_rank(id,chat.id)
           return await message.reply_text(f'{k} هييه مايمديك تكتم {rank} يورع!')
        if not r.get(f'{id}:gban:{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو محظور عام من قبل\n☆')
        else:
          r.delete(f'{id}:gban:{Dev_Zaid}')
          r.srem(f'listGBAN:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} لغيت حظره عام\n☆')
   

def register(app):
    """Register mute_and_gban handlers."""
    from telegram.ext import MessageHandler, CallbackQueryHandler, filters
    app.add_handler(MessageHandler(
        filters.ALL & filters.ChatType.GROUPS,
        mutesHandler
    ), group=6)
    app.add_handler(MessageHandler(
        filters.ALL & filters.ChatType.GROUPS,
        mutesHandlerG
    ), group=26)
    app.add_handler(CallbackQueryHandler(muteResponse, pattern=r'^muteK'))
    app.add_handler(CallbackQueryHandler(del_formutes, pattern=r'^delMute'))
