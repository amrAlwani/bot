
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

async def customCummandHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await addcommand(update, context, k)
   
   
async def addcommand(update, context, k):
   
   
   message = update.message
   
   
   chat = update.effective_chat
   
   
   user = update.effective_user
   if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return  
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return
   text = message.text
   name = r.get(f'{Dev_Zaid}:BotName') or NAME
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}'):
       text = r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}')
   if r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')
   if isLockCommand(user.id, chat.id, text): return
   if r.get(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}')
     return await message.reply_text(quote=True,text=f'{k} من عيوني لغيت اضافة امر ')
   
   if r.get(f'{chat.id}:addCustom2:{user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{chat.id}:addCustom2:{user.id}{Dev_Zaid}')
     return await message.reply_text(quote=True,text=f'{k} من عيوني لغيت اضافة امر ')

   if text == 'الاوامر المضافه' or text == 'الاوامر المضافة':
      if not owner_pls(user.id, chat.id):
          return await message.reply_text(quote=True,text=f'{k} هذا الامر يخص ( المالك وفوق ) وبس')
      else:
          if not r.smembers(f'{chat.id}:listCustom:{chat.id}{Dev_Zaid}'):
            return await message.reply_text(quote=True,text=f'{k} مافيه اوامر مضافه')
          else:
              text = 'الاوامر المضافة:\n'
              count = 0
              for cmnd in r.smembers(f'{chat.id}:listCustom:{chat.id}{Dev_Zaid}'):
                 count += 1
                 command = cmnd
                 cc = r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={command}')
                 old_c = cc
                 text += f'{count}) {command} ~ ( {old_c} )\n'
              text += '\n༄'
              return await message.reply_text(quote=True,text=text)
   
   if text == 'اضف امر' or text == 'تغيير امر':
     if not r.get(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}'):
       if not owner_pls(user.id, chat.id):
          return await message.reply_text(quote=True,text=f'{k} هذا الامر يخص ( المالك وفوق ) وبس')
       else:
          r.set(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}',1)
          await message.reply_text(quote=True,text=f'{k} تمام عيني ، ارسل الامر القديم عشان اغيره')
          return

   if r.get(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}') and admin_pls(user.id, chat.id) and len(message.text) < 50:
      r.delete(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}')
      r.set(f'{chat.id}:addCustom2:{user.id}{Dev_Zaid}', message.text)
      await message.reply_text(quote=True,text=f'{k} حلو عشان تغيير امر ( {message.text} )\n{k} ارسل الامر الجديد الحين\n☆')
      return
   
   if r.get(f'{chat.id}:addCustom2:{user.id}{Dev_Zaid}') and admin_pls(user.id, chat.id) and len(message.text) < 50:
      command_o = r.get(f'{chat.id}:addCustom2:{user.id}{Dev_Zaid}')
      command_n = message.text
      r.delete(f'{chat.id}:addCustom2:{user.id}{Dev_Zaid}')
      r.set(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={command_n}', command_o)
      r.sadd(f'{chat.id}:listCustom:{chat.id}{Dev_Zaid}', command_n)
      await message.reply_text(quote=True,text=f'{k} غيرت الامر القديم {command_o}\n{k} الى الامر الجديد ( {command_n} )')
      return 


async def delCustomCommandHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await delcommand(update, context, k)
   
   
async def delcommand(update, context, k):
   
   
   message = update.message
   
   
   chat = update.effective_chat
   
   
   user = update.effective_user
   if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return
   if r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}'):  return
   text = message.text
   if r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={message.text}'):
       text = r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={message.text}')
   
   if r.get(f'Custom:{Dev_Zaid}&text={message.text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={message.text}')
   
   if isLockCommand(user.id, chat.id, text): return
   if r.get(f'{chat.id}:delCustom:{user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{chat.id}:delCustom:{user.id}{Dev_Zaid}')
     return await message.reply_text(quote=True,text=f'{k} من عيوني لغيت مسح امر ')

   if text == 'مسح الاوامر' or text == 'مسح الاوامر المضافة':
     if not mod_pls(user.id, chat.id):
       return await message.reply_text(quote=True,text=f'{k} هذا الامر يخص ( المدير وفوق ) وبس') 
     else:
       if not r.smembers(f'{chat.id}:listCustom:{chat.id}{Dev_Zaid}'):
         return await message.reply_text(quote=True,text=f'{k} مافيه اوامر مضافه')
       else:
         count = 0
         for cmnd in r.smembers(f'{chat.id}:listCustom:{chat.id}{Dev_Zaid}'):
           command = cmnd
           r.delete(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={command}')
           r.srem(f'{chat.id}:listCustom:{chat.id}{Dev_Zaid}', command)
           count += 1
         text = f'من「 {user.mention_html()} 」\n{k} ابشر مسحت {count} أمر\n☆'
         return await message.reply_text(quote=True,text=text)
       
   
   if text == 'مسح امر':
     if not r.get(f'{chat.id}:delCustom:{user.id}{Dev_Zaid}'):
       if not mod_pls(user.id, chat.id):
          return await message.reply_text(quote=True,text=f'{k} هذا الامر يخص ( المدير وفوق ) وبس')
       else:
          r.set(f'{chat.id}:delCustom:{user.id}{Dev_Zaid}',1)
          await message.reply_text(quote=True,text=f'{k} ارسل الامر الحين')
          return
      

   if r.get(f'{chat.id}:delCustom:{user.id}{Dev_Zaid}') and admin_pls(user.id, chat.id) and len(message.text) < 50:
      r.delete(f'{chat.id}:delCustom:{user.id}{Dev_Zaid}')
      if not r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={message.text}'):
         return await message.reply_text(quote=True,text=f'{k} هذا الأمر مو مضاف')
      r.srem(f'{chat.id}:listCustom:{chat.id}{Dev_Zaid}', message.text)
      r.delete(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={message.text}')
      await message.reply_text(quote=True,text=f'{k} من「 {user.mention_html()} 」\n{k} ابشر مسحت الأمر\n☆')
      return
   
   
      
      
############ global CustomCommand



async def customCummandGlobalHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await addcommandg(update, context, k)
   
   
async def addcommandg(update, context, k):
   
   
   message = update.message
   
   
   chat = update.effective_chat
   
   
   user = update.effective_user
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return
   text = message.text
   if r.get(f'Custom:{Dev_Zaid}&text={message.text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={message.text}')
   
   if r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}')
     return await message.reply_text(quote=True,text=f'{k} من عيوني لغيت اضف امر عام')
   
   if r.get(f'{chat.id}:addCustom2G:{user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{chat.id}:addCustom2G:{user.id}{Dev_Zaid}')
     return await message.reply_text(quote=True,text=f'{k} من عيوني لغيت اضف امر عام')

   if text == 'الاوامر العامه' or text == 'الاوامر المضافه العامه' and not chat.type == ChatType.PRIVATE:
      if not dev_pls(user.id, chat.id):
          return await message.reply_text(quote=True,text=f'{k} هذا الامر يخص ( المطور وفوق ) وبس')
      else:
          if not r.smembers(f'listCustom:{Dev_Zaid}'):
            return await message.reply_text(quote=True,text=f'{k} مافيه اوامر عامه مضافه')
          else:
              text = 'الاوامر العامه:\n'
              count = 0
              for cmnd in r.smembers(f'listCustom:{Dev_Zaid}'):
                 count += 1
                 command = cmnd
                 cc = r.get(f'Custom:{Dev_Zaid}&text={command}')
                 old_c = cc
                 text += f'{count}) {command} ~ ( {old_c} )\n'
              text += '\n☆'
              return await message.reply_text(quote=True,text=text)
   
   if text == 'اضف امر عام' or text == 'تغيير امر عام':
     if not r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}'):
       if not dev_pls(user.id, chat.id):
          return await message.reply_text(quote=True,text=f'{k} هذا الامر يخص ( المطور وفوق ) وبس')
       else:
          r.set(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}',1)
          await message.reply_text(quote=True,text=f'{k} تمام عيني ، ارسل الامر القديم عشان اغيره')
          return

   if r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}') and dev_pls(user.id, chat.id) and len(message.text) < 50:
      r.delete(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}')
      r.set(f'{chat.id}:addCustom2G:{user.id}{Dev_Zaid}', message.text)
      await message.reply_text(quote=True,text=f'{k} حلو عشان تغيير امر ( {message.text} )\n{k} ارسل الامر الجديد الحين\n☆')
      return
   
   if r.get(f'{chat.id}:addCustom2G:{user.id}{Dev_Zaid}') and dev_pls(user.id, chat.id) and len(message.text) < 50:
      command_o = r.get(f'{chat.id}:addCustom2G:{user.id}{Dev_Zaid}')
      command_n = message.text
      r.delete(f'{chat.id}:addCustom2G:{user.id}{Dev_Zaid}')
      r.set(f'Custom:{Dev_Zaid}&text={command_n}', command_o)
      r.sadd(f'listCustom:{Dev_Zaid}', command_n)
      await message.reply_text(quote=True,text=f'{k} غيرت الامر القديم {command_o}\n{k} الى الامر الجديد ( {command_n} )')
      return 


async def delCustomCommandGHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await delcommandg(update, context, k)
   
   
async def delcommandg(update, context, k):
   
   
   message = update.message
   
   
   chat = update.effective_chat
   
   
   user = update.effective_user
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return
   if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
   text = message.text or ''
   if text and r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')
   
   if r.get(f'{chat.id}:delCustomG:{user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{chat.id}:delCustomG:{user.id}{Dev_Zaid}')
     return await message.reply_text(quote=True,text=f'{k} من عيوني لغيت مسح امر عام')

   if text == 'مسح الاوامر العامه':
     if not dev_pls(user.id, chat.id):
       return await message.reply_text(quote=True,text=f'{k} هذا الامر يخص ( المطور وفوق ) وبس') 
     else:
       if not r.smembers(f'listCustom:{Dev_Zaid}'):
         return await message.reply_text(quote=True,text=f'{k} مافيه اوامر عامه مضافه')
       else:
         count = 0
         for cmnd in r.smembers(f'listCustom:{Dev_Zaid}'):
           command = cmnd
           r.delete(f'Custom:{Dev_Zaid}&text={command}')
           r.srem(f'listCustom:{Dev_Zaid}', command)
           count += 1
         text = f'من「 {user.mention_html()} 」\n{k} ابشر مسحت {count} أمر عام\n☆'
         return await message.reply_text(quote=True,text=text)
       
   
   if text == 'مسح امر عام':
     if not r.get(f'{chat.id}:delCustomG:{user.id}{Dev_Zaid}'):
       if not dev_pls(user.id, chat.id):
          return await message.reply_text(quote=True,text=f'{k} هذا الامر يخص ( المطور وفوق ) وبس')
       else:
          r.set(f'{chat.id}:delCustomG:{user.id}{Dev_Zaid}',1)
          await message.reply_text(quote=True,text=f'{k} ارسل الامر الحين')
          return
   
   if re.match("^فتح امر ",text):
     if not gowner_pls(user.id, chat.id):
       return await message.reply_text(quote=True,text=f'{k} هذا الامر يخص ( المالك الاساسي وفوق ) وبس')
     else:
       txt=text.split(None,2)[2]
       if not r.hget(Dev_Zaid+f"locks-{chat.id}", txt):
         return await message.reply_text("الامر مو مقفول من قبل")
       r.hdel(Dev_Zaid+f"locks-{chat.id}", txt)
       return await message.reply_text("تم فتح الامر بنجاح")
   
   if text == "الاوامر المقفوله":
      if not gowner_pls(user.id, chat.id):
       return await message.reply_text(quote=True,text=f'{k} هذا الامر يخص ( المالك الاساسي وفوق ) وبس')
      else:
        if not r.hgetall(Dev_Zaid+f"locks-{chat.id}"):
          return await message.reply_text(f"{k} مافيه اوامر مقفولة")
        else:
          commands = r.hgetall(Dev_Zaid+f"locks-{chat.id}")
          txt = "الاوامر المقفوله:\n\n"
          count = 1
          for command in commands:
            cc = int(commands[command])
            if cc == 0:
              rank = "مالك اساسي"
            elif cc == 1:
              rank = "مالك وفوق"
            elif cc == 2:
              rank = "مدير و فوق"
            elif cc == 3:
              rank = "ادمن وفوق"
            elif cc == 4:
              rank = "مميز و فوق"
            txt += f"{count} ) {command} - ( {rank} )\n"
            count += 1
          return await message.reply_text(txt, disable_web_page_preview=True)
   
   if text == "مسح الاوامر المقفوله":
      if not gowner_pls(user.id, chat.id):
       return await message.reply_text(quote=True,text=f'{k} هذا الامر يخص ( المالك الاساسي وفوق ) وبس')
      else:
        if not r.hgetall(Dev_Zaid+f"locks-{chat.id}"):
          return await message.reply_text(f"{k} مافيه اوامر مقفولة")
        else:
          count = len(list(r.hgetall(Dev_Zaid+f"locks-{chat.id}").keys()))
          r.delete(Dev_Zaid+f"locks-{chat.id}")
          return await message.reply_text(f"{k} ابشر مسحت ( {count} )")
   
   if re.match("^قفل امر ",text):
     if not gowner_pls(user.id, chat.id):
       return await message.reply_text(quote=True,text=f'{k} هذا الامر يخص ( المالك الاساسي وفوق ) وبس')
     else:
       txt=text.split(None,2)[2]
       return await message.reply_text(
          f"{k} حسناً عزيزي اختار نوع الرتبه :\n{k} سيتم وضع امر ↤︎( {txt} ) له فقط",
          reply_markup=InlineKeyboardMarkup(
            [
              [
                InlineKeyboardButton (
                   "مالك اساسي",
                   callback_data=f"gowner+{user.id}"
                )
              ],
              [
                InlineKeyboardButton (
                   "مالك",
                   callback_data=f"owner+{user.id}"
                )
              ],
              [
                InlineKeyboardButton (
                   "مدير",
                   callback_data=f"mod+{user.id}"
                )
              ],
              [
                InlineKeyboardButton (
                   "ادمن",
                   callback_data=f"admin+{user.id}"
                )
              ],
              [
                InlineKeyboardButton (
                   "مميز",
                   callback_data=f"pre+{user.id}"
                )
              ]
            ]
          )
       )

   if r.get(f'{chat.id}:delCustomG:{user.id}{Dev_Zaid}') and dev_pls(user.id, chat.id) and len(message.text) < 50:
      r.delete(f'{chat.id}:delCustomG:{user.id}{Dev_Zaid}')
      if not r.get(f'Custom:{Dev_Zaid}&text={message.text}'):
         return await message.reply_text(quote=True,text=f'{k} هذا الأمر مو مضاف')
      r.srem(f'listCustom:{Dev_Zaid}', message.text)
      r.delete(f'Custom:{Dev_Zaid}&text={message.text}')
      await message.reply_text(quote=True,text=f'{k} من「 {user.mention_html()} 」\n{k} ابشر مسحت الأمر العام\n☆')
      return
   
   
      

def register(app):
    """Register customCommad handlers."""
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(
        filters.ALL & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
        customCummandHandler
    ), group=10)
    app.add_handler(MessageHandler(
        filters.ALL & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
        delCustomCommandHandler
    ), group=29)
    app.add_handler(MessageHandler(
        filters.ALL & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
        customCummandGlobalHandler
    ), group=30)
    app.add_handler(MessageHandler(
        filters.ALL & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
        delCustomCommandGHandler
    ), group=31)
