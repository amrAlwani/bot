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


async def funHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    message = update.message
    user = update.effective_user
    chat = update.effective_chat
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'scatteredda'
    await funFunc(update, context, k,channel)
    
async def funFunc(update, context, k,channel):
    if not update.message:
        return
    message = update.message
    user = update.effective_user
    chat = update.effective_chat
    if r.get(f'{chat.id}:disableFun:{Dev_Zaid}'):  return 
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
    ################# CAKE #################
    if text == 'رفع كيك' or text == 'رفع كيكه' or text == 'رفع كيكة':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:CakeList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} كيكه من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:CakeList:{chat.id}',id)
         r.set(f'{Dev_Zaid}:CakeName:{id}', mention)
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته كيكه 🍰\n☆')
    
    if text == 'تنزيل كيك' or text == 'تنزيل كيكه' or text == 'تنزيل كيكة':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:CakeList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو كيكه من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:CakeList:{chat.id}',id)
         r.delete(f'{Dev_Zaid}:CakeName:{id}')
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من كيكه\n☆')
    
    if text == 'قائمه الكيك' or text == 'قائمة الكيك':
     if not r.smembers(f'{Dev_Zaid}:CakeList:{chat.id}'):
       return await message.reply_text(f'{k} قائمة الكيك فاضية')
     else:
       txt = '- قائمة الكيك 🍰\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:CakeList:{chat.id}'):
          mention = r.get(f'{Dev_Zaid}:CakeName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await message.reply_text(txt, disable_web_page_preview=True)
    
    if text == 'مسح قائمة الكيك' or text == 'مسح قائمه الكيك':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:CakeList:{chat.id}'):
         return await message.reply_text(f'{k} قائمة الكيك فاضية')
       else:
         await message.reply_text(f'{k} ابشر مسحت قائمة الكيك')
         for cake in r.smembers(f'{Dev_Zaid}:CakeList:{chat.id}'):
           r.srem(f'{Dev_Zaid}:CakeList:{chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:CakeName:{cake}')
           
    ################# CAKE #################
    
    ################# 3SL #################
    if text == 'رفع عسل':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:3SLList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} عسل من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:3SLList:{chat.id}',id)
         r.set(f'{Dev_Zaid}:3SLName:{id}', mention)
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته عسل 🍯\n☆')
    
    if text == 'تنزيل عسل':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:3SLList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو عسل من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:3SLList:{chat.id}',id)
         r.delete(f'{Dev_Zaid}:3SLName:{id}')
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من عسل\n☆')
    
    if text == 'قائمه العسل' or text == 'قائمة العسل':
     if not r.smembers(f'{Dev_Zaid}:3SLList:{chat.id}'):
       return await message.reply_text(f'{k} قائمة العسل فاضية')
     else:
       txt = '- قائمة العسل 🍯\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:3SLList:{chat.id}'):
          mention = r.get(f'{Dev_Zaid}:3SLName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await message.reply_text(txt, disable_web_page_preview=True)
    
    if text == 'مسح قائمة العسل' or text == 'مسح قائمه العسل':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:3SLList:{chat.id}'):
         return await message.reply_text(f'{k} قائمة العسل فاضية')
       else:
         await message.reply_text(f'{k} ابشر مسحت قائمة العسل')
         for cake in r.smembers(f'{Dev_Zaid}:3SLList:{chat.id}'):
           r.srem(f'{Dev_Zaid}:3SLList:{chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:3SLName:{cake}')

    ################# 3SL #################
    
    ################# ZQ #################
    if text == 'رفع نصاب':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:ZQList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} نصاب من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:ZQList:{chat.id}',id)
         r.set(f'{Dev_Zaid}:ZQName:{id}', mention)
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته نصاب 💩\n☆')
    
    if text == 'تنزيل نصاب':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:ZQList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو نصاب من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:ZQList:{chat.id}',id)
         r.delete(f'{Dev_Zaid}:ZQName:{id}')
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من نصاب\n☆')
    
    if text == 'قائمه النصابين' or text == 'قائمة النصابين':
     if not r.smembers(f'{Dev_Zaid}:ZQList:{chat.id}'):
       return await message.reply_text(f'{k} قائمة النصابين فاضية')
     else:
       txt = '- قائمة النصابين 💩\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:ZQList:{chat.id}'):
          mention = r.get(f'{Dev_Zaid}:ZQName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await message.reply_text(txt, disable_web_page_preview=True)
    
    if text == 'مسح قائمة النصابين' or text == 'مسح قائمه النصابين':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:ZQList:{chat.id}'):
         return await message.reply_text(f'{k} قائمة النصابين فاضية')
       else:
         await message.reply_text(f'{k} ابشر مسحت قائمة النصابين')
         for cake in r.smembers(f'{Dev_Zaid}:ZQList:{chat.id}'):
           r.srem(f'{Dev_Zaid}:ZQList:{chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:ZQName:{cake}')

    ################# ZQ #################
    
    ################# 7MR #################
    if text == 'رفع حمار':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:7MRList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} حمار من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:7MRList:{chat.id}',id)
         r.set(f'{Dev_Zaid}:7MRName:{id}', mention)
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته حمار 🦓\n☆')
    
    if text == 'تنزيل حمار':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:7MRList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو حمار من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:7MRList:{chat.id}',id)
         r.delete(f'{Dev_Zaid}:7MRName:{id}')
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من حمار\n☆')
    
    if text == 'قائمه الحمير' or text == 'قائمة الحمير':
     if not r.smembers(f'{Dev_Zaid}:7MRList:{chat.id}'):
       return await message.reply_text(f'{k} قائمة الحمير فاضية')
     else:
       txt = '- قائمة الحمير 🦓\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:7MRList:{chat.id}'):
          mention = r.get(f'{Dev_Zaid}:7MRName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await message.reply_text(txt, disable_web_page_preview=True)
    
    if text == 'مسح قائمة الحمير' or text == 'مسح قائمه الحمير':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:7MRList:{chat.id}'):
         return await message.reply_text(f'{k} قائمة الحمير فاضية')
       else:
         await message.reply_text(f'{k} ابشر مسحت قائمة الحمير')
         for cake in r.smembers(f'{Dev_Zaid}:7MRList:{chat.id}'):
           r.srem(f'{Dev_Zaid}:7MRList:{chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:7MRName:{cake}')

    ################# 7MR #################
    
    ################# COW #################
    if text == 'رفع بقرة' or text == 'رفع بقره':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:COWList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} بقرة من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:COWList:{chat.id}',id)
         r.set(f'{Dev_Zaid}:COWName:{id}', mention)
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته بقرة 🐄\n☆')
    
    if text == 'تنزيل بقرة' or text == 'تنزيل بقره':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:COWList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو بقرة من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:COWList:{chat.id}',id)
         r.delete(f'{Dev_Zaid}:COWName:{id}')
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من بقرة\n☆')
    
    if text == 'قائمه البقر' or text == 'قائمة البقر':
     if not r.smembers(f'{Dev_Zaid}:COWList:{chat.id}'):
       return await message.reply_text(f'{k} قائمة البقر فاضية')
     else:
       txt = '- قائمة البقر 🐄\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:COWList:{chat.id}'):
          mention = r.get(f'{Dev_Zaid}:COWName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await message.reply_text(txt, disable_web_page_preview=True)
    
    if text == 'مسح قائمة البقر' or text == 'مسح قائمه البقر':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:COWList:{chat.id}'):
         return await message.reply_text(f'{k} قائمة البقر فاضية')
       else:
         await message.reply_text(f'{k} ابشر مسحت قائمة البقر')
         for cake in r.smembers(f'{Dev_Zaid}:COWList:{chat.id}'):
           r.srem(f'{Dev_Zaid}:COWList:{chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:COWName:{cake}')

    ################# COW #################
    
    ################# DOG #################
    if text == 'رفع كلب':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:DOGList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} كلب من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:DOGList:{chat.id}',id)
         r.set(f'{Dev_Zaid}:DOGName:{id}', mention)
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته كلب 🐩\n☆')
    
    if text == 'تنزيل كلب':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:DOGList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو كلب من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:DOGList:{chat.id}',id)
         r.delete(f'{Dev_Zaid}:DOGName:{id}')
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من كلب\n☆')
    
    if text == 'قائمه الكلاب' or text == 'قائمة الكلاب':
     if not r.smembers(f'{Dev_Zaid}:DOGList:{chat.id}'):
       return await message.reply_text(f'{k} قائمة الكلاب فاضية')
     else:
       txt = '- قائمة الكلاب 🐩\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:DOGList:{chat.id}'):
          mention = r.get(f'{Dev_Zaid}:DOGName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await message.reply_text(txt, disable_web_page_preview=True)
    
    if text == 'مسح قائمة الكلاب' or text == 'مسح قائمه الكلاب':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:DOGList:{chat.id}'):
         return await message.reply_text(f'{k} قائمة الكلاب فاضية')
       else:
         await message.reply_text(f'{k} ابشر مسحت قائمة الكلاب')
         for cake in r.smembers(f'{Dev_Zaid}:DOGList:{chat.id}'):
           r.srem(f'{Dev_Zaid}:DOGList:{chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:DOGName:{cake}')

    ################# DOG #################
    
    ################# MON #################
    if text == 'رفع قرد':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:MONList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} قرد من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:MONList:{chat.id}',id)
         r.set(f'{Dev_Zaid}:MONName:{id}', mention)
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته قرد 🐒\n☆')
    
    if text == 'تنزيل قرد':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:MONList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو قرد من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:MONList:{chat.id}',id)
         r.delete(f'{Dev_Zaid}:MONName:{id}')
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من قرد\n☆')
    
    if text == 'قائمه القرود' or text == 'قائمة القرود':
     if not r.smembers(f'{Dev_Zaid}:MONList:{chat.id}'):
       return await message.reply_text(f'{k} قائمة القرود فاضية')
     else:
       txt = '- قائمة القرود 🐒\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:MONList:{chat.id}'):
          mention = r.get(f'{Dev_Zaid}:MONName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await message.reply_text(txt, disable_web_page_preview=True)
    
    if text == 'مسح قائمة القرود' or text == 'مسح قائمه القرود':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:MONList:{chat.id}'):
         return await message.reply_text(f'{k} قائمة القرود فاضية')
       else:
         await message.reply_text(f'{k} ابشر مسحت قائمة القرود')
         for cake in r.smembers(f'{Dev_Zaid}:MONList:{chat.id}'):
           r.srem(f'{Dev_Zaid}:MONList:{chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:MONName:{cake}')

    ################# MON #################
    
    ################# TES #################
    if text == 'رفع تيس':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:TESList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} تيس من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:TESList:{chat.id}',id)
         r.set(f'{Dev_Zaid}:TESName:{id}', mention)
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته تيس 🐐\n☆')
    
    if text == 'تنزيل تيس':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:TESList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو تيس من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:TESList:{chat.id}',id)
         r.delete(f'{Dev_Zaid}:TESName:{id}')
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من تيس\n☆')
    
    if text == 'قائمه التيس' or text == 'قائمة التيس':
     if not r.smembers(f'{Dev_Zaid}:TESList:{chat.id}'):
       return await message.reply_text(f'{k} قائمة التيوس فاضية')
     else:
       txt = '- قائمة التيوس 🐐\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:TESList:{chat.id}'):
          mention = r.get(f'{Dev_Zaid}:TESName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await message.reply_text(txt, disable_web_page_preview=True)
    
    if text == 'مسح قائمة التيس' or text == 'مسح قائمه التيس':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:TESList:{chat.id}'):
         return await message.reply_text(f'{k} قائمة التيوس فاضية')
       else:
         await message.reply_text(f'{k} ابشر مسحت قائمة التيوس')
         for cake in r.smembers(f'{Dev_Zaid}:TESList:{chat.id}'):
           r.srem(f'{Dev_Zaid}:TESList:{chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:TESName:{cake}')

    ################# TES #################
    
    
    ################# TOR #################
    if text == 'رفع ثور':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:TORList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ثور من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:TORList:{chat.id}',id)
         r.set(f'{Dev_Zaid}:TORName:{id}', mention)
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته ثور 🐂\n☆')
    
    if text == 'تنزيل ثور':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:TORList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو ثور من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:TORList:{chat.id}',id)
         r.delete(f'{Dev_Zaid}:TORName:{id}')
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من ثور\n༄')
    
    if text == 'قائمه الثور' or text == 'قائمة الثور':
     if not r.smembers(f'{Dev_Zaid}:TORList:{chat.id}'):
       return await message.reply_text(f'{k} قائمة الثور فاضية')
     else:
       txt = '- قائمة الثور 🐂\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:TORList:{chat.id}'):
          mention = r.get(f'{Dev_Zaid}:TORName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await message.reply_text(txt, disable_web_page_preview=True)
    
    if text == 'مسح قائمة الثور' or text == 'مسح قائمه الثور':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:TORList:{chat.id}'):
         return await message.reply_text(f'{k} قائمة الثور فاضية')
       else:
         await message.reply_text(f'{k} ابشر مسحت قائمة الثور')
         for cake in r.smembers(f'{Dev_Zaid}:TORList:{chat.id}'):
           r.srem(f'{Dev_Zaid}:TORList:{chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:TORName:{cake}')

    ################# TOR #################
    
    
    ################# B3S #################
    if text == 'رفع هكر':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:B3SList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} هكر من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:B3SList:{chat.id}',id)
         r.set(f'{Dev_Zaid}:B3SName:{id}', mention)
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته هكر 🏅\n☆')
    
    if text == 'تنزيل هكر':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:B3SList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو هكر من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:B3SList:{chat.id}',id)
         r.delete(f'{Dev_Zaid}:B3SName:{id}')
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من هكر\n☆')
    
    if text == 'قائمه الهكر' or text == 'قائمة الهكر':
     if not r.smembers(f'{Dev_Zaid}:B3SList:{chat.id}'):
       return await message.reply_text(f'{k} قائمة الهكر فاضية')
     else:
       txt = '- قائمة الهكر 🏅\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:B3SList:{chat.id}'):
          mention = r.get(f'{Dev_Zaid}:B3SName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await message.reply_text(txt, disable_web_page_preview=True)
    
    if text == 'مسح قائمة الهكر' or text == 'مسح قائمه الهكر':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:B3SList:{chat.id}'):
         return await message.reply_text(f'{k} قائمة الهكر فاضية')
       else:
         await message.reply_text(f'{k} ابشر مسحت قائمة الهكر')
         for cake in r.smembers(f'{Dev_Zaid}:B3SList:{chat.id}'):
           r.srem(f'{Dev_Zaid}:B3SList:{chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:B3SName:{cake}')

    ################# B3S #################
    
    ################# DJJ #################
    if text == 'رفع دجاجه' or text == 'رفع دجاجة':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:DJJList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} دجاجه من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:DJJList:{chat.id}',id)
         r.set(f'{Dev_Zaid}:DJJName:{id}', mention)
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته دجاجه 🐓\n☆')
    
    if text == 'تنزيل دجاجه' or text == 'تنزيل دجاجة':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:DJJList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو دجاجه من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:DJJList:{chat.id}',id)
         r.delete(f'{Dev_Zaid}:DJJName:{id}')
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من دجاجه\n☆')
    
    if text == 'قائمه الدجاج' or text == 'قائمة الدجاج':
     if not r.smembers(f'{Dev_Zaid}:DJJList:{chat.id}'):
       return await message.reply_text(f'{k} قائمة الدجاج فاضية')
     else:
       txt = '- قائمة الدجاج 🐓\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:DJJList:{chat.id}'):
          mention = r.get(f'{Dev_Zaid}:DJJName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await message.reply_text(txt, disable_web_page_preview=True)
    
    if text == 'مسح قائمة الدجاج' or text == 'مسح قائمه الدجاج':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:DJJList:{chat.id}'):
         return await message.reply_text(f'{k} قائمة الدجاج فاضية')
       else:
         await message.reply_text(f'{k} ابشر مسحت قائمة الدجاج')
         for cake in r.smembers(f'{Dev_Zaid}:DJJList:{chat.id}'):
           r.srem(f'{Dev_Zaid}:DJJList:{chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:DJJName:{cake}')

    ################# DJJ #################
    
    ################# HTF #################
    if text == 'رفع ملكه':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:HTFList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ملكه من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:HTFList:{chat.id}',id)
         r.set(f'{Dev_Zaid}:HTFName:{id}', mention)
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته ملكه 🧱\n☆')
    
    if text == 'تنزيل ملكه':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:HTFList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو ملكه من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:HTFList:{chat.id}',id)
         r.delete(f'{Dev_Zaid}:HTFName:{id}')
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من ملكه\n☆')
    
    if text == 'قائمه الهطوف' or text == 'قائمة الهطوف':
     if not r.smembers(f'{Dev_Zaid}:HTFList:{chat.id}'):
       return await message.reply_text(f'{k} قائمة الهطوف فاضية')
     else:
       txt = '- قائمة الهطوف 🧱\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:HTFList:{chat.id}'):
          mention = r.get(f'{Dev_Zaid}:HTFName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await message.reply_text(txt, disable_web_page_preview=True)
    
    if text == 'مسح قائمة الهطوف' or text == 'مسح قائمه الهطوف':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:HTFList:{chat.id}'):
         return await message.reply_text(f'{k} قائمة الهطوف فاضية')
       else:
         await message.reply_text(f'{k} ابشر مسحت قائمة الهطوف')
         for cake in r.smembers(f'{Dev_Zaid}:HTFList:{chat.id}'):
           r.srem(f'{Dev_Zaid}:HTFList:{chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:HTFName:{cake}')

    ################# HTF #################
    
    ################# SYD #################
    if text == 'رفع صياد':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:SYDList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} صياد من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:SYDList:{chat.id}',id)
         r.set(f'{Dev_Zaid}:SYDName:{id}', mention)
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته صياد 🔫\n☆')
    
    if text == 'تنزيل صياد':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:SYDList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو صياد من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:SYDList:{chat.id}',id)
         r.delete(f'{Dev_Zaid}:SYDName:{id}')
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من صياد\n☆')
    
    if text == 'قائمه الصيادين' or text == 'قائمة الصيادين':
     if not r.smembers(f'{Dev_Zaid}:SYDList:{chat.id}'):
       return await message.reply_text(f'{k} قائمة الصيادين فاضية')
     else:
       txt = '- قائمة الصيادين 🔫\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:SYDList:{chat.id}'):
          mention = r.get(f'{Dev_Zaid}:SYDName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await message.reply_text(txt, disable_web_page_preview=True)
    
    if text == 'مسح قائمة الصيادين' or text == 'مسح قائمه الصيادين':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:SYDList:{chat.id}'):
         return await message.reply_text(f'{k} قائمة الصيادين فاضية')
       else:
         await message.reply_text(f'{k} ابشر مسحت قائمة الصيادين')
         for cake in r.smembers(f'{Dev_Zaid}:SYDList:{chat.id}'):
           r.srem(f'{Dev_Zaid}:SYDList:{chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:SYDName:{cake}')

    ################# SYD #################
    
    ################# 5RF #################
    if text == 'رفع خروف':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:5RFList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} خروف من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:5RFList:{chat.id}',id)
         r.set(f'{Dev_Zaid}:5RFName:{id}', mention)
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته خروف 🐏\n☆')
    
    if text == 'تنزيل خروف':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:5RFList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو خروف من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:5RFList:{chat.id}',id)
         r.delete(f'{Dev_Zaid}:5RFName:{id}')
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من خروف\n☆')
    
    if text == 'قائمه الخرفان' or text == 'قائمة الخرفان':
     if not r.smembers(f'{Dev_Zaid}:5RFList:{chat.id}'):
       return await message.reply_text(f'{k} قائمة الخرفان فاضية')
     else:
       txt = '- قائمة الخرفان 🐏\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:5RFList:{chat.id}'):
          mention = r.get(f'{Dev_Zaid}:5RFName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await message.reply_text(txt, disable_web_page_preview=True)
    
    if text == 'مسح قائمة الخرفان' or text == 'مسح قائمه الخرفان':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:5RFList:{chat.id}'):
         return await message.reply_text(f'{k} قائمة الخرفان فاضية')
       else:
         await message.reply_text(f'{k} ابشر مسحت قائمة الخرفان')
         for cake in r.smembers(f'{Dev_Zaid}:5RFList:{chat.id}'):
           r.srem(f'{Dev_Zaid}:5RFList:{chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:5RFName:{cake}')

    ################# 5RF #################
    
    ################# TEZ #################
    if text == 'رفع هكر':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if r.sismember(f'{Dev_Zaid}:TEZList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} هكر من قبل\n☆')
       else:
         r.sadd(f'{Dev_Zaid}:TEZList:{chat.id}',id)
         r.set(f'{Dev_Zaid}:TEZName:{id}', mention)
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر رفعته هكر ♕\n☆')
    
    if text == 'تنزيل هكر':
     if message.reply_to_message and message.reply_to_message.from_user:
       mention = message.reply_to_message.from_user.mention_html()
       id = message.reply_to_message.from_user.id
       if not r.sismember(f'{Dev_Zaid}:TEZList:{chat.id}',id):
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} مو هكر من قبل\n☆')
       else:
         r.srem(f'{Dev_Zaid}:TEZList:{chat.id}',id)
         r.delete(f'{Dev_Zaid}:TEZName:{id}')
         return await message.reply_text(f'「 ⁪⁬⁪⁬{mention} 」\n{k} ابشر نزلته من هكر\n☆')
    
    if text == 'قائمه هكر' or text == 'قائمة هكر':
     if not r.smembers(f'{Dev_Zaid}:TEZList:{chat.id}'):
       return await message.reply_text(f'{k} قائمة هكر فاضية')
     else:
       txt = '- قائمة هكر ♕\n'
       count = 1
       for cake in r.smembers(f'{Dev_Zaid}:TEZList:{chat.id}'):
          mention = r.get(f'{Dev_Zaid}:TEZName:{cake}')
          txt += f'{count} ➣ ⁪⁬⁪⁬{mention} ࿓ ( `{cake}` )\n'
          count += 1
       txt += '\n☆'
       return await message.reply_text(txt, disable_web_page_preview=True)
    
    if text == 'مسح قائمة هكر' or text == 'مسح قائمه هكر':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} هذا الامر يخص ( الادمن وفوق ) بس')
     else:
       if not r.smembers(f'{Dev_Zaid}:TEZList:{chat.id}'):
         return await message.reply_text(f'{k} قائمة هكر فاضية')
       else:
         await message.reply_text(f'{k} ابشر مسحت قائمة هكر')
         for cake in r.smembers(f'{Dev_Zaid}:TEZList:{chat.id}'):
           r.srem(f'{Dev_Zaid}:TEZList:{chat.id}',int(cake))
           r.delete(f'{Dev_Zaid}:TEZName:{cake}')

    ################# TEZ #################
    
    ################# 🔮 #################
    
    if text == 'رفع لقلبي' and message.reply_to_message:
     return await message.reply_text('{} رفعته لقلبك\n{} اللهم حسد 😔'.format(k,k))
    
    if text == 'تنزيل من قلبي' and message.reply_to_message:
     return await message.reply_text('اح اح ماتوصل')
    
    ################# 🔮 #################
    
    
    
    
       
      
    
    
    

def register(app):
    """Register fun handlers."""
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(
        filters.TEXT & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
        funHandler
    ), group=5)
