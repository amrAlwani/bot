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


async def addCustomReplyG(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await addreplyg(update, context, k)
    
async def addreplyg(update, context, k):
    
  message = update.message
    
  chat = update.effective_chat
    
  user = update.effective_user
  if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):  return
  if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return 
  if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
  if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
  if r.get(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}'):  return    
  if r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}'):  return
  if r.get(f'{chat.id}:delCustom:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:delCustomG:{user.id}{Dev_Zaid}'):  return 
  if message.text:
   text = message.text
   name = r.get(f'{Dev_Zaid}:BotName') or NAME
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}'):
       text = r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}')
   if r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')
   
   if r.get(f'{chat.id}:addFilterG:{user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{chat.id}:addFilterG:{user.id}{Dev_Zaid}')
     await message.reply_text(f'{k} من عيوني لغيت اضافة الرد العام')
     return 
   
   if r.get(f'{chat.id}:delFilterG:{user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{chat.id}:delFilterG:{user.id}{Dev_Zaid}')
     await message.reply_text(f'{k} من عيوني لغيت مسح الرد العام')
     return 
   
   if message.text == 'الغاء' and r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}'):
       r.delete(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
       await message.reply_text(f'{k} من عيوني لغيت اضافة الرد العام')

   if r.get(f'{chat.id}:delFilterG:{user.id}{Dev_Zaid}') and dev2_pls(user.id,chat.id):
      if not r.get(f'{message.text}:filterInfo:{Dev_Zaid}'):
        r.delete(f'{chat.id}:delFilterG:{user.id}{Dev_Zaid}')
        return await message.reply_text(f'{k} هذا الرد مو مضاف في قائمة الردود العامه')
      else:
           r.delete(f'{message.text}:filter:{Dev_Zaid}')
           r.delete(f'{message.text}:filtertype:{Dev_Zaid}')
           r.delete(f'{message.text}:filterInfo:{Dev_Zaid}')
           r.srem(f'FiltersList:{Dev_Zaid}', message.text)
           r.delete(f'{chat.id}:delFilterG:{user.id}{Dev_Zaid}')
           return await message.reply_text(f'( {message.text} )\n{k} وحذفنا الرد ياحلو')   

   
   if text == 'تعطيل ردود المطور':
     if not owner_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المالك وفوق ) بس')
     if r.get(f'{chat.id}:lock_global:{Dev_Zaid}'):
        return await message.reply_text(f'{k} من「 {user.mention_html()} 」\n{k} ردود المطور معطله من قبل\n☆',parse_mode=ParseMode.HTML)
     else:
        r.set(f'{chat.id}:lock_global:{Dev_Zaid}',1)
        return await message.reply_text(f'{k} من「 {user.mention_html()} 」\n{k} ابشر عطلت ردود المطور\n☆',parse_mode=ParseMode.HTML)
   
   if text == 'تفعيل ردود المطور':
     if not owner_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المالك وفوق ) بس')
     if not r.get(f'{chat.id}:lock_global:{Dev_Zaid}'):
        return await message.reply_text(f'{k} من「 {user.mention_html()} 」\n{k} ردود المطور مفعله من قبل\n☆',parse_mode=ParseMode.HTML)
     else:
        r.delete(f'{chat.id}:lock_global:{Dev_Zaid}')
        return await message.reply_text(f'{k} من「 {user.mention_html()} 」\n{k} ابشر فعلت ردود المطور\n☆',parse_mode=ParseMode.HTML)
   
   if text == 'الردود العامه':
     if not dev2_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
     else:
      if not r.smembers(f'FiltersList:{Dev_Zaid}'):
       return await message.reply_text(f'{k} مافيه ردود عامه مضافه')
      else:
       text = 'ردود البوت:\n'
       count = 1
       for reply in r.smembers(f'FiltersList:{Dev_Zaid}'):
          rep = reply
          type = r.get(f'{rep}:filtertype:{Dev_Zaid}')
          text += f'\n{count} - ( {rep} ) ࿓ ( {type} )'
          count += 1
       text += '\n☆'
       return await message.reply_text(text, disable_web_page_preview=True,parse_mode=ParseMode.HTML)
  
   if text == 'مسح الردود العامه':
     if not dev2_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
     else:
      if not r.smembers(f'FiltersList:{Dev_Zaid}'):
        return await message.reply_text(f'{k} مافيه ردود عامه مضافه')
      else:
        total = 0
        for reply in r.smembers(f'FiltersList:{Dev_Zaid}'):
           rep = reply
           r.delete(f'{rep}:filter:{Dev_Zaid}')
           r.delete(f'{rep}:filtertype:{Dev_Zaid}')
           r.delete(f'{rep}:filterInfo:{Dev_Zaid}')
           r.srem(f'FiltersList:{Dev_Zaid}', rep)
           total += 1
        return await message.reply_text(f'{k} ابشر مسحت ( {total} ) من الردود العامه')   
     
   if text == 'مسح رد عام':
     if not r.get(f'{chat.id}:delFilterG:{user.id}{Dev_Zaid}'):
      if not dev2_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
      else:
        r.set(f'{chat.id}:delFilterG:{user.id}{Dev_Zaid}',1)
        await message.reply_text(f'{k} تمام عيني\n{k} الحين ارسل الرد عشان امسحه\n☆',parse_mode=ParseMode.HTML)
        return 
   
   if text == 'اضف رد عام':
       if not r.get(f'{chat.id}:addFilterG:{user.id}{Dev_Zaid}'):
         if not dev2_pls(user.id, chat.id):
           return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
         else:
           await message.reply_text(f'{k} حلو ، الحين ارسل الكلمة اللي تبيها')
           r.set(f'{chat.id}:addFilterG:{user.id}{Dev_Zaid}',1)
           return 
   
   if r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}') and dev2_pls(user.id, chat.id):
       text = r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
       r.set(f'{text}:filter:{Dev_Zaid}', f'type=text&text={message.text.html}')
       r.set(f'{text}:filtertype:{Dev_Zaid}','نص')
       r.set(f'{text}:filterInfo:{Dev_Zaid}', f'by={user.id}')
       r.sadd(f'FiltersList:{Dev_Zaid}', f'{text}')
       r.delete(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
       return await message.reply_text(f'( {text} )\nواضفنا الرد ياحلو\n☆',parse_mode=ParseMode.HTML)
     
   if r.get(f'{chat.id}:addFilterG:{user.id}{Dev_Zaid}') and dev2_pls(user.id,chat.id):
      r.set(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}', message.text)
      r.delete(f'{chat.id}:addFilterG:{user.id}{Dev_Zaid}')
      await message.reply_text(f'{k} حلو الحين ارسل جواب الرد\n{k} ( نص,صوره,فيديو,متحركه,بصمه,صوت,ملف )\nـــــــــــــــــــــــــــــــــــــــــ\n`<USER_ID>` › آيدي المستخدم\n`<USER_NAME>` › اسم المستخدم\n`<USER_USERNAME>` › يوزر المستخدم\n`<USER_MENTION>` › رابط حساب المستخدم\n༄',parse_mode=ParseMode.MARKDOWN)
      return 
  
  await addreply_media(update, context, k)

async def addreply_media(update, context, k):

   message = update.message

   chat = update.effective_chat

   user = update.effective_user
   if message.photo and r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}') and dev2_pls(user.id, chat.id):
      type = 'photo'
      photo = message.photo[-1].file_id
      if message.caption:
        caption = message.caption_html
      else:
        caption = 'None'
      text = r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
      r.set(f'{text}:filter:{Dev_Zaid}', f'type={type}&photo={photo}&caption={caption}')
      r.set(f'{text}:filtertype:{Dev_Zaid}','صوره')
      r.set(f'{text}:filterInfo:{Dev_Zaid}', f'by={user.id}')
      r.sadd(f'FiltersList:{Dev_Zaid}', f'{text}')
      r.delete(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
      return await message.reply_text(f'( {text} )\nواضفنا الرد ياحلو\n☆',parse_mode=ParseMode.HTML)
   
   if message.video and r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}') and dev2_pls(user.id, chat.id):
      type = 'video'
      video = message.video.file_id
      if message.caption:
        caption = message.caption_html
      else:
        caption = 'None'
      text = r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
      r.set(f'{text}:filter:{Dev_Zaid}', f'type={type}&video={video}&caption={caption}')
      r.set(f'{text}:filtertype:{Dev_Zaid}','فيديو')
      r.set(f'{text}:filterInfo:{Dev_Zaid}', f'by={user.id}')
      r.sadd(f'FiltersList:{Dev_Zaid}', f'{text}')
      r.delete(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
      return await message.reply_text(f'( {text} )\nواضفنا الرد ياحلو\n☆',parse_mode=ParseMode.HTML)
   
   if message.animation and r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}') and dev2_pls(user.id, chat.id):
      type = 'animation'
      anim = message.animation.file_id
      if message.caption:
        caption = message.caption_html
      else:
        caption = 'None'
      text = r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
      r.set(f'{text}:filter:{Dev_Zaid}', f'type={type}&animation={anim}&caption={caption}')
      r.set(f'{text}:filtertype:{Dev_Zaid}','متحركه')
      r.set(f'{text}:filterInfo:{Dev_Zaid}', f'by={user.id}')
      r.sadd(f'FiltersList:{Dev_Zaid}', f'{text}')
      r.delete(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
      return await message.reply_text(f'( {text} )\nواضفنا الرد ياحلو\n☆',parse_mode=ParseMode.HTML)
   
   if message.audio and r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}') and dev2_pls(user.id, chat.id):
      type = 'audio'
      aud = message.audio.file_id
      if message.caption:
        caption = message.caption_html
      else:
        caption = 'None'
      text = r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
      r.set(f'{text}:filter:{Dev_Zaid}', f'type={type}&audio={aud}&caption={caption}')
      r.set(f'{text}:filtertype:{Dev_Zaid}','صوت')
      r.set(f'{text}:filterInfo:{Dev_Zaid}', f'by={user.id}')
      r.sadd(f'FiltersList:{Dev_Zaid}', f'{text}')
      r.delete(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
      return await message.reply_text(f'( {text} )\nواضفنا الرد ياحلو\n☆',parse_mode=ParseMode.HTML)
   
   if message.voice and r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}') and dev2_pls(user.id, chat.id):
      type = 'voice'
      voice = message.voice.file_id
      if message.caption:
        caption = message.caption_html
      else:
        caption = 'None'
      text = r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
      r.set(f'{text}:filter:{Dev_Zaid}', f'type={type}&voice={voice}&caption={caption}')
      r.set(f'{text}:filtertype:{Dev_Zaid}','بصمه')
      r.set(f'{text}:filterInfo:{Dev_Zaid}', f'by={user.id}')
      r.sadd(f'FiltersList:{Dev_Zaid}', f'{text}')
      r.delete(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
      return await message.reply_text(f'( {text} )\nواضفنا الرد ياحلو\n☆',parse_mode=ParseMode.HTML)
   
   if message.document and r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}') and dev2_pls(user.id, chat.id):
      type = 'doc'
      doc = message.document.file_id
      if message.caption:
        caption = message.caption_html
      else:
        caption = 'None'
      text = r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
      r.set(f'{text}:filter:{Dev_Zaid}', f'type={type}&doc={doc}&caption={caption}')
      r.set(f'{text}:filtertype:{Dev_Zaid}','ملف')
      r.set(f'{text}:filterInfo:{Dev_Zaid}', f'by={user.id}')
      r.sadd(f'FiltersList:{Dev_Zaid}', f'{text}')
      r.delete(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
      return await message.reply_text(f'( {text} )\nواضفنا الرد ياحلو\n☆',parse_mode=ParseMode.HTML)
   
   if message.sticker and r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}') and dev2_pls(user.id, chat.id):
      type = 'sticker'
      stic = message.sticker.file_id
      text = r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
      r.set(f'{text}:filter:{Dev_Zaid}', f'type={type}&sticker={stic}')
      r.set(f'{text}:filtertype:{Dev_Zaid}','ملصق')
      r.set(f'{text}:filterInfo:{Dev_Zaid}', f'by={user.id}')
      r.sadd(f'FiltersList:{Dev_Zaid}', f'{text}')
      r.delete(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}')
      return await message.reply_text(f'( {text} )\nواضفنا الرد ياحلو\n☆',parse_mode=ParseMode.HTML)
   
   
   
   
   
async def addCustomReplyDoneG(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await addreply2g(update, context, k)
    
async def addreply2g(update, context, k):
    message = update.message
    chat = update.effective_chat
    user = update.effective_user
    if not message or not chat or not user: return
    if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):  return
    if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
    if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
    if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return
    
    

async def addCustomReplyRandomG(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await addreplyrandomg(update, context, k)
   

async def addreplyrandomg(update, context, k):
   message = update.message
   chat = update.effective_chat
   user = update.effective_user
   if not message or not chat or not user: return
   if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return
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

   if r.get(f'{chat.id}:addFilterRG:{user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{chat.id}:addFilterRG:{user.id}{Dev_Zaid}')
     await message.reply_text(f'{k} من عيوني لغيت اضافة الرد المتعدد عام')
     return 
   
   if r.get(f'{chat.id}:addFilterRG2:{user.id}{Dev_Zaid}') and text == 'الغاء':
     rep = r.get(f'{chat.id}:addFilterRG2:{user.id}{Dev_Zaid}')
     r.delete(f'{chat.id}:addFilterRG2:{user.id}{Dev_Zaid}')
     r.delete(f'{rep.decode("utf-8")}:randomfilter:{Dev_Zaid}')
     await message.reply_text(f'{k} من عيوني لغيت اضافه الرد المتعدد عام')
     return 
     
   if r.get(f'{chat.id}:delFilterRG:{user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{chat.id}:delFilterRG:{user.id}{Dev_Zaid}')
     return await message.reply_text(f'{k} من عيوني لغيت مسح الرد المتعدد العام')
   
   if r.get(f'{chat.id}:addFilterRG2:{user.id}{Dev_Zaid}') and text == 'تم':
     text = r.get(f'{chat.id}:addFilterRG2:{user.id}{Dev_Zaid}')
     count = len(r.smembers((f'{text}:randomfilter:{Dev_Zaid}')))
     r.set(f'{text}:randomFilter:{Dev_Zaid}', 1)
     r.sadd(f'RFiltersList:{Dev_Zaid}', text)
     r.delete(f'{chat.id}:addFilterRG2:{user.id}{Dev_Zaid}')
     return await message.reply_text(f'{k} تم اضافه الرد المتعدد ( {text} )\n{k} بـ ( {count} ) جواب رد\n☆',parse_mode=ParseMode.HTML)
   
   if r.get(f'{chat.id}:delFilterRG:{user.id}{Dev_Zaid}') and dev2_pls(user.id,chat.id):
     if not r.get(f'{message.text}:randomFilter:{Dev_Zaid}'):
       r.delete(f'{chat.id}:delFilterRG:{user.id}{Dev_Zaid}')
       return await message.reply_text(f'{k} هذا الرد مو مضاف في قائمة الردود')
     else:
       r.delete(f'{message.text}:randomFilter:{Dev_Zaid}')
       r.delete(f'{message.text}:randomfilter:{Dev_Zaid}')
       r.delete(f'{chat.id}:delFilterRG:{user.id}{Dev_Zaid}')
       r.srem(f'RFiltersList:{Dev_Zaid}',message.text)
       return await message.reply_text(f'{k} ابشر مسحت الرد المتعدد ')
       
   
   if r.get(f'{chat.id}:addFilterRG:{user.id}{Dev_Zaid}') and dev2_pls(user.id,chat.id):
     r.delete(f'{chat.id}:addFilterRG:{user.id}{Dev_Zaid}')
     r.set(f'{chat.id}:addFilterRG2:{user.id}{Dev_Zaid}',message.text)
     return await message.reply_text(f'{k} حلو الحين ارسل اجوبة الرد\n{k} بس تخلص ارسل تم\nـــــــــــــــــــــــــــــــــــــــــ\n`<USER_ID>` › آيدي المستخدم\n`<USER_NAME>` › اسم المستخدم\n`<USER_USERNAME>` › يوزر المستخدم\n`<USER_MENTION>` › رابط حساب المستخدم\n༄',parse_mode=ParseMode.MARKDOWN)
   
   if r.get(f'{chat.id}:addFilterRG2:{user.id}{Dev_Zaid}') and dev2_pls(user.id,chat.id):
     text = r.get(f'{chat.id}:addFilterRG2:{user.id}{Dev_Zaid}')
     r.sadd(f'{text}:randomfilter:{Dev_Zaid}', message.text.html)
     return await message.reply_text(f'{k} حلو ضفت هذا الرد\n{k} بس تخلص ارسل تم\nـــــــــــــــــــــــــــــــــــــــــ\n`<USER_ID>` › آيدي المستخدم\n`<USER_NAME>` › اسم المستخدم\n`<USER_USERNAME>` › يوزر المستخدم\n`<USER_MENTION>` › رابط حساب المستخدم\n༄',parse_mode=ParseMode.MARKDOWN)
     
   if text == 'الردود المتعدده العامه':
     if not dev2_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
     else:
      if not r.smembers(f'RFiltersList:{Dev_Zaid}'):
       return await message.reply_text(f'{k} مافيه ردود عشوائيه عامة')
      else:
       text = 'الردود المتعدده:\n'
       count = 1
       for reply in r.smembers(f'RFiltersList:{Dev_Zaid}'):
          rep = reply
          ttt = len(r.smembers(f'{rep}:randomfilter:{Dev_Zaid}'))
          text += f'\n{count} - ( {rep} ) ࿓ ( {ttt} )'
          count += 1
       text += '\n☆'
       return await message.reply_text(text, disable_web_page_preview=True,parse_mode=ParseMode.HTML)
   
   if text == 'مسح الردود المتعدده العامه':
     if not dev2_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
     else:
       if not r.smembers(f'RFiltersList:{Dev_Zaid}'):
         return await message.reply_text(f'{k} مافيه ردود عشوائيه عامة')
       else:
         count = 0
         for reply in r.smembers(f'RFiltersList:{Dev_Zaid}'):
            rep = reply
            r.delete(f'{rep}:randomfilter:{Dev_Zaid}')
            r.srem(f'RFiltersList:{Dev_Zaid}', rep)
            r.delete(f'{rep}:randomFilter:{Dev_Zaid}')
            count += 1
         return await message.reply_text(f'{k} ابشر مسحت ( {count} ) رد متعدد ')
            
            
   
   if text == 'اضف رد متعدد عام' and not r.get(f'{chat.id}:addFilterRG:{user.id}{Dev_Zaid}') and not r.get(f'{chat.id}:addFilterRG2:{user.id}{Dev_Zaid}'):
     if not dev2_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
     else:
       r.set(f'{chat.id}:addFilterRG:{user.id}{Dev_Zaid}',1)
       return await message.reply_text(f'{k} حلو ، ارسل الحين الكلمة الي تبيها')
   
   if text == 'مسح رد متعدد عام' and not r.get(f'{chat.id}:addFilterRG:{user.id}{Dev_Zaid}'):
     if not dev2_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
     else:
       r.set(f'{chat.id}:delFilterRG:{user.id}{Dev_Zaid}',1)
       return await message.reply_text(f'{k} تمام عيني\n{k} الحين ارسل الرد عشان امسحه\n☆',parse_mode=ParseMode.HTML)
   
   
     
     
     


def register(app):
    """Register globalFilters handlers."""
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(
        filters.ALL & filters.ChatType.GROUPS,
        addCustomReplyG
    ), group=12)
    app.add_handler(MessageHandler(
        filters.ALL & filters.ChatType.GROUPS,
        addCustomReplyDoneG
    ), group=34)
    app.add_handler(MessageHandler(
        filters.ALL & filters.ChatType.GROUPS,
        addCustomReplyRandomG
    ), group=35)
