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

import random, re, time, pytz
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


async def addCustomReplyDone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await addreply2(update, context, k)
    
async def addreply2(update, context, k):
    
   message = update.message
    
   chat = update.effective_chat
    
   user = update.effective_user
   if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
   
   TIME_ZONE = "Asia/Riyadh"
   ZONE = pytz.timezone(TIME_ZONE)
   TIME = datetime.now(ZONE)
   date = TIME.strftime("%d/%m/%Y %I:%M:%S %p")
   
   if message.text:
     if message.text == 'الغاء' and r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}'):
       r.delete(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
       await message.reply_text(f'{k} من عيوني لغيت اضافة الرد')
     
     if r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}') and mod_pls(user.id, chat.id):
       text = r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
       r.set(f'{text}:filter:{Dev_Zaid}{chat.id}', f'type=text&text={message.text.html}')
       r.set(f'{text}:filtertype:{chat.id}{Dev_Zaid}','نص')
       r.set(f'{text}:filterInfo:{chat.id}{Dev_Zaid}', f'by={user.id}&date={date}')
       r.sadd(f'{chat.id}:FiltersList:{Dev_Zaid}', f'{text}')
       r.delete(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
       return await message.reply_text(f'( {text} )\nواضفنا الرد ياحلو\n☆',parse_mode=ParseMode.HTML)
   
   if message.photo and r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}') and mod_pls(user.id, chat.id):
      type = 'photo'
      photo = message.photo[-1].file_id
      if message.caption:
        caption = message.caption_html
      else:
        caption = 'None'
      text = r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
      r.set(f'{text}:filter:{Dev_Zaid}{chat.id}', f'type={type}&photo={photo}&caption={caption}')
      r.set(f'{text}:filtertype:{chat.id}{Dev_Zaid}','صوره')
      r.set(f'{text}:filterInfo:{chat.id}{Dev_Zaid}', f'by={user.id}&date={date}')
      r.sadd(f'{chat.id}:FiltersList:{Dev_Zaid}', f'{text}')
      r.delete(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
      return await message.reply_text(f'( {text} )\nواضفنا الرد ياحلو\n☆',parse_mode=ParseMode.HTML)
   
   if message.video and r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}') and mod_pls(user.id, chat.id):
      type = 'video'
      video = message.video.file_id
      if message.caption:
        caption = message.caption_html
      else:
        caption = 'None'
      text = r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
      r.set(f'{text}:filter:{Dev_Zaid}{chat.id}', f'type={type}&video={video}&caption={caption}')
      r.set(f'{text}:filtertype:{chat.id}{Dev_Zaid}','فيديو')
      r.set(f'{text}:filterInfo:{chat.id}{Dev_Zaid}', f'by={user.id}&date={date}')
      r.sadd(f'{chat.id}:FiltersList:{Dev_Zaid}', f'{text}')
      r.delete(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
      return await message.reply_text(f'( {text} )\nواضفنا الرد ياحلو\n☆',parse_mode=ParseMode.HTML)
   
   if message.animation and r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}') and mod_pls(user.id, chat.id):
      type = 'animation'
      anim = message.animation.file_id
      if message.caption:
        caption = message.caption_html
      else:
        caption = 'None'
      text = r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
      r.set(f'{text}:filter:{Dev_Zaid}{chat.id}', f'type={type}&animation={anim}&caption={caption}')
      r.set(f'{text}:filtertype:{chat.id}{Dev_Zaid}','متحركه')
      r.set(f'{text}:filterInfo:{chat.id}{Dev_Zaid}', f'by={user.id}&date={date}')
      r.sadd(f'{chat.id}:FiltersList:{Dev_Zaid}', f'{text}')
      r.delete(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
      return await message.reply_text(f'( {text} )\nواضفنا الرد ياحلو\n☆',parse_mode=ParseMode.HTML)
   
   if message.audio and r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}') and mod_pls(user.id, chat.id):
      type = 'audio'
      aud = message.audio.file_id
      if message.caption:
        caption = message.caption_html
      else:
        caption = 'None'
      text = r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
      r.set(f'{text}:filter:{Dev_Zaid}{chat.id}', f'type={type}&audio={aud}&caption={caption}')
      r.set(f'{text}:filtertype:{chat.id}{Dev_Zaid}','صوت')
      r.set(f'{text}:filterInfo:{chat.id}{Dev_Zaid}', f'by={user.id}&date={date}')
      r.sadd(f'{chat.id}:FiltersList:{Dev_Zaid}', f'{text}')
      r.delete(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
      return await message.reply_text(f'( {text} )\nواضفنا الرد ياحلو\n☆',parse_mode=ParseMode.HTML)
   
   if message.voice and r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}') and mod_pls(user.id, chat.id):
      type = 'voice'
      voice = message.voice.file_id
      if message.caption:
        caption = message.caption_html
      else:
        caption = 'None'
      text = r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
      r.set(f'{text}:filter:{Dev_Zaid}{chat.id}', f'type={type}&voice={voice}&caption={caption}')
      r.set(f'{text}:filtertype:{chat.id}{Dev_Zaid}','بصمه')
      r.set(f'{text}:filterInfo:{chat.id}{Dev_Zaid}', f'by={user.id}&date={date}')
      r.sadd(f'{chat.id}:FiltersList:{Dev_Zaid}', f'{text}')
      r.delete(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
      return await message.reply_text(f'( {text} )\nواضفنا الرد ياحلو\n☆',parse_mode=ParseMode.HTML)
   
   if message.document and r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}') and mod_pls(user.id, chat.id):
      type = 'doc'
      doc = message.document.file_id
      if message.caption:
        caption = message.caption_html
      else:
        caption = 'None'
      text = r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
      r.set(f'{text}:filter:{Dev_Zaid}{chat.id}', f'type={type}&doc={doc}&caption={caption}')
      r.set(f'{text}:filtertype:{chat.id}{Dev_Zaid}','ملف')
      r.set(f'{text}:filterInfo:{chat.id}{Dev_Zaid}', f'by={user.id}&date={date}')
      r.sadd(f'{chat.id}:FiltersList:{Dev_Zaid}', f'{text}')
      r.delete(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
      return await message.reply_text(f'( {text} )\nواضفنا الرد ياحلو\n☆',parse_mode=ParseMode.HTML)
   
   if message.sticker and r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}') and mod_pls(user.id, chat.id):
      type = 'sticker'
      stic = message.sticker.file_id
      text = r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
      r.set(f'{text}:filter:{Dev_Zaid}{chat.id}', f'type={type}&sticker={stic}')
      r.set(f'{text}:filtertype:{chat.id}{Dev_Zaid}','ستيكر')
      r.set(f'{text}:filterInfo:{chat.id}{Dev_Zaid}', f'by={user.id}&date={date}')
      r.sadd(f'{chat.id}:FiltersList:{Dev_Zaid}', f'{text}')
      r.delete(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}')
      return await message.reply_text(f'( {text} )\nواضفنا الرد ياحلو\n☆',parse_mode=ParseMode.HTML)
   

async def addCustomReply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await addreply(update, context, k)
    
async def addreply(update, context, k):
    
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
   text = message.text or ''
   name = r.get(f'{Dev_Zaid}:BotName') or NAME
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}'):
       text = r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}')
   if r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')
   if isLockCommand(user.id, chat.id, text): return
   if r.get(f'{chat.id}:addFilter:{user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{chat.id}:addFilter:{user.id}{Dev_Zaid}')
     await message.reply_text(f'{k} من عيوني لغيت اضافة الرد')
     return 
   
   if r.get(f'{chat.id}:delFilter:{user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{chat.id}:delFilter:{user.id}{Dev_Zaid}')
     await message.reply_text(f'{k} من عيوني لغيت مسح الرد')
     return 

   if r.get(f'{chat.id}:delFilter:{user.id}{Dev_Zaid}') and mod_pls(user.id,chat.id):
      if not r.get(f'{message.text}:filterInfo:{chat.id}{Dev_Zaid}'):
        r.delete(f'{chat.id}:delFilter:{user.id}{Dev_Zaid}')
        return await message.reply_text(f'{k} هذا الرد مو مضاف في قائمة الردود')
      else:
           r.delete(f'{message.text}:filter:{Dev_Zaid}{chat.id}')
           r.delete(f'{message.text}:filtertype:{chat.id}{Dev_Zaid}')
           r.delete(f'{message.text}:filterInfo:{chat.id}{Dev_Zaid}')
           r.srem(f'{chat.id}:FiltersList:{Dev_Zaid}', message.text)
           r.delete(f'{chat.id}:delFilter:{user.id}{Dev_Zaid}')
           return await message.reply_text(f'( {message.text} )\n{k} وحذفنا الرد ياحلو')

   if r.get(f'{chat.id}:addFilter:{user.id}{Dev_Zaid}') and mod_pls(user.id,chat.id):
      r.set(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}', message.text)
      r.delete(f'{chat.id}:addFilter:{user.id}{Dev_Zaid}')
      await message.reply_text(f'{k} حلو الحين ارسل جواب الرد\n{k} ( نص,صوره,فيديو,متحركه,بصمه,صوت,ملف )\nـــــــــــــــــــــــــــــــــــــــــ\n`<USER_ID>` › آيدي المستخدم\n`<USER_NAME>` › اسم المستخدم\n`<USER_USERNAME>` › يوزر المستخدم\n`<USER_MENTION>` › رابط حساب المستخدم\n༄',parse_mode=ParseMode.MARKDOWN)
      return 

   if text.startswith('الرد ') and len(message.text.split()) > 1 and mod_pls(user.id,chat.id):
      reply = message.text.split(None,1)[1]
      if not r.get(f'{reply}:filterInfo:{chat.id}{Dev_Zaid}'):
        return await message.reply_text(f'{k} الرد مو مضاف')
      else:
        get = r.get(f'{reply}:filterInfo:{chat.id}{Dev_Zaid}')
        split = get.split('by=')[1]
        by = split.split('&date=')[0]
        date = split.split('&date=')[1]
        type = r.get(f'{reply}:filtertype:{chat.id}{Dev_Zaid}')
        text = f'{k} الرد ↢ [{reply}](tg://user?id={by})\n{k} تاريخ الاضافة ↢\n( {date} )\n{k} نوع الرد {type}\n☆'
        await message.reply_text(text)
        return 
   
   if text == 'تعطيل الردود':
     if not mod_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
     if r.get(f'{chat.id}:lock_filter:{Dev_Zaid}'):
        return await message.reply_text(f'{k} من「 {user.mention} 」\n{k} الردود معطله من قبل\n☆',parse_mode=ParseMode.HTML)
     else:
        r.set(f'{chat.id}:lock_filter:{Dev_Zaid}',1)
        return await message.reply_text(f'{k} من「 {user.mention} 」\n{k} ابشر عطلت الردود\n☆',parse_mode=ParseMode.HTML)
   
   if text == 'تفعيل الردود':
     if not mod_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
     if not r.get(f'{chat.id}:lock_filter:{Dev_Zaid}'):
        return await message.reply_text(f'{k} من「 {user.mention} 」\n{k} الردود مفعله من قبل\n☆',parse_mode=ParseMode.HTML)
     else:
        r.delete(f'{chat.id}:lock_filter:{Dev_Zaid}')
        return await message.reply_text(f'{k} من「 {user.mention} 」\n{k} ابشر فعلت الردود\n☆',parse_mode=ParseMode.HTML)
  
   if text == 'تعطيل ردود الاعضاء':
     if not mod_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
     if r.get(f'{chat.id}:lock_filterMEM:{Dev_Zaid}'):
        return await message.reply_text(f'{k} من「 {user.mention} 」\n{k} ردود الاعضاء معطله من قبل\n☆',parse_mode=ParseMode.HTML)
     else:
        r.set(f'{chat.id}:lock_filterMEM:{Dev_Zaid}',1)
        return await message.reply_text(f'{k} من「 {user.mention} 」\n{k} ابشر عطلت ردود الاعضاء\n☆',parse_mode=ParseMode.HTML)
   
   if text == 'تفعيل ردود الاعضاء':
     if not mod_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
     if not r.get(f'{chat.id}:lock_filterMEM:{Dev_Zaid}'):
        return await message.reply_text(f'{k} من「 {user.mention} 」\n{k} ردود الاعضاء مفعله من قبل\n☆',parse_mode=ParseMode.HTML)
     else:
        r.delete(f'{chat.id}:lock_filterMEM:{Dev_Zaid}')
        return await message.reply_text(f'{k} من「 {user.mention} 」\n{k} ابشر فعلت ردود الاعضاء\n☆',parse_mode=ParseMode.HTML)
   
   if text == 'ردود الاعضاء':
     if not mod_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
     else:
      if not r.smembers(f'{chat.id}:FiltersListMEM:{Dev_Zaid}'):
       return await message.reply_text(f'{k} مافيه ردود اعضاء مضافه')
      else:
       text = 'ردود الاعضاء:\n'
       count = 1
       for reply in r.smembers(f'{chat.id}:FiltersListMEM:{Dev_Zaid}'):
          rep = reply.split("&&&&")[0]
          type = reply.split("&&&&")[1]
          try:
            mention=f'<a href="tg://user?id={type}">{type}</a>'
          except:
            mention=f'<a href="tg://user?id={type}">{type}</a>'
          text += f'\n{count} - ( {rep} ) ࿓ ( {mention} )'
          count += 1
       text += '\n☆'
       return await message.reply_text(text, disable_web_page_preview=True,parse_mode=ParseMode.HTML)
   
   if text == 'مسح ردود الاعضاء':
     if not mod_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
     else:
      if not r.smembers(f'{chat.id}:FiltersListMEM:{Dev_Zaid}'):
        return await message.reply_text(f'{k} مافيه ردود اعضاء مضافه')
      else:
        total = 0
        for reply in r.smembers(f'{chat.id}:FiltersListMEM:{Dev_Zaid}'):
           rep = reply
           r.delete(f'{rep}:filterMEM:{Dev_Zaid}{chat.id}')
           r.srem(f'{chat.id}:FiltersListMEM:{Dev_Zaid}', rep)
           r.delete(f"{rep.split('&&&&')[1]}:FILT:{chat.id}{Dev_Zaid}")
           total += 1
        return await message.reply_text(f'{k} ابشر مسحت ( {total} ) من ردود الاعضاء')
   
   if text == 'الردود':
     if not mod_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
     else:
      if not r.smembers(f'{chat.id}:FiltersList:{Dev_Zaid}'):
       return await message.reply_text(f'{k} مافيه ردود مضافه')
      else:
       text = 'ردود المجموعه:\n'
       count = 1
       for reply in r.smembers(f'{chat.id}:FiltersList:{Dev_Zaid}'):
          rep = reply
          type = r.get(f'{rep}:filtertype:{chat.id}{Dev_Zaid}')
          text += f'\n{count} - ( {rep} ) ࿓ ( {type} )'
          count += 1
       text += '\n☆'
       return await message.reply_text(text, disable_web_page_preview=True,parse_mode=ParseMode.HTML)
  
   if text == 'مسح الردود':
     if not mod_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
     else:
      if not r.smembers(f'{chat.id}:FiltersList:{Dev_Zaid}'):
        return await message.reply_text(f'{k} مافيه ردود مضافه')
      else:
        total = 0
        for reply in r.smembers(f'{chat.id}:FiltersList:{Dev_Zaid}'):
           rep = reply
           r.delete(f'{rep}:filter:{Dev_Zaid}{chat.id}')
           r.delete(f'{rep}:filtertype:{chat.id}{Dev_Zaid}')
           r.delete(f'{rep}:filterInfo:{chat.id}{Dev_Zaid}')
           r.srem(f'{chat.id}:FiltersList:{Dev_Zaid}', rep)
           total += 1
        return await message.reply_text(f'{k} ابشر مسحت ( {total} ) من الردود')
   
   if text == 'اضف ردي':
      if r.get(f'{chat.id}:lock_filterMEM:{Dev_Zaid}'):
        return await message.reply_text(f'{k} تم تعطيل ردود الأعضاء')
      if r.get(f"{user.id}:FILT:{chat.id}{Dev_Zaid}"):
        name = r.get(f"{user.id}:FILT:{chat.id}{Dev_Zaid}")
        return await message.reply_text(f"{k} عندك رد مضاف من قبل و هو ( {name} )")
      else:
        await message.reply_text(f'{k} حلو ، الحين ارسل اسمك')
        r.set(f'{chat.id}:addFilterMM:{user.id}{Dev_Zaid}',1,ex=600)
        return 
   
   if r.get(f'{chat.id}:addFilterMM:{user.id}{Dev_Zaid}') and text == "الغاء":
     r.delete(f'{chat.id}:addFilterMM:{user.id}{Dev_Zaid}')
     return await message.reply_text(f"{k} ابشر لغيت اضافة ردك")
     
   
   if r.get(f'{chat.id}:addFilterMM:{user.id}{Dev_Zaid}') and len(message.text) <= 50:
     name = message.text
     if r.sismember(f'{chat.id}:FiltersListMEM:{Dev_Zaid}',name):
       return await message.reply_text(f"{k} هذا الإسم محجوز")
     else:
       r.sadd(f'{chat.id}:FiltersListMEM:{Dev_Zaid}',f"{name}&&&&{user.id}")
       r.sadd(f'{chat.id}:FiltersListMEMM:{Dev_Zaid}',user.id)
       r.set(f'{name}:filterMEM:{Dev_Zaid}{chat.id}',user.id)
       r.set(f"{user.id}:FILT:{chat.id}{Dev_Zaid}",name)
       r.delete(f'{chat.id}:addFilterMM:{user.id}{Dev_Zaid}')
       return await message.reply_text(f"{k} ابشر ضفت ردك ( {name} )")
   
   if text == 'مسح ردي':
     if r.get(f"{user.id}:FILT:{chat.id}{Dev_Zaid}"):
       rep=r.get(f"{user.id}:FILT:{chat.id}{Dev_Zaid}")
       r.delete(f'{rep}:filterMEM:{Dev_Zaid}{chat.id}')
       r.srem(f'{chat.id}:FiltersListMEM:{Dev_Zaid}', f"{rep}&&&&{user.id}")
       r.delete(f"{user.id}:FILT:{chat.id}{Dev_Zaid}")
       return await message.reply_text(f"{k} ابشر مسحت ردك ( {rep} )")
     else:
       return await message.reply_text(f"{k} ماعندك رد")
        
   if text == 'اضف رد':
     if not r.get(f'{chat.id}:addFilter:{user.id}{Dev_Zaid}'):
      if not mod_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
      else:
        await message.reply_text(f'{k} حلو ، الحين ارسل الكلمة اللي تبيها')
        r.set(f'{chat.id}:addFilter:{user.id}{Dev_Zaid}',1)
        return 
        
   if text == 'مسح رد':
     if not r.get(f'{chat.id}:delFilter:{user.id}{Dev_Zaid}'):
      if not mod_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
      else:
        r.set(f'{chat.id}:delFilter:{user.id}{Dev_Zaid}',1)
        await message.reply_text(f'{k} تمام عيني\n{k} الحين ارسل الرد عشان امسحه\n☆',parse_mode=ParseMode.HTML)
        return 
   
   
   
   
   

   

async def addCustomReplyRandom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await addreplyrandom(update, context, k)
   

async def addreplyrandom(update, context, k):
   

   message = update.message
   

   chat = update.effective_chat
   

   user = update.effective_user
   if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return
   if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}'):  return 
   text = message.text
   name = r.get(f'{Dev_Zaid}:BotName') or NAME
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}'):
       text = r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}')
   if r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')
   
   if isLockCommand(user.id, chat.id, text): return

   if r.get(f'{chat.id}:addFilterR:{user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{chat.id}:addFilterR:{user.id}{Dev_Zaid}')
     await message.reply_text(f'{k} من عيوني لغيت اضافة الرد المميز')
     return 
   
   if r.get(f'{chat.id}:addFilterR2:{user.id}{Dev_Zaid}') and text == 'الغاء':
     rep = r.get(f'{chat.id}:addFilterR2:{user.id}{Dev_Zaid}')
     r.delete(f'{chat.id}:addFilterR2:{user.id}{Dev_Zaid}')
     r.delete(f'{rep}:randomfilter:{chat.id}{Dev_Zaid}')
     await message.reply_text(f'{k} من عيوني لغيت اضافه الرد المميز')
     return 
     
   if r.get(f'{chat.id}:delFilterR:{user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{chat.id}:delFilterR:{user.id}{Dev_Zaid}')
     return await message.reply_text(f'{k} من عيوني لغيت مسح الرد المميز')
   
   if r.get(f'{chat.id}:addFilterR2:{user.id}{Dev_Zaid}') and text == 'تم':
     text = r.get(f'{chat.id}:addFilterR2:{user.id}{Dev_Zaid}')
     count = len(r.smembers((f'{text}:randomfilter:{chat.id}{Dev_Zaid}')))
     r.set(f'{text}:randomFilter:{chat.id}{Dev_Zaid}', 1)
     r.sadd(f'{chat.id}:RFiltersList:{Dev_Zaid}', text)
     r.delete(f'{chat.id}:addFilterR2:{user.id}{Dev_Zaid}')
     return await message.reply_text(f'{k} تم اضافه الرد المميز ( {text} )\n{k} بـ ( {count} ) جواب رد\n☆',parse_mode=ParseMode.HTML)
   
   if r.get(f'{chat.id}:delFilterR:{user.id}{Dev_Zaid}') and mod_pls(user.id,chat.id):
     if not r.get(f'{message.text}:randomFilter:{chat.id}{Dev_Zaid}'):
       r.delete(f'{chat.id}:delFilterR:{user.id}{Dev_Zaid}')
       return await message.reply_text(f'{k} هذا الرد مو مضاف في قائمة الردود')
     else:
       r.delete(f'{message.text}:randomFilter:{chat.id}{Dev_Zaid}')
       r.delete(f'{message.text}:randomfilter:{chat.id}{Dev_Zaid}')
       r.delete(f'{chat.id}:delFilterR:{user.id}{Dev_Zaid}')
       r.srem(f'{chat.id}:RFiltersList:{Dev_Zaid}',message.text)
       return await message.reply_text(f'{k} ابشر مسحت الرد العشوائي ')
       
   
   if r.get(f'{chat.id}:addFilterR:{user.id}{Dev_Zaid}') and mod_pls(user.id,chat.id):
     r.delete(f'{chat.id}:addFilterR:{user.id}{Dev_Zaid}')
     r.set(f'{chat.id}:addFilterR2:{user.id}{Dev_Zaid}',message.text)
     return await message.reply_text(f'{k} حلو الحين ارسل اجوبة الرد\n{k} بس تخلص ارسل تم\nـــــــــــــــــــــــــــــــــــــــــ\n`<USER_ID>` › آيدي المستخدم\n`<USER_NAME>` › اسم المستخدم\n`<USER_USERNAME>` › يوزر المستخدم\n`<USER_MENTION>` › رابط حساب المستخدم\n༄',parse_mode=ParseMode.MARKDOWN)
   
   if r.get(f'{chat.id}:addFilterR2:{user.id}{Dev_Zaid}') and mod_pls(user.id,chat.id):
     text = r.get(f'{chat.id}:addFilterR2:{user.id}{Dev_Zaid}')
     r.sadd(f'{text}:randomfilter:{chat.id}{Dev_Zaid}', message.text.html)
     return await message.reply_text(f'{k} حلو ضفت هذا الرد\n{k} بس تخلص ارسل تم\nـــــــــــــــــــــــــــــــــــــــــ\n`<USER_ID>` › آيدي المستخدم\n`<USER_NAME>` › اسم المستخدم\n`<USER_USERNAME>` › يوزر المستخدم\n`<USER_MENTION>` › رابط حساب المستخدم\n༄',parse_mode=ParseMode.MARKDOWN)
     
   if text == 'الردود المميزه':
     if not mod_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
     else:
      if not r.smembers(f'{chat.id}:RFiltersList:{Dev_Zaid}'):
       return await message.reply_text(f'{k} مافيه ردود عشوائيه مضافه')
      else:
       text = 'الردود المميزه:\n'
       count = 1
       for reply in r.smembers(f'{chat.id}:RFiltersList:{Dev_Zaid}'):
          rep = reply
          ttt = len(r.smembers(f'{rep}:randomfilter:{chat.id}{Dev_Zaid}'))
          text += f'\n{count} - ( {rep} ) ☆ ( {ttt} )'
          count += 1
       text += '\n☆'
       return await message.reply_text(text, disable_web_page_preview=True,parse_mode=ParseMode.HTML)
   
   if text == 'مسح الردود المميزه':
     if not mod_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
     else:
       if not r.smembers(f'{chat.id}:RFiltersList:{Dev_Zaid}'):
         return await message.reply_text(f'{k} مافيه ردود مميزه مضافه')
       else:
         count = 0
         for reply in r.smembers(f'{chat.id}:RFiltersList:{Dev_Zaid}'):
            rep = reply
            r.delete(f'{rep}:randomfilter:{chat.id}{Dev_Zaid}')
            r.srem(f'{chat.id}:RFiltersList:{Dev_Zaid}', rep)
            r.delete(f'{rep}:randomFilter:{chat.id}{Dev_Zaid}')
            count += 1
         return await message.reply_text(f'{k} ابشر مسحت ( {count} ) رد مميز ')
            
   if text == 'اضف رد مميز' and not r.get(f'{chat.id}:addFilterR:{user.id}{Dev_Zaid}') and not r.get(f'{chat.id}:addFilterR2:{user.id}{Dev_Zaid}'):
     if not mod_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
     else:
       r.set(f'{chat.id}:addFilterR:{user.id}{Dev_Zaid}',1)
       return await message.reply_text(f'{k} حلو ، ارسل الحين الكلمة الي تبيها')
   
   if text == 'مسح رد مميز' and not r.get(f'{chat.id}:delFilterR:{user.id}{Dev_Zaid}'):
     if not mod_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
     else:
       r.set(f'{chat.id}:delFilterR:{user.id}{Dev_Zaid}',1)
       return await message.reply_text(f'{k} تمام عيني\n{k} الحين ارسل الرد عشان امسحه\n☆',parse_mode=ParseMode.HTML)
   
   
     
     
     


def register(app):
    """Register customFilter handlers."""
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(
        filters.ALL & filters.ChatType.GROUPS,
        addCustomReplyDone
    ), group=11)
    app.add_handler(MessageHandler(
        filters.ALL & filters.ChatType.GROUPS,
        addCustomReply
    ), group=32)
    app.add_handler(MessageHandler(
        filters.ALL & filters.ChatType.GROUPS,
        addCustomReplyRandom
    ), group=33)
