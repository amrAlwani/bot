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


async def customrankHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'scatteredda'
    await customRankFunc(update, context, k, channel)
    
async def customRankFunc(update, context, k,channel):
   message = update.message
   chat = update.effective_chat
   user = update.effective_user
   if not message or not chat or not user:
       return
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
   if text == 'الغاء':
     if r.get(f'{user.id}:addRank2:{chat.id}{Dev_Zaid}') or r.get(f'{user.id}:addRank:{chat.id}{Dev_Zaid}') or r.get(f'{user.id}:delRank:{chat.id}{Dev_Zaid}'):
        await message.reply_text(f'{k} من عيوني لغيت كل شي يخص الرتب')
        r.delete(f'{user.id}:addRank:{chat.id}{Dev_Zaid}')
        r.delete(f'{user.id}:delRank:{chat.id}{Dev_Zaid}')
        r.delete(f'{user.id}:addRank2:{chat.id}{Dev_Zaid}')
   
   if r.get(f'{user.id}:addRank2:{chat.id}{Dev_Zaid}') and mod_pls(user.id,chat.id) and len(message.text) <= 20:
     rank = r.get(f'{user.id}:addRank2:{chat.id}{Dev_Zaid}')
     r.delete(f'{user.id}:addRank2:{chat.id}{Dev_Zaid}')
     if rank == 'مالك اساسي':
       if r.get(f'{chat.id}:RankGowner:{Dev_Zaid}'):
         rrr = r.get(f'{chat.id}:RankGowner:{Dev_Zaid}')
         r.srem(f'{chat.id}:ranklist:{Dev_Zaid}',f'{rank}&&newr={rrr}')
         r.delete(f'{chat.id}:RankGowner:{Dev_Zaid}')
       r.set(f'{chat.id}:RankGowner:{Dev_Zaid}',message.text)
     if rank == 'مالك':
       if r.get(f'{chat.id}:RankOwner:{Dev_Zaid}'):
         rrr = r.get(f'{chat.id}:RankOwner:{Dev_Zaid}')
         r.srem(f'{chat.id}:ranklist:{Dev_Zaid}',f'{rank}&&newr={rrr}')
         r.delete(f'{chat.id}:RankOwner:{Dev_Zaid}')
       r.set(f'{chat.id}:RankOwner:{Dev_Zaid}',message.text)
     if rank == 'مدير':
       if r.get(f'{chat.id}:RankMod:{Dev_Zaid}'):
         rrr = r.get(f'{chat.id}:RankMod:{Dev_Zaid}')
         r.srem(f'{chat.id}:ranklist:{Dev_Zaid}',f'{rank}&&newr={rrr}')
         r.delete(f'{chat.id}:RankMod:{Dev_Zaid}')     
       r.set(f'{chat.id}:RankMod:{Dev_Zaid}',message.text)
     if rank == 'ادمن':
       if r.get(f'{chat.id}:RankAdm:{Dev_Zaid}'):
         rrr = r.get(f'{chat.id}:RankAdm:{Dev_Zaid}')
         r.srem(f'{chat.id}:ranklist:{Dev_Zaid}',f'{rank}&&newr={rrr}')
         r.delete(f'{chat.id}:RankAdm:{Dev_Zaid}')     
       r.set(f'{chat.id}:RankAdm:{Dev_Zaid}',message.text)
     if rank == 'مميز':
       if r.get(f'{chat.id}:RankPre:{Dev_Zaid}'):
         rrr = r.get(f'{chat.id}:RankPre:{Dev_Zaid}')
         r.srem(f'{chat.id}:ranklist:{Dev_Zaid}',f'{rank}&&newr={rrr}')
         r.delete(f'{chat.id}:RankPre:{Dev_Zaid}')     
       r.set(f'{chat.id}:RankPre:{Dev_Zaid}',message.text)
     if rank == 'عضو':
       if r.get(f'{chat.id}:RankMem:{Dev_Zaid}'):
         rrr = r.get(f'{chat.id}:RankMem:{Dev_Zaid}')
         r.srem(f'{chat.id}:ranklist:{Dev_Zaid}',f'{rank}&&newr={rrr}')
         r.delete(f'{chat.id}:RankMem:{Dev_Zaid}')     
       r.set(f'{chat.id}:RankMem:{Dev_Zaid}',message.text)
     r.sadd(f'{chat.id}:ranklist:{Dev_Zaid}',f'{rank}&&newr={message.text}')  
     return await message.reply_text(f'{k} تم غيرت الرتبه الى ( {message.text} )')
       
   
   if r.get(f'{user.id}:addRank:{chat.id}{Dev_Zaid}') and mod_pls(user.id,chat.id):
     r.delete(f'{user.id}:addRank:{chat.id}{Dev_Zaid}')
     if not message.text in ['مالك اساسي','مالك','مدير','ادمن','مميز','عضو']:
       return await message.reply_text(f'{k} ركز! الرتبه اللي كتبتها مو موجوده')
     else:
       r.set(f'{user.id}:addRank2:{chat.id}{Dev_Zaid}',message.text,ex=600)
       return await message.reply_text(f'{k} حلو الحين ارسل الرتبه الجديدة')
   
   if r.get(f'{user.id}:delRank:{chat.id}{Dev_Zaid}') and mod_pls(user.id,chat.id):
     r.delete(f'{user.id}:delRank:{chat.id}{Dev_Zaid}')
     if not message.text in ['مالك اساسي','مالك','مدير','ادمن','مميز','عضو']:
       return await message.reply_text(f'{k} مافي رتبه زي كذا لازم تكتب الرتبه الاساسيه مثال مالك اساسي مو {message.text[:20]}')
     else:
       rank = message.text
       if rank == 'مالك اساسي':
         rank2 = r.get(f'{chat.id}:RankGowner:{Dev_Zaid}')
         r.delete(f'{chat.id}:RankGowner:{Dev_Zaid}')
       if rank == 'مالك':
         rank2 = r.get(f'{chat.id}:RankOwner:{Dev_Zaid}')
         r.delete(f'{chat.id}:RankOwner:{Dev_Zaid}')
       if rank == 'مدير':
         rank2 = r.get(f'{chat.id}:RankMod:{Dev_Zaid}')
         r.delete(f'{chat.id}:RankMod:{Dev_Zaid}')
       if rank == 'ادمن':
         rank2 = r.get(f'{chat.id}:RankAdm:{Dev_Zaid}')
         r.delete(f'{chat.id}:RankAdm:{Dev_Zaid}')
       if rank == 'مميز':
         rank2 = r.get(f'{chat.id}:RankPre:{Dev_Zaid}')
         r.delete(f'{chat.id}:RankPre:{Dev_Zaid}')
       if rank == 'عضو':
         rank2 = r.get(f'{chat.id}:RankMem:{Dev_Zaid}')
         r.delete(f'{chat.id}:RankMem:{Dev_Zaid}')
       r.srem(f'{chat.id}:ranklist:{Dev_Zaid}',f'{rank}&&newr={rank2}')
       return await message.reply_text(f'{k} مسحت رتبه ( {rank2} )')
   
   if text == 'مسح الرتب':
     if not mod_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
     else:
       if not r.smembers(f'{chat.id}:ranklist:{Dev_Zaid}'):
         return await message.reply_text(f'{k} مافيه رتب مضافة')
       else:
         await message.reply_text(f'{k} مسحت كل الرتب المضافة')
         r.delete(f'{chat.id}:RankGowner:{Dev_Zaid}')
         r.delete(f'{chat.id}:RankOwner:{Dev_Zaid}')
         r.delete(f'{chat.id}:RankMod:{Dev_Zaid}')
         r.delete(f'{chat.id}:RankAdm:{Dev_Zaid}')
         r.delete(f'{chat.id}:RankPre:{Dev_Zaid}')
         r.delete(f'{chat.id}:RankMem:{Dev_Zaid}')
         return r.delete(f'{chat.id}:ranklist:{Dev_Zaid}')
   
   if text == 'قائمه الرتب' or text == 'قائمة الرتب':
     if not mod_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
     else:
       if not r.smembers(f'{chat.id}:ranklist:{Dev_Zaid}'):
         return await message.reply_text(f'{k} مافيه رتب مضافة')
       else:
         txt = 'قائمة الرتب:\n'
         count = 1
         for rrr in r.smembers(f'{chat.id}:ranklist:{Dev_Zaid}'):
            rank = rrr.split('&&newr=')
            txt += f'{count}) {rank[0]} ~ ( {rank[1]} )\n'
            count += 1
         txt += '\n☆'
         return await message.reply_text(txt, disable_web_page_preview=True)

   if text == 'مسح رتبه' or text == 'مسح رتبة':
     if not mod_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
     else:
       r.set(f'{user.id}:delRank:{chat.id}{Dev_Zaid}',1,ex=600)
       return await message.reply_text(f'{k} ارسل اسم الرتبه اللي تبي تمسحها الحين')
   
   if text == 'تغيير رتبه' or text == 'تغيير رتبة':
     if not mod_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الأمر يخص ( المدير وفوق ) بس')
     else:
       r.set(f'{user.id}:addRank:{chat.id}{Dev_Zaid}',1,ex=600)
       return await message.reply_text(f'''
{k} ارسل الرتبه اللي تبي تغييرها

{k} مالك اساسي
{k} مالك
{k} مدير
{k} ادمن
{k} مميز
{k} عضو
☆''')

def register(app):
    """Register customRank handlers."""
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(
        filters.TEXT & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
        customrankHandler
    ), group=13)
