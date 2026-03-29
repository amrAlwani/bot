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

async def getRanksHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'scatteredda'
    await get_ranks_func(update, context, k, channel)
    
async def get_ranks_func(update, context, k, channel):
    
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
   if isLockCommand(user.id, chat.id, text): return
   if text == 'قائمه Dev':
      if not devp_pls(user.id,chat.id):
        return await message.reply_text(f'{k} هذا الامر يخص ( Dev🎖️) بس')
      else:
        if not r.smembers(f'{Dev_Zaid}DEV2'):
           return await message.reply_text(f'{k} مافيه قائمة  Dev²🎖️')
        else:
          text = '- قائمة  Dev²🎖:\n\n'
          count = 1
          for dev2 in r.smembers(f'{Dev_Zaid}DEV2'):
             if count == 101: break
             try:
               user = await context.bot.get_chat(int(dev2))
               mention = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'[@{channel}](tg://user?id={int(dev2)})'
               id = int(dev2)
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          await message.reply_text(text)
   
   if text == 'قائمه MY':
      if not dev2_pls(user.id,chat.id):
        return await message.reply_text(f'{k} هذا الامر يخص ( Dev²🎖️ وفوق ) بس')
      else:
        if not r.smembers(f'{Dev_Zaid}DEV'):
          return await message.reply_text(f'{k}  مافيه Myth🎖️ ')
        else:
          text = '- قائمة Myth🎖️:\n\n'
          count = 1
          for dev in r.smembers(f'{Dev_Zaid}DEV'):
             if count == 101: break
             try:
               user = await context.bot.get_chat(int(dev))
               mention = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'[@{channel}](tg://user?id={int(dev)})'
               id = int(dev)
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          await message.reply_text(text)
          
   cid = chat.id
   if text == 'المالكين الاساسيين':
      if not dev_pls(user.id,chat.id):
        return await message.reply_text(f'{k} هذا الامر يخص ( المطور وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listGOWNER:{Dev_Zaid}'):
          return await message.reply_text(f'{k} مافيه مالكين اساسيين ')
        else:
          text = '- المالكين الاساسيين:\n\n'
          count = 1
          for gowner in r.smembers(f'{cid}:listGOWNER:{Dev_Zaid}'):
             if count == 101: break
             try:
               user = await context.bot.get_chat(int(gowner))
               mention = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'[@{channel}](tg://user?id={int(gowner)})'
               id = int(gowner)
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          await message.reply_text(text)
          
   if text == 'المالكين':
      if not gowner_pls(user.id,chat.id):
        return await message.reply_text(f'{k} هذا الامر يخص ( المالك الاساسي ) بس')
      else:
        if not r.smembers(f'{cid}:listOWNER:{Dev_Zaid}'):
          return await message.reply_text(f'{k} مافيه مالكيين ')
        else:
          text = '- المالكيين:\n\n'
          count = 1
          for owner in r.smembers(f'{cid}:listOWNER:{Dev_Zaid}'):
             if count == 101: break
             try:
               user = await context.bot.get_chat(int(owner))
               mention = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'[@{channel}](tg://user?id={int(owner)})'
               id = int(owner)
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          await message.reply_text(text)
   
   if text == 'المدراء':
      if not owner_pls(user.id,chat.id):
        return await message.reply_text(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listMOD:{Dev_Zaid}'):
          return await message.reply_text(f'{k} مافيه مدراء ')
        else:
          text = '- المدراء:\n\n'
          count = 1
          for mod in r.smembers(f'{cid}:listMOD:{Dev_Zaid}'):
             if count == 101: break
             try:
               user = await context.bot.get_chat(int(mod))
               mention = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'[@{channel}](tg://user?id={int(mod)})'
               id = int(mod)
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          await message.reply_text(text)
   
   if text == 'الادمنيه':
      if not mod_pls(user.id,chat.id):
        return await message.reply_text(f'{k} هذا الامر يخص ( المدير وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listADMIN:{Dev_Zaid}'):
          return await message.reply_text(f'{k} مافيه ادمن ')
        else:
          text = '- الادمنيه:\n\n'
          count = 1
          for ADM in r.smembers(f'{cid}:listADMIN:{Dev_Zaid}'):
             if count == 101: break
             try:
               user = await context.bot.get_chat(int(ADM))
               mention = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'[@{channel}](tg://user?id={int(ADM)})'
               id = int(ADM)
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          await message.reply_text(text)
   
   if text == 'المشرفين':
      if not owner_pls(user.id,chat.id):
        return await message.reply_text(f'{k} هذا الامر يخص ( المالك وفوق ) بس')
      else:
          text = '- المشرفين:\n\n'
          count = 1
          for mm in chat.get_members(filter=ChatMembersFilter.ADMINISTRATORS):
            if count == 101: break
            if not mmessage.user.is_deleted and not mmessage.user.is_bot:
               id = mmessage.user.id
               username = mmessage.user.username
               if mmessage.user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ [@{channel}](tg://user?id={id}) ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          await message.reply_text(text)
   
   if text == 'المميزين':
      if not admin_pls(user.id,chat.id):
        return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listPRE:{Dev_Zaid}'):
          return await message.reply_text(f'{k} مافيه مميزين ')
        else:
          text = '- المميزين:\n\n'
          count = 1
          for PRE in r.smembers(f'{cid}:listPRE:{Dev_Zaid}'):
             if count == 101: break
             try:
               user = await context.bot.get_chat(int(PRE))
               mention = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
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
          await message.reply_text(text)
   
   if text == 'المكتومين':
      if not mod_pls(user.id,chat.id):
        return await message.reply_text(f'{k} هذا الامر يخص ( المدير وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listMUTE:{Dev_Zaid}'):
          return await message.reply_text(f'{k} مافيه مكتومين ')
        else:
          text = '- المكتومين:\n\n'
          count = 1
          for PRE in r.smembers(f'{cid}:listMUTE:{Dev_Zaid}'):
             if count == 101: break
             try:
               user = await context.bot.get_chat(int(PRE))
               mention = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
               id = user.id
               username = user.username
               if user.username:
                 text += f'{count} ➣ @{username} ࿓ ( `{id}` )\n'
               else:
                 text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
             except:
               mention = f'[@{channel}](tg://user?id={PRE})'
               id = PRE
               text += f'{count} ➣ {mention} ࿓ ( `{id}` )\n'
               count += 1
          text += '\n☆'
          await message.reply_text(text)
   
   

             
        
        

def register(app):
    """Register get_ranks handlers."""
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(
        filters.TEXT & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
        getRanksHandler
    ), group=8)
