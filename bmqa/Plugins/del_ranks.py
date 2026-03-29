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


async def delRanksHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await del_ranks_func(update, context, k)
    

async def del_ranks_func(update, context, k):
    

   message = update.message
    

   chat = update.effective_chat
    

   user = update.effective_user
   if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):  return
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
   if isLockCommand(user.id, chat.id, text): return
   id = user.id
   cid = chat.id
   demoted = '''{} ابشر عيني {}
{} مسحت ( {} ) من {} 
☆
'''
   if text == 'مسح قائمه Dev':
      if not devp_pls(id, cid):
        return await message.reply_text(f'{k} هذا الامر يخص ( Dev🎖️) بس')
      else:
        if not r.smembers(f'{Dev_Zaid}DEV2'):
          return await message.reply_text(f'{k} مافيه قائمة Dev²🎖')
        else:
          count = 0
          for dev2 in r.smembers(f'{Dev_Zaid}DEV2'):
             r.srem(f'{Dev_Zaid}DEV2', int(dev2))
             r.delete(f'{int(dev2)}:rankDEV2:{Dev_Zaid}')
             count += 1
          await message.reply_text(demoted.format(k,get_rank(id,cid),k,count,'قائمة Dev'))
   
   if text == 'مسح قائمه MY':
      if not dev2_pls(id, cid):
        return await message.reply_text(f'{k} هذا الأمر يخص ( Dev²🎖️ وفوق ) بس')
      else:
        if not r.smembers(f'{Dev_Zaid}DEV'):
          return await message.reply_text(f'{k} مافيه قائمة Myth🎖️')
        else:
          count = 0
          for dev in r.smembers(f'{Dev_Zaid}DEV'):
             r.srem(f'{Dev_Zaid}DEV', int(dev))
             r.delete(f'{int(dev)}:rankDEV:{Dev_Zaid}')
             count += 1
          await message.reply_text(demoted.format(k,get_rank(id,cid),k,count,'قائمة MY'))
   
   if text == 'مسح المالكين الاساسيين':
      if not dev_pls(id, cid):
        return await message.reply_text(f'{k} هذا الامر يخص ( Myth🎖️ مالك القروب وفوق) بس')
      else:
        if not r.smembers(f'{cid}:listGOWNER:{Dev_Zaid}'):
          return await message.reply_text(f'{k} مافيه مالكين اساسيين')
        else:
          count = 0
          for gowner in r.smembers(f'{cid}:listGOWNER:{Dev_Zaid}'):
             r.srem(f'{cid}:listGOWNER:{Dev_Zaid}', int(gowner))
             r.delete(f'{cid}:rankGOWNER:{int(gowner)}{Dev_Zaid}')
             count += 1
          await message.reply_text(demoted.format(k,get_rank(id,cid),k,count,'المالكين الاساسيين'))
   
   if text == 'مسح المالكين':
      if not gowner_pls(id, cid):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المالك الاساسي وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listOWNER:{Dev_Zaid}'):
          return await message.reply_text(f'{k} مافيه مالكين ')
        else:
          count = 0
          for owner in r.smembers(f'{cid}:listOWNER:{Dev_Zaid}'):
             r.srem(f'{cid}:listOWNER:{Dev_Zaid}', int(owner))
             r.delete(f'{cid}:rankOWNER:{int(owner)}{Dev_Zaid}')
             count += 1
          await message.reply_text(demoted.format(k,get_rank(id,cid),k,count,'المالكين'))
   
   if text == 'مسح المدراء':
      if not owner_pls(id, cid):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المالك وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listMOD:{Dev_Zaid}'):
          return await message.reply_text(f'{k} مافيه مدراء')
        else:
          count = 0
          for MOD in r.smembers(f'{cid}:listMOD:{Dev_Zaid}'):
             r.srem(f'{cid}:listMOD:{Dev_Zaid}', int(MOD))
             r.delete(f'{cid}:rankMOD:{int(MOD)}{Dev_Zaid}')
             count += 1
          await message.reply_text(demoted.format(k,get_rank(id,cid),k,count,'المدراء'))
   
   if text == 'مسح الادمنيه' or text == 'مسح الادمن':
      if not mod_pls(id, cid):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listADMIN:{Dev_Zaid}'):
          return await message.reply_text(f'{k} مافيه ادمن')
        else:
          count = 0
          for ADM in r.smembers(f'{cid}:listADMIN:{Dev_Zaid}'):
             r.srem(f'{cid}:listADMIN:{Dev_Zaid}', int(ADM))
             r.delete(f'{cid}:rankADMIN:{int(ADM)}{Dev_Zaid}')
             count += 1
          await message.reply_text(demoted.format(k,get_rank(id,cid),k,count,'الادمن'))
   
   if text == 'مسح المميزين':
      if not mod_pls(id, cid):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listPRE:{Dev_Zaid}'):
          return await message.reply_text(f'{k} مافيه مميزين')
        else:
          count = 0
          for MOD in r.smembers(f'{cid}:listPRE:{Dev_Zaid}'):
             r.srem(f'{cid}:listPRE:{Dev_Zaid}', int(MOD))
             r.delete(f'{cid}:rankPRE:{int(MOD)}{Dev_Zaid}')
             count += 1
          await message.reply_text(demoted.format(k,get_rank(id,cid),k,count,'المميزين'))
   
   if text == 'مسح المكتومين':
      if not mod_pls(id, cid):
        return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
      else:
        if not r.smembers(f'{cid}:listMUTE:{Dev_Zaid}'):
          return await message.reply_text(f'{k} مافيه مكتومين')
        else:
          count = 0
          for MOD in r.smembers(f'{cid}:listMUTE:{Dev_Zaid}'):
             try:
               mod = int(MOD)
             except:
               mod = MOD
             r.srem(f'{cid}:listMUTE:{Dev_Zaid}', mod)
             r.delete(f'{mod}:mute:{cid}{Dev_Zaid}')
             count += 1
          await message.reply_text(demoted.format(k,get_rank(id,cid),k,count,'المكتومين'))
   
   if text == 'مسح المكتومين عام':
      if not dev_pls(id, cid):
        return await message.reply_text(f'{k} هذا الامر يخص ( Myth🎖️ وفوق ) بس')
      else:
        if not r.smembers(f'listMUTE:{Dev_Zaid}'):
          return await message.reply_text(f'{k} مافيه مكتومين عام')
        else:
          count = 0
          for MOD in r.smembers(f'listMUTE:{Dev_Zaid}'):
             r.srem(f'listMUTE:{Dev_Zaid}', int(MOD))
             r.delete(f'{int(MOD)}:mute:{Dev_Zaid}')
             count += 1
          await message.reply_text(demoted.format(k,get_rank(id,cid),k,count,'المكتومين عام'))
   
   if text == 'مسح المحظورين عام':
      if not dev_pls(id, cid):
        return await message.reply_text(f'{k} هذا الامر يخص ( Myth🎖️ وفوق ) بس')
      else:
        if not r.smembers(f'listGBAN:{Dev_Zaid}'):
          return await message.reply_text(f'{k} مافيه حمير محظورين')
        else:
          count = 0
          for MOD in r.smembers(f'listGBAN:{Dev_Zaid}'):
             r.srem(f'listGBAN:{Dev_Zaid}', int(MOD))
             r.delete(f'{int(MOD)}:gban:{Dev_Zaid}')
             count += 1
          await message.reply_text(demoted.format(k,get_rank(id,cid),k,count,'الحمير المحظورين عام'))
          
             
       
   
   


def register(app):
    """Register del_ranks handlers."""
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(
        filters.TEXT & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
        delRanksHandler
    ), group=9)
