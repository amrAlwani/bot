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


async def ranksCommandsHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
   k = r.get(f'{Dev_Zaid}:botkey') or '☆'
   await ranks_reply_promote(update, context, k)
   await ranks_reply_demote(update, context, k)
   

async def ranks_reply_promote(update, context, k):
    message = update.message
    chat = update.effective_chat
    user = update.effective_user
    if not message or not chat or not user: return
    if not r.get(f'{chat.id}:enable:{Dev_Zaid}') and not dev_pls(user.id, chat.id):  return
    if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return 
    if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
    if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
    if r.get(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}'):  return 
    if r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}'):  return 
    if r.get(f'{chat.id}:delCustom:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:delCustomG:{user.id}{Dev_Zaid}'):  return 
    text = message.text
    name = r.get(f'{Dev_Zaid}:BotName') or NAME
    if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
    if r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}'):
       text = r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}')
    if r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')
    if isLockCommand(user.id, chat.id, text): return
    if text == 'تعطيل الرفع':
      if not owner_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
      else:
        if r.get(f'{chat.id}:disableRanks:{Dev_Zaid}'):
          return await message.reply_text(f'{k} من「 {user.mention_html()} 」\n{k} الرفع معطل من قبل\n☆')
        else:
          r.set(f'{chat.id}:disableRanks:{Dev_Zaid}', 1)
          return await message.reply_text(f'{k} من「 {user.mention_html()} 」\n{k} ابشر عطلت الرفع\n☆')
    
    if text == 'تفعيل الرفع':
      if not owner_pls(user.id, chat.id):
        return await message.reply_text(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
      else:
        if not r.get(f'{chat.id}:disableRanks:{Dev_Zaid}'):
          return await message.reply_text(f'「 {user.mention_html()} 」\n{k} الرفع مفعل من قبل\n☆')
        else:
          r.delete(f'{chat.id}:disableRanks:{Dev_Zaid}')
          return await message.reply_text(f'{k} من「 {user.mention_html()} 」\n{k} ابشر فعلت الرفع\n☆')
    
    cid = chat.id
    
    if r.get(f'{chat.id}:disableRanks:{Dev_Zaid}'):  return
    rank = get_rank(user.id, chat.id)
    if text.startswith('رفع Dev '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not devp_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص ( Dev🎖️) بس')
        if len(text.split()) == 4:
           user = text.split()[3]
           if user.startswith('@'):
              try:
                 get = context.bot.get_chat(user)
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = context.bot.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if message.reply_to_message and message.reply_to_message.from_user:
           id = message.reply_to_message.from_user.id
           mention = message.reply_to_message.from_user.first_name
        '''
        if id == user.id:
           return await message.reply_text(f'{k} هطف تبي ترفع نفسك؟')
        
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف ارفع نفسي')
        
           
        if r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} Dev²🎖 من قبل\n☆')
        else:
          r.set(f'{id}:rankDEV2:{Dev_Zaid}', 1)
          r.sadd(f'{Dev_Zaid}DEV2', id)
          return await message.reply_text(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار Dev²🎖\n☆')
          if r.get(f'{id}:mute:{Dev_Zaid}'):
            r.delete(f'{id}:mute:{Dev_Zaid}')
            r.srem(f'listMUTE:{Dev_Zaid}', id)
          if r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{chat.id}{Dev_Zaid}')
            r.srem(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text == 'رفع Dev' and message.reply_to_message and message.reply_to_message.from_user:
        if not devp_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص ( Dev🎖️) بس')
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if id == user.id:
           return await message.reply_text(f'{k} هطف تبي ترفع نفسك؟')        
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف ارفع نفسي')           
        if r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} Dev²🎖 من قبل\n☆')
        else:
          r.set(f'{id}:rankDEV2:{Dev_Zaid}', 1)
          r.sadd(f'{Dev_Zaid}DEV2', id)
          return await message.reply_text(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار Dev²🎖\n☆')
          if r.get(f'{id}:mute:{Dev_Zaid}'):
            r.delete(f'{id}:mute:{Dev_Zaid}')
            r.srem(f'listMUTE:{Dev_Zaid}', id)
          if r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{chat.id}{Dev_Zaid}')
            r.srem(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
          
    if text.startswith('رفع MY '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return False
        if not dev2_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الامر يخص ( Dev²🎖️ وفوق ) بس')
        if len(text.split()) == 3:
           user = text.split()[2]
           if user.startswith('@'):
              try:
                 get = context.bot.get_chat(user)
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = context.bot.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if message.reply_to_message and message.reply_to_message.from_user:
           id = message.reply_to_message.from_user.id
           mention = message.reply_to_message.from_user.first_name
        '''
        if id == user.id:
           return await message.reply_text(f'{k} هطف تبي ترفع نفسك؟')
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف ارفع نفسي')
        
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
        if r.get(f'{id}:rankDEV:{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} Myth🎖️ من قبل\n☆')
        else:
          r.set(f'{id}:rankDEV:{Dev_Zaid}', 1)
          r.sadd(f'{Dev_Zaid}DEV', id)
          await message.reply_text(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار Myth🎖️\n☆')
          if r.get(f'{id}:mute:{Dev_Zaid}'):
            r.delete(f'{id}:mute:{Dev_Zaid}')
            r.srem(f'listMUTE:{Dev_Zaid}', id)
          if r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{chat.id}{Dev_Zaid}')
            r.srem(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text == 'رفع MY' and message.reply_to_message and message.reply_to_message.from_user:
        if not dev2_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الامر يخص ( Dev²🎖️ وفوق ) بس')
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if id == user.id:
           return await message.reply_text(f'{k} هطف تبي ترفع نفسك؟')
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف ارفع نفسي')        
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
        if r.get(f'{id}:rankDEV:{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} Myth🎖️ من قبل\n☆')
        else:
          r.set(f'{id}:rankDEV:{Dev_Zaid}', 1)
          r.sadd(f'{Dev_Zaid}DEV', id)
          await message.reply_text(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار Myth🎖️\n☆')
          if r.get(f'{id}:mute:{Dev_Zaid}'):
            r.delete(f'{id}:mute:{Dev_Zaid}')
            r.srem(f'listMUTE:{Dev_Zaid}', id)
          if r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{chat.id}{Dev_Zaid}')
            r.srem(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
    
    cid = chat.id
    
    if text.startswith('رفع مالك اساسي '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not gowner_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص ( المالك الاساسي وفوق ) بس')
        if len(text.split()) == 4:
           user = text.split()[3]
           if user.startswith('@'):
              try:
                 get = context.bot.get_chat(user)
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = context.bot.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if message.reply_to_message and message.reply_to_message.from_user:
           id = message.reply_to_message.from_user.id
           mention = message.reply_to_message.from_user.first_name
        '''
        if id == user.id:
           return await message.reply_text(f'{k} هطف تبي ترفع نفسك؟')
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف ارفع نفسي')
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')           
        if r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مالك اساسي من قبل\n☆')
        else:
          r.set(f'{cid}:rankGOWNER:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listGOWNER:{Dev_Zaid}', id)
          await message.reply_text(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مالك اساسي\n☆')
          if r.get(f'{id}:mute:{Dev_Zaid}'):
            r.delete(f'{id}:mute:{Dev_Zaid}')
            r.srem(f'listMUTE:{Dev_Zaid}', id)
          if r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{chat.id}{Dev_Zaid}')
            r.srem(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
          return 
    
    if text == 'رفع مالك اساسي' and message.reply_to_message and message.reply_to_message.from_user:
        if not gowner_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص (المالك الاساسي وفوق) بس')
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name       
        if id == user.id:
           return await message.reply_text(f'{k} هطف تبي ترفع نفسك؟')
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف ارفع نفسي')
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')           
        if r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مالك اساسي من قبل\n☆')
        else:
          r.set(f'{cid}:rankGOWNER:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listGOWNER:{Dev_Zaid}', id)
          await message.reply_text(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مالك اساسي\n☆')
          if r.get(f'{id}:mute:{Dev_Zaid}'):
            r.delete(f'{id}:mute:{Dev_Zaid}')
            r.srem(f'listMUTE:{Dev_Zaid}', id)
          if r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{chat.id}{Dev_Zaid}')
            r.srem(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
          return 
    
    if text.startswith('رفع مالك '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not gowner_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص ( المالك الاساسي ) بس')
        if len(text.split()) == 3:
           user = text.split()[2]
           if user.startswith('@'):
              try:
                 get = context.bot.get_chat(user)
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = context.bot.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if message.reply_to_message and message.reply_to_message.from_user:
           id = message.reply_to_message.from_user.id
           mention = message.reply_to_message.from_user.first_name
        '''
        if id == user.id:
           return await message.reply_text(f'{k} هطف تبي ترفع نفسك؟')
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف ارفع نفسي')
        
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
        if r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مالك من قبل\n☆')
        else:
          r.set(f'{cid}:rankOWNER:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listOWNER:{Dev_Zaid}', id)
          await message.reply_text(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مالك\n☆')
          if r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{chat.id}{Dev_Zaid}')
            r.srem(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text == 'رفع مالك' and message.reply_to_message and message.reply_to_message.from_user:
        if not gowner_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص ( المالك الاساسي ) بس')
        if message.reply_to_message and message.reply_to_message.from_user:
           id = message.reply_to_message.from_user.id
           mention = message.reply_to_message.from_user.first_name
        if id == user.id:
           return await message.reply_text(f'{k} هطف تبي ترفع نفسك؟')
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف ارفع نفسي')
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
        if r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مالك من قبل\n☆')
        else:
          r.set(f'{cid}:rankOWNER:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listOWNER:{Dev_Zaid}', id)
          await message.reply_text(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مالك\n☆')
          if r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{chat.id}{Dev_Zaid}')
            r.srem(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
    
    
    if text.startswith('رفع مدير '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not owner_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
        if len(text.split()) == 3:
           user = text.split()[2]
           if user.startswith('@'):
              try:
                 get = context.bot.get_chat(user)
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = context.bot.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if message.reply_to_message and message.reply_to_message.from_user:
           id = message.reply_to_message.from_user.id
           mention = message.reply_to_message.from_user.first_name
        '''
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف ارفع نفسي')
        if id == user.id:
           return await message.reply_text(f'{k} هطف تبي ترفع نفسك؟')
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')           
        if r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مدير من قبل\n☆')
        else:
          r.set(f'{cid}:rankMOD:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listMOD:{Dev_Zaid}', id)
          await message.reply_text(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مدير\n☆')
          if r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{chat.id}{Dev_Zaid}')
            r.srem(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text == 'رفع مدير' and message.reply_to_message and message.reply_to_message.from_user:
        if not owner_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف ارفع نفسي')
        if id == user.id:
           return await message.reply_text(f'{k} هطف تبي ترفع نفسك؟')
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')           
        if r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مدير من قبل\n☆')
        else:
          r.set(f'{cid}:rankMOD:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listMOD:{Dev_Zaid}', id)
          await message.reply_text(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مدير\n☆')
          if r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{chat.id}{Dev_Zaid}')
            r.srem(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text.startswith('رفع ادمن '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not mod_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الامر يخص ( المدير وفوق ) بس')
        if len(text.split()) == 3:
           user = text.split()[2]
           if user.startswith('@'):
              try:
                 get = context.bot.get_chat(user)
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = context.bot.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if message.reply_to_message and message.reply_to_message.from_user:
           id = message.reply_to_message.from_user.id
           mention = message.reply_to_message.from_user.first_name
        '''
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف ارفع نفسي')
        if id == user.id:
           return await message.reply_text(f'{k} هطف تبي ترفع نفسك؟')
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
           
        if r.get(f'{cid}:rankADMIN:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} ادمن من قبل\n☆')
        else:
          r.set(f'{cid}:rankADMIN:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listADMIN:{Dev_Zaid}', id)
          await message.reply_text(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار ادمن\n☆')
          if r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{chat.id}{Dev_Zaid}')
            r.srem(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text == 'رفع ادمن' and message.reply_to_message and message.reply_to_message.from_user:        
        if not mod_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الامر يخص ( المدير وفوق ) بس')
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف ارفع نفسي')
        if id == user.id:
           return await message.reply_text(f'{k} هطف تبي ترفع نفسك؟')
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
           
        if r.get(f'{cid}:rankADMIN:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} ادمن من قبل\n☆')
        else:
          r.set(f'{cid}:rankADMIN:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listADMIN:{Dev_Zaid}', id)
          await message.reply_text(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار ادمن\n☆')
          if r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{chat.id}{Dev_Zaid}')
            r.srem(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text.startswith('رفع مميز '):
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not admin_pls(user.id,chat.id):
        return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
      else:
        if len(text.split()) == 3:
           user = text.split()[2]
           if user.startswith('@'):
              try:
                 get = context.bot.get_chat(user)
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = context.bot.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if message.reply_to_message and message.reply_to_message.from_user:
           id = message.reply_to_message.from_user.id
           mention = message.reply_to_message.from_user.first_name
        '''
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف ارفع نفسي')
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
        if id == user.id:
           return await message.reply_text(f'{k} هطف تبي ترفع نفسك؟')
        if r.get(f'{cid}:rankPRE:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مميز من قبل\n☆')
        else:
          r.set(f'{cid}:rankPRE:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listPRE:{Dev_Zaid}', id)
          await message.reply_text(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مميز\n☆')
          if r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{chat.id}{Dev_Zaid}')
            r.srem(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
    
    if text == 'رفع مميز' and message.reply_to_message and message.reply_to_message.from_user:
      if not admin_pls(user.id,chat.id):
        return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
      else:
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف ارفع نفسي')
        if id == user.id:
           return await message.reply_text(f'{k} هطف تبي ترفع نفسك؟')
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
        if r.get(f'{cid}:rankPRE:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مميز من قبل\n☆')
        else:
          r.set(f'{cid}:rankPRE:{id}{Dev_Zaid}', 1)
          r.sadd(f'{cid}:listPRE:{Dev_Zaid}', id)
          await message.reply_text(f'{k} الحلو 「 {mention} 」\n{k} رفعته صار مميز\n☆')
          if r.get(f'{id}:mute:{chat.id}{Dev_Zaid}'):
            r.delete(f'{id}:mute:{chat.id}{Dev_Zaid}')
            r.srem(f'{chat.id}:listMUTE:{Dev_Zaid}', id)
          
    
    
    
async def ranks_reply_demote(update, context, k):
    message = update.message
    chat = update.effective_chat
    user = update.effective_user
    if not message or not chat or not user: return
    if not r.get(f'{chat.id}:enable:{Dev_Zaid}') and not dev_pls(user.id, chat.id):  return
    if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return 
    if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
    if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
    if r.get(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}'):  return 
    if r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}'):  return 
    if r.get(f'{chat.id}:delCustom:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:delCustomG:{user.id}{Dev_Zaid}'):  return 
    text = message.text
    name = r.get(f'{Dev_Zaid}:BotName') or NAME
    if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
    if r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}'):
       text = r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}')
    if r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')
    if isLockCommand(user.id, chat.id, text): return
    rank = get_rank(user.id, chat.id)
    cid = chat.id
    
    if text == 'تنزيل Dev' and message.reply_to_message and message.reply_to_message.from_user:
        if not devp_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الامر يخص ( Dev🎖️) بس')
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name     
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف انزل نفسي')           
        if not r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو Dev²🎖\n☆')
        else:
          r.delete(f'{id}:rankDEV2:{Dev_Zaid}')
          r.srem(f'{Dev_Zaid}DEV2', id)
          return await message.reply_text(f'「 {mention} 」\n{k} نزلته من Dev²🎖\n☆')
    
    if text.startswith('تنزيل Dev '):
      if not '@' in text and not re.findall('[0-9]+', text):
          return
      if not devp_pls(user.id,chat.id):
        return await message.reply_text(f'{k} هذا الامر يخص ( Dev🎖️) بس')
      else:
        if len(text.split()) == 4:
           user = text.split()[3]
           if user.startswith('@'):
              try:
                 get = context.bot.get_chat(user)
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = context.bot.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if message.reply_to_message and message.reply_to_message.from_user:
           id = message.reply_to_message.from_user.id
           mention = message.reply_to_message.from_user.first_name
        '''
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف انزل نفسي')           
        if not r.get(f'{id}:rankDEV2:{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو Dev²🎖\n☆')
        else:
          r.delete(f'{id}:rankDEV2:{Dev_Zaid}')
          r.srem(f'{Dev_Zaid}DEV2', id)
          return await message.reply_text(f'「 {mention} 」\n{k} نزلته من Dev²🎖\n☆')
          
    if text == 'تنزيل MY'  and message.reply_to_message and message.reply_to_message.from_user:
        if not dev2_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص ( Dev²🎖️ وفوق ) بس')
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف انزل نفسي')        
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')           
        if not r.get(f'{id}:rankDEV:{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو Myth🎖️ من قبل\n☆')
        else:
          r.delete(f'{id}:rankDEV:{Dev_Zaid}')
          r.srem(f'{Dev_Zaid}DEV', id)
          return await message.reply_text(f'「 {mention} 」\n{k} نزلته من Myth🎖️\n☆')
    
    if text.startswith('تنزيل MY '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not dev2_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص ( Dev²🎖️ وفوق ) بس')
        if len(text.split()) == 3:
           user = text.split()[2]
           if user.startswith('@'):
              try:
                 get = context.bot.get_chat(user)
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = context.bot.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if message.reply_to_message and message.reply_to_message.from_user:
           id = message.reply_to_message.from_user.id
           mention = message.reply_to_message.from_user.first_name
        '''
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف انزل نفسي')
        
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
           
        if not r.get(f'{id}:rankDEV:{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو Myth🎖️ من قبل\n☆')
        else:
          r.delete(f'{id}:rankDEV:{Dev_Zaid}')
          r.srem(f'{Dev_Zaid}DEV', id)
          return await message.reply_text(f'「 {mention} 」\n{k} نزلته من Myth🎖️\n☆')
    
    
    
    if text == 'تنزيل مالك اساسي' and message.reply_to_message and message.reply_to_message.from_user:
        if not gowner_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الامر يخص (المالك الاساسي وفوق) بس')
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name        
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف انزل نفسي')
        if not r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو مالك اساسي\n☆')
        else:
          r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} نزلته من المالك الاساسي\n☆')
    
    if text.startswith('تنزيل مالك اساسي '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not gowner_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الامر يخص (المالك الاساسي وفوق) بس')
        if len(text.split()) == 4:
           user = text.split()[3]
           if user.startswith('@'):
              try:
                 get = context.bot.get_chat(user)
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = context.bot.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا الآيدي')
        '''
        if message.reply_to_message and message.reply_to_message.from_user:
           id = message.reply_to_message.from_user.id
           mention = message.reply_to_message.from_user.first_name
        '''
        
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف انزل نفسي')
        if not r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو مالك اساسي\n☆')
        else:
          r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} نزلته من المالك الاساسي\n☆')
    
    
    if text.startswith('تنزيل مالك '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return
        if not gowner_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الامر يخص ( المالك الاساسي ) بس')
        if len(text.split()) == 3:
           user = text.split()[2]
           if user.startswith('@'):
              try:
                 get = context.bot.get_chat(user)
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = context.bot.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا الآيدي')        
        '''
        if message.reply_to_message and message.reply_to_message.from_user:
           id = message.reply_to_message.from_user.id
           mention = message.reply_to_message.from_user.first_name
        '''        
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف انزل نفسي')        
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')        
        if not r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو مالك من قبل\n☆')
        else:
          r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} نزلته من المالك \n☆')
    
    if text == 'تنزيل مالك' and message.reply_to_message and message.reply_to_message.from_user:    
        
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name     
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف انزل نفسي')        
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')        
        if not r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو مالك من قبل\n☆')
        else:
          r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} نزلته من المالك \n☆')

    if text.startswith('تنزيل مدير '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return 
        if not owner_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
        if len(text.split()) == 3:
           user = text.split()[2]
           if user.startswith('@'):
              try:
                 get = context.bot.get_chat(user)
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = context.bot.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا الآيدي')
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف انزل نفسي')
        
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
           
        if not r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو مدير من قبل\n☆')
        else:
          r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} نزلته من رتبة المدير \n☆')
    
    if text == 'تنزيل مدير' and message.reply_to_message and message.reply_to_message.from_user:
        if not owner_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف انزل نفسي')
        
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
           
        if not r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو مدير من قبل\n☆')
        else:
          r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} نزلته من رتبة المدير \n☆')
    
    if text.startswith('تنزيل ادمن '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return 
        if not mod_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص ( المدير وفوق ) بس')
        if len(text.split()) == 3:
           user = text.split()[2]
           if user.startswith('@'):
              try:
                 get = context.bot.get_chat(user)
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = context.bot.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا الآيدي')
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف انزل نفسي')
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
        if not r.get(f'{cid}:rankADMIN:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو ادمن من قبل\n☆')
        else:
          r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} نزلته من رتبة الادمن \n☆')
    
    if text == 'تنزيل ادمن' and message.reply_to_message and message.reply_to_message.from_user:
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف انزل نفسي')
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
        if not r.get(f'{cid}:rankADMIN:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو ادمن من قبل\n☆')
        else:
          r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} نزلته من رتبة الادمن \n☆')
    
    if text.startswith('تنزيل مميز '):
        if not '@' in text and not re.findall('[0-9]+', text):
          return 
        if not admin_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
        if len(text.split()) == 3:
           user = text.split()[2]
           if user.startswith('@'):
              try:
                 get = context.bot.get_chat(user)
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = context.bot.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا الآيدي')
        
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف انزل نفسي')
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
        if not r.get(f'{cid}:rankPRE:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو مميز من قبل\n☆')
        else:
          r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} نزلته من المميزين \n☆')
    
    if text == 'تنزيل مميز' and message.reply_to_message and message.reply_to_message.from_user:
        if not admin_pls(user.id,chat.id):
           return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
        id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.first_name
        if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف انزل نفسي')
        if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
        if not r.get(f'{cid}:rankPRE:{id}{Dev_Zaid}'):
          return await message.reply_text(f'「 {mention} 」\n{k} مو مميز من قبل\n☆')
        else:
          r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
          r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
          return await message.reply_text(f'「 {mention} 」\n{k} نزلته من المميزين \n☆')
    
    if text.startswith('تنزيل الكل '):
       if not '@' in text and not re.findall('[0-9]+', text):
          return 
       if not mod_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص ( المدير وفوق ) بس')
       
       if len(text.split()) == 3:
           user = text.split()[2]
           if user.startswith('@'):
              try:
                 get = context.bot.get_chat(user)
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا اليوزر')
           else:
              try:
                 get = context.bot.get_chat(int(user))
                 mention = f'[{get.first_name}](tg://user?id={get.id})'
                 id = get.id
              except:
                 return await message.reply_text(f'{k} مافيه عضو بهذا الآيدي')
       
       if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
       if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف انزل نفسي')
       if devp_pls(user.id,chat.id):
          rank = get_rank(id,cid)
          if id == user.id:
             return await message.reply_text(f'{k} مافيك تنزل نفسك')
          if not rank == 'عضو' and not id in [6168217372]:
              await message.reply_text(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{id}:rankDEV2:{Dev_Zaid}')
              r.srem(f'{Dev_Zaid}DEV2', id)
              r.delete(f'{id}:rankDEV:{Dev_Zaid}')
              r.srem(f'{Dev_Zaid}DEV', id)
              r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887]:
              return await message.reply_text(f'{k} مايمديك تستخدم الأمر على مبرمج السورس')
          else:
              return await message.reply_text(f'{k} ماله رتبة')
       
       if dev2_pls(user.id, chat.id):
          rank = get_rank(id,cid)
          if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372]:
              await message.reply_text(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{id}:rankDEV:{Dev_Zaid}')
              r.srem(f'{Dev_Zaid}DEV', id)
              r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')):
              return await message.reply_text(f'{k} رتبته اعلى منك')
          else:
              return await message.reply_text(f'{k} ماله رتبة')

       if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372] and not r.get(
               f'{id}:rankDEV2:{Dev_Zaid}'):
           await message.reply_text(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
           r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
           r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
           r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
           r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
           r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
           r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
           r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
           r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
           r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
           r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
           return
       if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
               f'{id}:rankDEV2:{Dev_Zaid}'):
           return await message.reply_text(f'{k} رتبته اعلى منك')
       else:
           return await message.reply_text(f'{k} ماله رتبة')
       
       if gowner_pls(user.id, chat.id):
          rank = get_rank(id,cid)
          if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372] and not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') and not r.get(f'{id}:rankDEV:{Dev_Zaid}'):
              await message.reply_text(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') or r.get(f'{id}:rankDEV:{Dev_Zaid}'):
              return await message.reply_text(f'{k} رتبته اعلى منك')
          else:
              return await message.reply_text(f'{k} ماله رتبة')
       
       if owner_pls(user.id, chat.id):
          rank = get_rank(id,cid)
          if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372] and not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') and not r.get(f'{id}:rankDEV:{Dev_Zaid}') and not r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
              await message.reply_text(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') or r.get(f'{id}:rankDEV:{Dev_Zaid}') or r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
              return await message.reply_text(f'{k} رتبته اعلى منك')
          else:
              return await message.reply_text(f'{k} ماله رتبة')
       
       if mod_pls(user.id, chat.id):
          rank = get_rank(id,cid)
          if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372] and not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') and not r.get(f'{id}:rankDEV:{Dev_Zaid}') and not r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
              await message.reply_text(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') or r.get(f'{id}:rankDEV:{Dev_Zaid}') or r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
              return await message.reply_text(f'{k} رتبته اعلى منك')
          else:
              return await message.reply_text(f'{k} ماله رتبة')
       
       if admin_pls(user.id, chat.id):
          rank = get_rank(id,cid)
          if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372] and not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') and not r.get(f'{id}:rankDEV:{Dev_Zaid}') and not r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_Zaid}') and not r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
              await message.reply_text(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') or r.get(f'{id}:rankDEV:{Dev_Zaid}') or r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_Zaid}') or r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
              return await message.reply_text(f'{k} رتبته اعلى منك')
          else:
              return await message.reply_text(f'{k} ماله رتبة')
    
    
    if text == 'تنزيل الكل' and message.reply_to_message and message.reply_to_message.from_user:
       if not owner_pls(user.id,chat.id):
          return await message.reply_text(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
       
       id = message.reply_to_message.from_user.id
       mention= message.reply_to_message.from_user.first_name
       
       if rank == get_rank(id, cid):
           return await message.reply_text('نفس رتبتك ترا')
       if id == int(Dev_Zaid):
           return await message.reply_text('ركز حبيبي كيف انزل نفسي')
       if devp_pls(user.id,chat.id):
          rank = get_rank(id,cid)
          if id == user.id:
             return await message.reply_text(f'{k} مافيك تنزل نفسك')
          if not rank == 'عضو' and not id in [6168217372]:
              await message.reply_text(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{id}:rankDEV2:{Dev_Zaid}')
              r.srem(f'{Dev_Zaid}DEV2', id)
              r.delete(f'{id}:rankDEV:{Dev_Zaid}')
              r.srem(f'{Dev_Zaid}DEV', id)
              r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887]:
              return await message.reply_text(f'{k} مايمديك تستخدم الأمر على مبرمج السورس')
          else:
             return await message.reply_text(f'{k} ماله رتبة')
       
       if dev2_pls(user.id, chat.id):
          rank = get_rank(id,cid)
          if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372]:
              await message.reply_text(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{id}:rankDEV:{Dev_Zaid}')
              r.srem(f'{Dev_Zaid}DEV', id)
              r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')):
              return await message.reply_text(f'{k} رتبته اعلى منك')
          else:
              return await message.reply_text(f'{k} ماله رتبة')
       
       if dev_pls(user.id, chat.id):
          rank = get_rank(id,cid)
          if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372] and not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}'):
              await message.reply_text(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{cid}:rankGOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}'):
              return await message.reply_text(f'{k} رتبته اعلى منك')
          else:
              return await message.reply_text(f'{k} ماله رتبة')

       if gowner_pls(user.id, chat.id):
           rank = get_rank(id, cid)
           if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [
               6168217372] and not r.get(f'{id}:rankDEV2:{Dev_Zaid}') and not r.get(f'{id}:rankDEV:{Dev_Zaid}'):
               await message.reply_text(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
               r.delete(f'{cid}:rankOWNER:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listOWNER:{Dev_Zaid}', id)
               r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
               r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
               r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
               return
           if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                   f'{id}:rankDEV2:{Dev_Zaid}') or r.get(f'{id}:rankDEV:{Dev_Zaid}'):
               return await message.reply_text(f'{k} رتبته اعلى منك')
           else:
               return await message.reply_text(f'{k} ماله رتبة')
       
       if owner_pls(user.id, chat.id):
          rank = get_rank(id,cid)
          if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [6168217372] and not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') and not r.get(f'{id}:rankDEV:{Dev_Zaid}') and not r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
              await message.reply_text(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
              r.delete(f'{cid}:rankMOD:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listMOD:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
              r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
              r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
              return
          if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                  f'{id}:rankDEV2:{Dev_Zaid}') or r.get(f'{id}:rankDEV:{Dev_Zaid}') or r.get(
                  f'{cid}:rankGOWNER:{id}{Dev_Zaid}'):
              return await message.reply_text(f'{k} رتبته اعلى منك')
          else:
              return await message.reply_text(f'{k} ماله رتبة')

       if mod_pls(user.id, chat.id):
           rank = get_rank(id, cid)
           if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [
               6168217372] and not r.get(f'{id}:rankDEV2:{Dev_Zaid}') and not r.get(
                   f'{id}:rankDEV:{Dev_Zaid}') and not r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}') and not r.get(
                   f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
               await message.reply_text(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
               r.delete(f'{cid}:rankADMIN:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listADMIN:{Dev_Zaid}', id)
               r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
               return
           if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or not r.get(
                   f'{id}:rankDEV2:{Dev_Zaid}') or r.get(f'{id}:rankDEV:{Dev_Zaid}') or r.get(
                   f'{cid}:rankGOWNER:{id}{Dev_Zaid}') or r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}'):
               return await message.reply_text(f'{k} رتبته اعلى منك')
           else:
               return await message.reply_text(f'{k} ماله رتبة')

       if admin_pls(user.id, chat.id):
           rank = get_rank(id, cid)
           if not rank == 'عضو' and not id == int(r.get(f'{Dev_Zaid}botowner')) and not id in [
               6168217372] and not r.get(f'{id}:rankDEV2:{Dev_Zaid}') and not r.get(
                   f'{id}:rankDEV:{Dev_Zaid}') and not r.get(f'{cid}:rankGOWNER:{id}{Dev_Zaid}') and not r.get(
                   f'{cid}:rankOWNER:{id}{Dev_Zaid}') and not r.get(f'{cid}:rankMOD:{id}{Dev_Zaid}'):
               await message.reply_text(f'「 {mention} 」\n{k} نزلته من {rank} \n☆')
               r.delete(f'{cid}:rankPRE:{id}{Dev_Zaid}')
               r.srem(f'{cid}:listPRE:{Dev_Zaid}', id)
               return
           if id in [6168217372, 5117901887] or id == int(r.get(f'{Dev_Zaid}botowner')) or r.get(
                   f'{id}:rankDEV2:{Dev_Zaid}') or r.get(f'{id}:rankDEV:{Dev_Zaid}') or r.get(
                   f'{cid}:rankGOWNER:{id}{Dev_Zaid}') or r.get(f'{cid}:rankOWNER:{id}{Dev_Zaid}') or r.get(
                   f'{cid}:rankMOD:{id}{Dev_Zaid}'):
               return await message.reply_text(f'{k} رتبته اعلى منك')
           else:
               return await message.reply_text(f'{k} ماله رتبة')

def register(app):
    """Register set_ranks handlers."""
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(
        filters.TEXT & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
        ranksCommandsHandler
    ), group=7)
