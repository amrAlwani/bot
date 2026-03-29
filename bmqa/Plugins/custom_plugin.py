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


async def addPluginHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await plugin_func(update, context, k)
    
async def plugin_func(update, context, k):
    
   message = update.message
    
   chat = update.effective_chat
    
   user = update.effective_user
   if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):
        return
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return
   if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
   
   if r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}'):  return
   if r.get(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:delCustom:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:delCustomG:{user.id}{Dev_Zaid}'):  return 
   text = message.text or ''
   name = r.get(f'{Dev_Zaid}:BotName') or NAME
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}'):
       text = r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}')
   if r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')
   
   if r.get(f'{user.id}:setAddP4:{chat.id}{Dev_Zaid}') or r.get(f'{user.id}:setAddP:{chat.id}{Dev_Zaid}') or r.get(f'{user.id}:setAddP2:{chat.id}{Dev_Zaid}') or r.get(f'{user.id}:setAddP3:{chat.id}{Dev_Zaid}') or r.get(f'{user.id}:setAddP4:{chat.id}{Dev_Zaid}') or r.get(f'{user.id}:setDelp:{chat.id}{Dev_Zaid}'):
     if text == 'الغاء':
       await message.reply_text(f'{k} ابشر ياعيني لغيت كلشي')
       r.delete(f'{user.id}:setAddP:{chat.id}{Dev_Zaid}')
       r.delete(f'{user.id}:setAddP2:{chat.id}{Dev_Zaid}')
       r.delete(f'{user.id}:setAddP3:{chat.id}{Dev_Zaid}')
       r.delete(f'{user.id}:setAddP4:{chat.id}{Dev_Zaid}')
       r.delete(f'{user.id}:setDelp:{chat.id}{Dev_Zaid}')
       return 
     
   if text == 'اضف ميزة' or text == 'اضف ميزه':
     if devp_pls(user.id,chat.id):
        r.set(f'{user.id}:setAddP:{chat.id}{Dev_Zaid}',1)
        return await message.reply_text(f'{k} هلا عيني ارسل اسم الميزة الحين')
   
   if r.get(f'{user.id}:setAddP:{chat.id}{Dev_Zaid}') and devp_pls(user.id,chat.id) and len((message.text or '').split()) == 1:
      r.delete(f'{user.id}:setAddP:{chat.id}{Dev_Zaid}')
      r.set(f'{user.id}:setAddP2:{chat.id}{Dev_Zaid}',message.text or '')
      return await message.reply_text(f'{k} تمام عيني ارسل نوع الميزة الحين ( صوره,فيديو,متحركه,بصمه,صوت)\n☆')
   
   if text in ['صوره','فيديو','متحركه','بصمه','صوت'] and r.get(f'{user.id}:setAddP2:{chat.id}{Dev_Zaid}') and devp_pls(user.id,chat.id):
      miza = r.get(f'{user.id}:setAddP2:{chat.id}{Dev_Zaid}')
      r.delete(f'{user.id}:setAddP2:{chat.id}{Dev_Zaid}')
      r.set(f'{user.id}:setAddP3:{chat.id}{Dev_Zaid}',f'miza={miza}&&type={message.text}')
      return await message.reply_text(f'{k} ارسل يوزر القناة الحين')
   
   if r.get(f'{user.id}:setAddP3:{chat.id}{Dev_Zaid}') and devp_pls(user.id,chat.id):
      miza = r.get(f'{user.id}:setAddP3:{chat.id}{Dev_Zaid}')
      miza += f'&&channel={message.text.replace("@","")}'
      r.delete(f'{user.id}:setAddP3:{chat.id}{Dev_Zaid}')
      r.set(f'{user.id}:setAddP4:{chat.id}{Dev_Zaid}', miza)
      return await message.reply_text(f'{k} ارسل الحين ايديات الرسايل العشوائية\n{k} مثال 1 - 100')
   
   if r.get(f'{user.id}:setAddP4:{chat.id}{Dev_Zaid}') and devp_pls(user.id,chat.id):
      miza = r.get(f'{user.id}:setAddP4:{chat.id}{Dev_Zaid}')
      id1 = int(message.text.split('-')[0])
      id2 = int(message.text.split('-')[1])
      r.delete(f'{user.id}:setAddP4:{chat.id}{Dev_Zaid}')
      miza_name = miza.split('miza=')[1].split('&&')[0]
      miza_type = miza.split('&&type=')[1].split('&&')[0]
      miza_channel = miza.split('&&channel=')[1].split('&&')[0]
      r.set(f'{miza_name}:customPlugin:{Dev_Zaid}', f'type={miza_type}&&channel={miza_channel}&&random={id1}_{id2}')
      r.sadd(f'customPlugins:{Dev_Zaid}', miza_name)
      return await message.reply_text(f'{k} ابشر ضفت الميزة ( {miza_name} )\n{k} نوع الميزة {miza_type}\n{k} قناة الميزة ( @{miza_channel} )')
   
   if text == 'مسح ميزة' or text == 'مسح ميزه':
     if devp_pls(user.id,chat.id):
        r.set(f'{user.id}:setDelp:{chat.id}{Dev_Zaid}',1)
        return await message.reply_text(f'{k} هلا عيني ارسل اسم الميزة الحين')
        
   if r.get(f'{user.id}:setDelp:{chat.id}{Dev_Zaid}') and devp_pls(user.id,chat.id):
     if not r.get(f'{message.text}:customPlugin:{Dev_Zaid}'):
       r.delete(f'{user.id}:setDelp:{chat.id}{Dev_Zaid}')
       return await message.reply_text(f'{k} مافي ميزة بهالأسم')
     else:
       r.srem(f'customPlugins:{Dev_Zaid}', message.text)
       r.delete(f'{message.text}:customPlugin:{Dev_Zaid}')
       r.delete(f'{user.id}:setDelp:{chat.id}{Dev_Zaid}')
       r.delete(f'{message.text}:customPluginD:{Dev_Zaid}{chat.id}')
       return await message.reply_text(f'{k} الميزة ( {message.text} ) مسحتها .')
   
   if text == 'المميزات المضافه':
     if devp_pls(user.id,chat.id):
       if not r.smembers(f'customPlugins:{Dev_Zaid}'):
         return await message.reply_text(f'{k} مافي ولا ميزة مضافة')
       else:
         text = 'المميزات المضافه:\n\n'
         count = 1
         for miza in r.smembers(f'customPlugins:{Dev_Zaid}'):
            text += f'{count}) - {miza}\n'
            count += 1
         text += '\n☆'
         return await message.reply_text(text)
   
   if r.get(f'{message.text}:customPlugin:{Dev_Zaid}'):
      if r.get(f'{message.text}:customPluginD:{Dev_Zaid}{chat.id}'):
         return
      else:
         miza = r.get(f'{message.text}:customPlugin:{Dev_Zaid}')
         type = miza.split('type=')[1].split('&&')[0]
         channel = miza.split('&&channel=')[1].split('&&')[0]
         random1 = int(miza.split('&&random=')[1].split('_')[0])
         random2 = int(miza.split('&&random=')[1].split('_')[1])
         rand = randomessage.randint(random1,random2)
         if type == 'صوره':
            await message.reply_photo(f'https://t.me/{channel}/{rand}')
         
         if type == 'فيديو':
            await message.reply_video(f'https://t.me/{channel}/{rand}')
        
         if type == 'متحركه':
            await message.reply_animation(f'https://t.me/{channel}/{rand}')
         
         if type == 'بصمه':
            await message.reply_voice(f'https://t.me/{channel}/{rand}')
         
         if type == 'صوت':
            await message.reply_audio(f'https://t.me/{channel}/{rand}')
   
   if text.startswith('تعطيل ') and len(text.split()) == 2:
      miza = text.split()[1]
      if r.get(f'{miza}:customPlugin:{Dev_Zaid}'):
        if not owner_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص ( المالك وفوق ) بس') 
        else:
          if r.get(f'{miza}:customPluginD:{Dev_Zaid}{chat.id}'):
            return await message.reply_text(f'{k} من「 {user.mention_html()} 」\n{k} ميزة {miza} معطله من قبل\n☆')
          else:
            r.set(f'{miza}:customPluginD:{Dev_Zaid}{chat.id}',1)
            return await message.reply_text(f'من「 {user.mention_html()} 」\n{k} ابشر عطلت ميزة {miza}\n☆')
   
   if text.startswith('تفعيل ') and len(text.split()) == 2:
      miza = text.split()[1]
      if r.get(f'{miza}:customPlugin:{Dev_Zaid}'):
        if not owner_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص ( المالك وفوق ) بس') 
        else:
          if not r.get(f'{miza}:customPluginD:{Dev_Zaid}{chat.id}'):
            return await message.reply_text(f'{k} من「 {user.mention_html()} 」\n{k} ميزة {miza} مفعله من قبل\n☆')
          else:
            r.delete(f'{miza}:customPluginD:{Dev_Zaid}{chat.id}')
            return await message.reply_text(f'من「 {user.mention_html()} 」\n{k} ابشر فعلت ميزة {miza}\n☆')
   
            
            
          
   
   
   
   
      
   

def register(app):
    """Register custom_plugin handlers."""
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(
        filters.ALL & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
        addPluginHandler
    ), group=15)
