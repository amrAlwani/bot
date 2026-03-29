import random, re, time, os




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
from helpers.get_create import get_creation_date
from io import BytesIO
from .games import get_emoji_bank
from helpers.Ranks import isLockCommand

class _DummyClient:
    @staticmethod
    def on_message(*args, **kwargs):
        def decorator(func): return func
        return decorator
    @staticmethod
    def on_callback_query(*args, **kwargs):
        def decorator(func): return func
        return decorator
    @staticmethod
    def on_inline_query(*args, **kwargs):
        def decorator(func): return func
        return decorator
    @staticmethod
    def on_edited_message(*args, **kwargs):
        def decorator(func): return func
        return decorator
    @staticmethod
    def on_chat_member_updated(*args, **kwargs):
        def decorator(func): return func
        return decorator

Client = _DummyClient()


def get_top(users):
   users = [tuple(i.items()) for i in users]
   top = sorted(users, key=lambda i: i[-1][-1], reverse=True)
   top = [dict(i) for i in top]
   return top
custom_ids = ['''
- ᴜѕᴇʀɴᴀᴍᴇ ➣ {اليوزر} .
- ᴍѕɢѕ ➣ {الرسائل} .
- ѕᴛᴀᴛѕ ➣ {الرتبه} .
- ʏᴏᴜʀ ɪᴅ ➣ {الايدي} .
- ᴇᴅɪᴛ ᴍsɢ ➣ {التعديل} .
- ᴅᴇᴛᴀɪʟs ➣ {التفاعل} .
-  ɢᴀᴍᴇ ➣ {المجوهرات} .
{البايو}
''','''
• USE 𖦹 {اليوزر}
• MSG 𖥳 {الرسائل}
• STA 𖦹 {الرتبه}
• iD 𖥳 {الايدي}
{البايو}
''','''
➞: 𝒔𝒕𝒂𓂅 {اليوزر} 𓍯
➞: 𝒖𝒔𝒆𝒓𓂅 {المعرف} 𓍯
➞: 𝒎𝒔𝒈𝒆𓂅 {الرسائل} 𓍯
➞: 𝒊𝒅 𓂅 {الايدي} 𓍯
{البايو}
''','''
♡ : 𝐼𝐷 𖠀 {الايدي} .
♡ : 𝑈𝑆𝐸𝑅 𖠀 {اليوزر} .
♡ : 𝑀𝑆𝐺𝑆 𖠀 {الرسائل} .
♡ : 𝑆𝑇𝐴𝑇𝑆 𖠀 {الرتبه} .
♡ : 𝐸𝐷𝐼𝑇  𖠀 {التعديل} .
{البايو}
''', '''
- الايـدي || {الايدي}.
• الاسـم  || {الاسم}.
• المُعرف || {اليوزر}.
• الرُتبـه || {الرتبه}.
• الرسائل || {الرسائل}.
{البايو}
''', '''
⌁ NaMe ⇨ {الاسم}
⌁ Use ⇨ {اليوزر}
⌁ Msg ⇨ {الرسائل}
⌁ Sta ⇨ {الرتبه}
⌁ iD ⇨ {الايدي}
{البايو}
''', '''
📋¦ ɴᴀᴍᴇ ➺ {الاسم}
🗞¦ ʏᴏᴜʀ ɪᴅ ➺ {الايدي}
🔦¦ ᴜѕᴇʀɴᴀᴍᴇ ➺ {اليوزر}
🕹¦ ѕᴛᴀᴛѕ ➺ {الرتبه}
🔭¦ ᴅᴇᴛᴀɪʟs ➺ {التفاعل}
📨¦  ᴍѕɢѕ ➺ {الرسائل}
🎰¦ ɢᴀᴍᴇ ➺ {المجوهرات}
{البايو}
''', '''
✾ 𝐔𝐒𝐄 ⤷ {اليوزر}
✾ 𝐌𝐒𝐆 ⤷ {الرسائل}
✾ 𝐒𝐓𝐀 ⤷ {الرتبه}
✾ 𝐈𝐃 ⤷ {الايدي}
✾ 𝐁𝐈𝐎 ⤷ {البايو}
''', '''
𓆰 𝑼𝑬𝑺 : {اليوزر}
𓆰 𝑺𝑻𝑨 : {الرتبه}
𓆰 𝑰𝑫 : {الايدي}
𓆰 𝑴𝑺𝑮 : {الرسائل}
{البايو}'''
]


comments = [
  'تيكفه لاتكتب ايدي',
  'يع',
  'جبر',
  'احلى من يكتب ايدي',
  'افخم ايدي',
  'لحد يرسل ايدي من بعده',
  'يلبييه اطلق ايدي',
  'ازق ايدي',
  'لعد تكتب ايدي',
  'للاسف ايديك تلوث بصري ):',
  'جابك الله انت وأيديك على شكل جبر خاطر لقلبّي'
]

async def addmsgCount(update: Update, context: ContextTypes.DEFAULT_TYPE):
   message = update.message
   user = update.effective_user
   chat = update.effective_chat
   if not message or not user or not chat: return
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return
   if not r.get(f'{Dev_Zaid}{chat.id}:TotalMsgs:{user.id}'):
      r.set(f'{Dev_Zaid}{chat.id}:TotalMsgs:{user.id}', 1)
   else:
      get = int(r.get(f'{Dev_Zaid}{chat.id}:TotalMsgs:{user.id}'))
      r.set(f'{Dev_Zaid}{chat.id}:TotalMsgs:{user.id}', get+1)
   r.set(f"{user.id}:bankName", user.first_name[:25])

@Client.on_edited_message()
async def addeditedmsgCount(update: Update, context: ContextTypes.DEFAULT_TYPE):
   message = update.message or update.edited_message
   user = update.effective_user
   chat = update.effective_chat
   if not message or not user or not chat: return
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return
   if not r.get(f'{chat.id}:TotalEDMsgs:{user.id}{Dev_Zaid}'):
      r.set(f'{chat.id}:TotalEDMsgs:{user.id}{Dev_Zaid}', 1)
   else:
      get = int(r.get(f'{chat.id}:TotalEDMsgs:{user.id}{Dev_Zaid}'))
      r.set(f'{chat.id}:TotalEDMsgs:{user.id}{Dev_Zaid}', get+1)

async def rankGetHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
   k = r.get(f'{Dev_Zaid}:botkey') or '☆'
   await get_my_rank(update, context, k)



async def get_my_rank(update, context, k):



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
   if text == 'مجموعاتي':
     if not r.smembers(f'{user.id}:groups'):
       return await message.reply_text(f'{k} ماعندك مجموعات')
     else:
       groups = len(r.smembers(f'{user.id}:groups'))
       return await message.reply_text(f'{k} عدد مجموعاتك ↼ ( {groups} )')

   if text == 'انشائي':
      create_date = get_creation_date(user.id)
      return await message.reply_text(f'{k} الانشاء ( {create_date} )')

   if text == 'الانشاء' and not message.reply_to_message:
      create_date = get_creation_date(user.id)
      return await message.reply_text(f'{k} الانشاء ( {create_date} )')

   if (text == 'الانشاء' or text == 'انشائه') and message.reply_to_message:
      create_date = get_creation_date(message.reply_to_message.from_user.id)
      return await message.reply_text(f'{k} الانشاء ( {create_date} )')

   if text == 'اسمي':
     return await message.reply_text(user.first_name, disable_web_page_preview=True)

   if text == 'معلوماتي':
      msgs = int(r.get(f'{Dev_Zaid}{chat.id}:TotalMsgs:{user.id}') or 0)
      if msgs > 50:
        tfa3l = 'شد حيلك'
      if msgs > 500:
        tfa3l = 'يجي منك'
      if msgs > 750:
        tfa3l = 'تفاعل متوسط'
      if msgs > 2500:
        tfa3l = 'متفاعل'
      if msgs > 5000:
        tfa3l = 'اسطورة التفاعل'
      if msgs > 10000:
        tfa3l = 'كنق التلي'
      else:
        tfa3l = 'تفاعل صفر'
      if not r.get(f'{chat.id}:TotalEDMsgs:{user.id}{Dev_Zaid}'):
         edits = 0
      else:
         edits= int(r.get(f'{chat.id}:TotalEDMsgs:{user.id}{Dev_Zaid}'))
      if not r.get(f'{chat.id}TotalContacts{user.id}{Dev_Zaid}'):
         contacts = 0
      else:
         contacts = int(r.get(f'{chat.id}TotalContacts{user.id}{Dev_Zaid}'))
      if user.username:
         username = f'@{user.username}'
      if user.usernames:
         username = ''
         for i in user.usernames: username += f"@{i.username} "
      else:
         username = 'مافي يوزر'
      rank = get_rank(user.id,chat.id)
      text = f'''
⚘ المعلومات
❁ الاسم ↼ {user.mention_html()}
❁ اليوزر ↼ {username}
❁ الايدي  ↼ {user.id}
❁ الرتبه ↼ {rank}
┄─┅═ـ═┅─┄
⚘ احصائيات الرسايل
❁ الرسايل ↼ {msgs}
❁ التعديل ↼ {edits}
❁ التفاعل ↼ {tfa3l}
'''
      return await message.reply_text(text)

   if text == 'بايو' and message.reply_to_message and message.reply_to_message.from_user:
      if r.get(f'{chat.id}:disableBio:{Dev_Zaid}'):  return
      get = await context.bot.get_chat(message.reply_to_message.from_user.id)
      if not get.bio:
        return await message.reply_text(f'{k} ماعنده بايو')
      else:
        return await message.reply_text(f'`{get.bio}`')

   if text == 'بايو' and not message.reply_to_message:
      if r.get(f'{chat.id}:disableBio:{Dev_Zaid}'):  return
      get = await context.bot.get_chat(user.id)
      if not get.bio:
        return await message.reply_text(f'{k} ماعندك بايو')
      else:
        return await message.reply_text(f'`{get.bio}`')


   if text == 'المجموعه' or text == 'المجموعة':
      try:
        chat_obj = await context.bot.get_chat(chat.id)
        link = chat_obj.invite_link or 'مافي رابط'
        admins_list = await context.bot.get_chat_administrators(chat.id)
        admins = len(admins_list)
        count = chat_obj.get_member_count if callable(getattr(chat_obj, 'get_member_count', None)) else '؟'
        try:
          count = await context.bot.get_chat_member_count(chat.id)
        except:
          count = '؟'
        info_text = f'معلومات المجموعة:\n\n{k} الاسم ↢ {chat.title}\n{k} الايدي ↢ {chat.id}\n{k} عدد الاعضاء ↢ ( {count} )\n{k} عدد المشرفين ↢ ( {admins} )\n{k} الرابط ↢ {link} '
        if chat.photo:
          if chat.username:
            return await message.reply_photo(f'https://t.me/{chat.username}', caption=info_text)
        return await message.reply_text(info_text, disable_web_page_preview=True)
      except Exception as e:
        print(e)
        return await message.reply_text(f'{k} مافي معلومات للمجموعة')

   if text == 'جهاتي':
     if not r.get(f'{chat.id}TotalContacts{user.id}{Dev_Zaid}'):
       contacts = 0
     else:
       contacts = int(r.get(f'{chat.id}TotalContacts{user.id}{Dev_Zaid}'))
     return await message.reply_text(f'{k} عدد جهاتك ↢ {contacts}')

   if text == 'افتاري':
     if r.get(f'{chat.id}:disableAV:{Dev_Zaid}'): return False
     if not user.photo:
       return await message.reply_text(f'{k} ماقدر اجيب افتارك ارسل نقطه خاص وارجع جرب')
     else:
       if user.username:
         photo = f'http://t.me/{user.username}'
       else:
         _photos = await context.bot.get_user_profile_photos(user.id, limit=1)
         if _photos.total_count > 0:
           photo = _photos.photos[0][-1].file_id
       get_bio_obj = await context.bot.get_chat(user.id)

       get_bio = getattr(get_bio_obj, "bio", None)
       if not get_bio:
         caption=None
       else:
         caption = f'`{get_bio}`'
       return await message.reply_photo(photo,caption=caption)

   if text == 'افتار' and message.reply_to_message and message.reply_to_message.from_user:
     if r.get(f'{chat.id}:disableAV:{Dev_Zaid}'): return False
     if not message.reply_to_message.from_user.photo:
       return await message.reply_text(f'{k} مقدر اجيب افتاره يمكن حاظرني')
     else:
       if message.reply_to_message.from_user.username:
         photo = f'http://t.me/{message.reply_to_message.from_user.username}'
       else:
         _photos = await context.bot.get_user_profile_photos(message.reply_to_message.from_user.id, limit=1)
         if _photos.total_count > 0:
           photo = _photos.photos[0][-1].file_id
       get_bio_obj = await context.bot.get_chat(message.reply_to_message.from_user.id)

       get_bio = getattr(get_bio_obj, "bio", None)
       if not get_bio:
         caption=None
       else:
         caption = f'`{get_bio}`'
       return await message.reply_photo(photo,caption=caption)

   if text == 'ايديي':
     return await message.reply_text(f'( `{user.id}` )')

   if text.startswith('افتار') and len(text.split()) == 2:
     if r.get(f'{chat.id}:disableAV:{Dev_Zaid}'): return False
     try:
       user = int(text.split()[1])
     except:
       user = text.split()[1]
     try:
       get = await context.bot.get_chat(user)
       if get.photo:
         _photos = await context.bot.get_user_profile_photos(get.id, limit=1)
         if _photos.total_count > 0:
           photo = _photos.photos[0][-1].file_id
         if get.bio:
           caption = f'`{get.bio}`'
         else:
           caption = None
         return await message.reply_photo(photo,caption=caption)
     except Exception as e:
       print (e)
       return


   if text == 'رتبتي':
      rank = get_rank(user.id, chat.id)
      await message.reply_text(f'{k} رتبتك ↢ {rank}')

   if text == 'مسح رسائلي' or text == 'مسح رسايلي':
      msgs = int(r.get(f'{Dev_Zaid}{chat.id}:TotalMsgs:{user.id}') or 0)
      r.delete(f'{Dev_Zaid}{chat.id}:TotalMsgs:{user.id}')
      return await message.reply_text(f'{k} ابشر مسحت ( {msgs} ) من رسائلك')

   if text == 'مسح تكليجاتي':
      if not r.get(f'{chat.id}:TotalEDMsgs:{user.id}{Dev_Zaid}'):
        return await message.reply_text(f'{k} عدد تكليجاتك ↢ 0')
      msgs = int(r.get(f'{chat.id}:TotalEDMsgs:{user.id}{Dev_Zaid}'))
      r.delete(f'{chat.id}:TotalEDMsgs:{user.id}{Dev_Zaid}')
      return await message.reply_text(f'{k} ابشر مسحت ( {msgs} ) من تكليجاتك')

   if text == 'تكليجاتي' or text == 'تعديلاتي':
      if not r.get(f'{chat.id}:TotalEDMsgs:{user.id}{Dev_Zaid}'):
        return await message.reply_text(f'{k} عدد تكليجاتك ↢ 0')
      msgs = int(r.get(f'{chat.id}:TotalEDMsgs:{user.id}{Dev_Zaid}'))
      return await message.reply_text(f'{k} عدد تكليجاتك ↢ {msgs}')

   if text == 'رسايلي' or text == 'رسائلي':
      msgs = int(r.get(f'{Dev_Zaid}{chat.id}:TotalMsgs:{user.id}') or 0)
      return await message.reply_text(f'{k} عدد رسايلك ↢ {msgs}')
      
   if (text == 'رسايله' or text == 'رسائلة') and message.reply_to_message and message.reply_to_message.from_user:
      msgs = int(r.get(f'{Dev_Zaid}{chat.id}:TotalMsgs:{message.reply_to_message.from_user.id}') or 0)
      return await message.reply_text(f'{k} عدد رسايله ↢ {msgs}')




   if text == 'رتبته' and message.reply_to_message and message.reply_to_message.from_user:
      rank = get_rank(message.reply_to_message.from_user.id, chat.id)
      try:
        _cm = await context.bot.get_chat_member(chat.id, message.reply_to_message.from_user.id)
        status = _cm.status
      except:
        status = None
      if status == ChatMemberStatus.OWNER:
        rank2 = 'المالك'
      elif status == ChatMemberStatus.ADMINISTRATOR:
        rank2 = 'مشرف'
      elif status == ChatMemberStatus.RESTRICTED:
        rank2 = 'مقيد'
      elif status == ChatMemberStatus.LEFT:
        rank2 = 'طالع'
      elif status == ChatMemberStatus.MEMBER:
        rank2 = 'عضو'
      elif status == ChatMemberStatus.BANNED:
        rank2 = 'لاقم حظر'
      else:
        rank2 = 'غير معروف'
      await message.reply_text(f'رتبته:\n{k} في البوت ( {rank} )\n{k} في المجموعة ( {rank2} )\n-')

   if text == 'نقل ملكية' or text == 'نقل ملكيه':
     if r.get(f'{chat.id}:rankGOWNER:{user.id}{Dev_Zaid}'):
       try:
         _cm = await context.bot.get_chat_member(chat.id, user.id)
         status = _cm.status
       except:
         status = None
       if status == ChatMemberStatus.OWNER:
          return await message.reply_text(f'{k} انت مالك القروب')
       else:
          admins = await context.bot.get_chat_administrators(chat.id)
          for member in admins:
            if member.status == ChatMemberStatus.OWNER:
              if getattr(member.user, 'is_deleted', False):
                return await message.reply_text(f'{k} حساب المالك محذوف')
              else:
                r.delete(f'{chat.id}:rankGOWNER:{user.id}{Dev_Zaid}')
                r.srem(f'{chat.id}:listGOWNER:{Dev_Zaid}', user.id)
                r.set(f'{chat.id}:rankGOWNER:{member.user.id}{Dev_Zaid}', 1)
                r.sadd(f'{chat.id}:listGOWNER:{Dev_Zaid}', member.user.id)
                return await message.reply_text(f'「 {member.user.mention_html()} 」\n{k} نقلت له ملكية المجموعة')

   if text == "مسح المتفاعلين" or text == "تصفير المتفاعلين":
     if not owner_pls(user.id, chat.id):
       return await message.reply_text(f'{k} عذراً الامر يخص ↤〖 المالك 〗فقط .')
     else:
       keys = r.keys(f"{Dev_Zaid}{chat.id}:TotalMsgs:*")
       for _ in keys: r.delete(_)
       return await message.reply_text(f"{k} ابشر مسحت كل المتفاعلين")

   if text == "مسح القروبات" or text == "تصفير القروبات":
     if not devp_pls(user.id, chat.id):
       return await message.reply_text(f'{k} عذراً الامر يخص ↤〖 Dev🎖️ 〗فقط .')
     else:
       keys = r.keys(f"{Dev_Zaid}:TotalGroupMsgs:*")
       for _ in keys: r.delete(_)
       return await message.reply_text(f"{k} ابشر مسحت توب القروبات")

   if text == "ترتيبي" or text == "تفاعلي":
     _uid = user.id
     users_keys = r.keys(f"{Dev_Zaid}{chat.id}:TotalMsgs:*")
     jj = []
     for _ukey in users_keys:
          try:
            _uid2 = int(_ukey.split("TotalMsgs:")[1])
            _msgs = r.get(_ukey)
            jj.append({"id": _uid2, "msgs": int(_msgs)})
          except:
            pass
     top = get_top(jj)
     ids = [i["id"] for i in top]
     try:
       rank = ids.index(_uid) + 1
     except ValueError:
       rank = '؟'
     msgs = int(r.get(f"{Dev_Zaid}{chat.id}:TotalMsgs:{_uid}") or 0)
     return await message.reply_text(f"{k} ترتيبك بالمتفاعلين ↢ {rank}\n{k} رسائلك بالتفاعل ↢ {msgs:,}\n-")

   if text == "المتفاعلين" or text == "توب المتفاعلين":
        users = r.keys(f"{Dev_Zaid}{chat.id}:TotalMsgs:*")
        # print(users)
        jj = []
        for user in users:
                  try:
                    id = int(user.split("TotalMsgs:")[1])
                    # print(id)
                    msgs = r.get(user)
                    name = r.get(f"{id}:bankName") or str(id)
                    jj.append({"name": name, "id": id, "msgs": int(msgs)})
                  except:
                    pass
        top = get_top(jj)
        text = "- توب اكثر 20 متفاعل :\n━━━━━━━━━\n"
        count = 1
        for i in top:
            if count == 21: break
            emoji = get_emoji_bank(count)
            text += f"{emoji}{i['msgs']:,} l [{i['name']}](tg://user?id={i['id']})\n"
            count +=1
        return await context.bot.send_message(chat.id, text, disable_web_page_preview=True, reply_to_message_id=message.message_id)

   if text == "القروبات" or text == "توب القروبات":
        groups = r.keys(f"{Dev_Zaid}:TotalGroupMsgs:*")
        result = []

        for group in groups:
            try:
                chat_id = int(group.split("TotalGroupMsgs:")[1])
                msgs = r.get(group)
                _tmp_chat = await context.bot.get_chat(chat_id)

                group_title = _tmp_chat.title if _tmp_chat else str(chat_id)
                result.append({"group_title": group_title, "chat_id": chat_id, "msgs": int(msgs)})
            except:
                pass

        top_groups = get_top(result)
        response_text = "- توب اكثر 20 قروب متفاعل:\n━━━━━━━━━\n"
        count = 1

        for group in top_groups:
            if count == 21:
                break
            emoji = get_emoji_bank(count)
            response_text += f"{emoji}{group['msgs']:,} l {group['group_title']}\n"
            count += 1

        return await context.bot.send_message(chat.id, response_text, disable_web_page_preview=True, reply_to_message_id=message.message_id)


   if text == 'كشف' and message.reply_to_message and message.reply_to_message.from_user:
       try:
           _rid = message.reply_to_message.from_user.id
           _cm = await context.bot.get_chat_member(chat.id, _rid)
           rank = get_rank(_rid, chat.id)
           name = message.reply_to_message.from_user.first_name
           msgs = int(r.get(f'{Dev_Zaid}{chat.id}:TotalMsgs:{_rid}') or 0)
           id = _rid
           if message.reply_to_message.from_user.username:
               username = f'@{message.reply_to_message.from_user.username}'
           elif getattr(message.reply_to_message.from_user, 'usernames', None):
               username = ''
               for i in message.reply_to_message.from_user.usernames: username += f"@{i.username} "
           else:
               username = 'مافي يوزر'
           status = _cm.status
           if status == ChatMemberStatus.OWNER:
               rank2 = 'المالك'
           elif status == ChatMemberStatus.ADMINISTRATOR:
               rank2 = 'مشرف'
           elif status == ChatMemberStatus.RESTRICTED:
               rank2 = 'مقيد'
           elif status == ChatMemberStatus.LEFT:
               rank2 = 'طالع'
           elif status == ChatMemberStatus.MEMBER:
               rank2 = 'عضو'
           elif status == ChatMemberStatus.BANNED:
               rank2 = 'لاقم حظر'
           else:
               rank2 = 'غير معروف'
           _txt = f'''
{k} الاسم ↢ {name}
{k} الايدي ↢ {id}
{k} اليوزر : ( {username} ) 
{k} الرتبه ↢ ( {rank} )
{k} الرسائل ↢ ( {msgs} )
{k} بالمجموعة ↢ ( {rank2} )
{k} نوع الكشف ↢ بالرد
-
'''
           return await message.reply_text(_txt, disable_web_page_preview=True)
       except:
           return await message.reply_text(f'{k} العضو مو بالمجموعة')

   if text.startswith('كشف') and len(text.split()) > 1 and message.entities:
       _mention_id = None
       for ent in message.entities:
           if ent.type == 'text_mention' and ent.user:
               _mention_id = ent.user.id
               break
       if _mention_id is None:
           pass
       else:
           ks = 'بالمنشن'
           try:
               _cm = await context.bot.get_chat_member(chat.id, _mention_id)
               name = _cm.user.first_name
               id = _cm.user.id
               msgs = int(r.get(f'{Dev_Zaid}{chat.id}:TotalMsgs:{id}') or 0)
               username = f'@{_cm.user.username}' if _cm.user.username else 'ماعنده يوزر'
               status = _cm.status
               if status == ChatMemberStatus.OWNER:
                   rank = 'المالك'
               elif status == ChatMemberStatus.ADMINISTRATOR:
                   rank = 'مشرف'
               elif status == ChatMemberStatus.RESTRICTED:
                   rank = 'مقيد'
               elif status == ChatMemberStatus.LEFT:
                   rank = 'طالع'
               elif status == ChatMemberStatus.MEMBER:
                   rank = 'عضو'
               elif status == ChatMemberStatus.BANNED:
                   rank = 'لاقم حظر'
               else:
                   rank = 'غير معروف'
           except:
               rank = 'طالع'
               try:
                   get = await context.bot.get_chat(_mention_id)
                   name = get.first_name or str(get.id)
                   id = get.id
                   msgs = int(r.get(f'{Dev_Zaid}{chat.id}:TotalMsgs:{get.id}') or 0)
                   username = f'@{get.username}' if get.username else 'ماعنده يوزر'
               except Exception as e:
                   print(e)
                   return
           rank2 = get_rank(id, chat.id)
           _txt = f'''
{k} الاسم ↢ {name}
{k} الايدي ↢{id}
{k} اليوزر : ↢ ( {username} )
{k} الرتبه ↢ ({rank2} )
{k} الرسائل ↢ ( {msgs} )
{k} بالمجموعة ↢ ( {rank} )
{k} نوع الكشف ↢ {ks}
-
        '''
           return await message.reply_text(_txt, disable_web_page_preview=True)

   if text.startswith('كشف') and len(text.split()) == 2:
       try:
           _u = int(text.split()[1])
           ks = 'بالايدي'
       except:
           _u = text.split()[1].replace('@', '')
           ks = 'باليوزر'
       try:
           _cm = await context.bot.get_chat_member(chat.id, _u)
           name = _cm.user.first_name
           id = _cm.user.id
           msgs = int(r.get(f'{Dev_Zaid}{chat.id}:TotalMsgs:{_cm.user.id}') or 0)
           username = f'@{_cm.user.username}' if _cm.user.username else 'ماعنده يوزر'
           status = _cm.status
           if status == ChatMemberStatus.OWNER:
               rank = 'المالك'
           elif status == ChatMemberStatus.ADMINISTRATOR:
               rank = 'مشرف'
           elif status == ChatMemberStatus.RESTRICTED:
               rank = 'مقيد'
           elif status == ChatMemberStatus.LEFT:
               rank = 'طالع'
           elif status == ChatMemberStatus.MEMBER:
               rank = 'عضو'
           elif status == ChatMemberStatus.BANNED:
               rank = 'لاقم حظر'
           else:
               rank = 'غير معروف'
       except:
           rank = 'طالع'
           try:
               get = await context.bot.get_chat(_u)
               name = get.first_name or str(get.id)
               id = get.id
               msgs = int(r.get(f'{Dev_Zaid}{chat.id}:TotalMsgs:{get.id}') or 0)
               username = f'@{get.username}' if get.username else 'ماعنده يوزر'
           except Exception as e:
               print(e)
               return
       rank2 = get_rank(id, chat.id)
       _txt = f'''
{k} الاسم ↢ {name}
{k} الايدي ↢{id}
{k} اليوزر : ↢ ( {username} )
{k} الرتبه ↢ ({rank2} )
{k} الرسائل ↢ ( {msgs} )
{k} بالمجموعة ↢ ( {rank} )
{k} نوع الكشف ↢ {ks}
-
        '''
       return await message.reply_text(_txt, disable_web_page_preview=True)


   if text == 'صلاحياته' and message.reply_to_message and message.reply_to_message.from_user:
      try:
        get = await context.bot.get_chat_member(chat.id, message.reply_to_message.from_user.id)
      except:
        return await message.reply_text(f'{k} ما قدرت أجيب معلوماته')
      if get.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
         return await message.reply_text(f'{k} هو العضو وما عنده صلاحيات')
      if get.status == ChatMemberStatus.OWNER:
         return await message.reply_text(f'{k} هو المالك وعنده كل الصلاحيات')
      if get.status == ChatMemberStatus.ADMINISTRATOR:
         p1 = "✔️" if getattr(get, 'can_manage_chat', False) else "✖️"
         p2 = "✔️" if getattr(get, 'can_delete_messages', False) else "✖️"
         p3 = "✔️" if getattr(get, 'can_manage_video_chats', False) else "✖️"
         p4 = "✔️" if getattr(get, 'can_restrict_members', False) else "✖️"
         p5 = "✔️" if getattr(get, 'can_promote_members', False) else "✖️"
         p6 = "✔️" if getattr(get, 'can_change_info', False) else "✖️"
         p7 = "✔️" if getattr(get, 'can_pin_messages', False) else "✖️"
         _txt = f'''
{k} هو مشرف وهذي صلاحياته :

1) - ادارة المجموعة ↼ ( {p1} )
2) - مسح الرسائل ↼ ( {p2} )
3) - ادارة مكالمات ↼ ( {p3} )
4) - تقييد الأعضاء وحظرهم ↼ ( {p4} )
5) - رفع المشرفين ↼ ( {p5} )
6) - تعديل معلومات المجموعة ↼ ( {p6} )
7) - تثبيت الرسايل ↼ ( {p7} )


'''
         return await message.reply_text(_txt)

   if text == 'صلاحياتي':
      try:
        get = await context.bot.get_chat_member(chat.id, user.id)
      except:
        return await message.reply_text(f'{k} ما قدرت أجيب معلوماتك')
      if get.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
         return await message.reply_text(f'{k} انت العضو وماعندك صلاحيات')
      if get.status == ChatMemberStatus.OWNER:
         return await message.reply_text(f'{k} انت المالك وعندك كل الصلاحيات')
      if get.status == ChatMemberStatus.ADMINISTRATOR:
         p1 = "✔️" if getattr(get, 'can_manage_chat', False) else "✖️"
         p2 = "✔️" if getattr(get, 'can_delete_messages', False) else "✖️"
         p3 = "✔️" if getattr(get, 'can_manage_video_chats', False) else "✖️"
         p4 = "✔️" if getattr(get, 'can_restrict_members', False) else "✖️"
         p5 = "✔️" if getattr(get, 'can_promote_members', False) else "✖️"
         p6 = "✔️" if getattr(get, 'can_change_info', False) else "✖️"
         p7 = "✔️" if getattr(get, 'can_pin_messages', False) else "✖️"
         _txt = f'''
{k} انت مشرف وهذي صلاحياتك :

1) - ادارة المجموعة ↼ ( {p1} )
2) - مسح الرسائل ↼ ( {p2} )
3) - ادارة مكالمات ↼ ( {p3} )
4) - تقييد الأعضاء وحظرهم ↼ ( {p4} )
5) - رفع المشرفين ↼ ( {p5} )
6) - تعديل معلومات المجموعة ↼ ( {p6} )
7) - تثبيت الرسايل ↼ ( {p7} )


'''
         return await message.reply_text(_txt)


   if r.get(f'{chat.id}:addCustomID:{user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{chat.id}:addCustomID:{user.id}{Dev_Zaid}')
     await message.reply_text(f'{k} ابشر تم الغاء تعيين الايدي ')
     return

   if r.get(f'{chat.id}:addCustomIDG:{user.id}{Dev_Zaid}') and text == 'الغاء':
     r.delete(f'{chat.id}:addCustomIDG:{user.id}{Dev_Zaid}')
     await message.reply_text(f'{k} ابشر تم الغاء تعيين الايدي عام')
     return

   if r.get(f'{chat.id}:addCustomIDG:{user.id}{Dev_Zaid}') and dev_pls(user.id, chat.id):
      r.set(f'customID:{Dev_Zaid}', message.text)
      await message.reply_text(f'{k} وسوينا الايدي العام\n{k} يمديك تجرب شكل الايدي الجديد الحين')
      r.delete(f'{chat.id}:addCustomIDG:{user.id}{Dev_Zaid}')
      return

   if r.get(f'{chat.id}:addCustomID:{user.id}{Dev_Zaid}') and mod_pls(user.id, chat.id):
      r.set(f'{chat.id}:customID:{Dev_Zaid}', message.text)
      await message.reply_text(f'{k} وسوينا الايدي\n{k} يمديك تجرب شكل الايدي الجديد الحين')
      r.delete(f'{chat.id}:addCustomID:{user.id}{Dev_Zaid}')
      return

   if text == 'مسح الايدي':
      if not mod_pls(user.id, chat.id):
        return await message.reply_text(f'{k} عذراً الامر يخص ↤〖 المدير 〗فقط .')
      if not r.get(f'{chat.id}:customID:{Dev_Zaid}'):
        return await message.reply_text(f'{k} الايدي مو معدل')
      else:
        await message.reply_text(f'{k} ابشر مسحت الايدي')
        r.delete(f'{chat.id}:customID:{Dev_Zaid}')
        return

   if text == 'مسح الايدي العام' or text == 'مسح الايدي عام':
      if not dev2_pls(user.id, chat.id):
        return await message.reply_text(f'{k} عذراً الامر يخص ↤〖 Dev²🎖 〗فقط .')
      if not r.get(f'customID:{Dev_Zaid}'):
        return await message.reply_text(f'{k} الايدي العام مو معدل')
      else:
        await message.reply_text(f'{k} ابشر مسحت الايدي العام')
        r.delete(f'customID:{Dev_Zaid}')

   if text == 'الايدي':
      if not mod_pls(user.id, chat.id):
        return
      if not r.get(f'{chat.id}:customID:{Dev_Zaid}'):
        return await message.reply_text(f'{k} الايدي مو معدل')
      else:
        id = r.get(f'{chat.id}:customID:{Dev_Zaid}')
        return await message.reply_text(f'`{id}`')

   if text == 'الايدي العام':
      if not dev2_pls(user.id, chat.id):
        return
      if not r.get(f'customID:{Dev_Zaid}'):
        return await message.reply_text(f'{k} الايدي العام مو معدل')
      else:
        id = r.get(f'customID:{Dev_Zaid}')
        return await message.reply_text(f'`{id}`')

   if text == 'تغيير الايدي':
      if not mod_pls(user.id, chat.id):
        return await message.reply_text(f'{k} عذراً الامر يخص ↤〖 المدير 〗فقط .')
      else:
        id = random.choice(custom_ids)
        r.set(f'{chat.id}:customID:{Dev_Zaid}', id)
        await message.reply_text(f'{k} وسوينا الايدي\n{k} يمديك تجرب شكل الايدي الجديد الحين')

   if text == 'تعيين الايدي':
      if not mod_pls(user.id, chat.id):
        return await message.reply_text(f'{k} عذراً الامر يخص ↤〖 المدير 〗فقط .')
      reply = '''
تمام , الحين ارسل شكل الايدي الجديد

- الاختصارات:

{الاسم} ↼ يطلع اسم الشخص
{الايدي} ↼ يطلع ايدي الشخص
{اليوزر} ↼ يطلع يوزر الشخص
{الرتبه} ↼ يطلع رتبته الشخص
{التفاعل} ↼ يطلع تفاعل الشخص
{الرسائل} ↼ يطلع كم رسالة عند الشخص
{التعديل} ↼ يطلع كم مره عدل الشخص
{البايو} ↼ يطلع البايو اللي كاتبه
{تعليق} ↼ يطلع تعليق عشوائي
{الانشاء} ↼ يطلع انشاء الحساب

قناة اشكال الايدي https://t.me/scatteredda

'''
      await message.reply_text(reply)
      r.set(f'{chat.id}:addCustomID:{user.id}{Dev_Zaid}', 1)
      return
   if text == 'تعيين الايدي عام':
      if not dev2_pls(user.id, chat.id):
        return await message.reply_text(f'{k} عذراً الامر يخص ↤〖 Dev²🎖 〗فقط .')
      reply = '''
تمام , الحين ارسل شكل الايدي الجديد

- الاختصارات:

{الاسم} ↼ يطلع اسم الشخص
{الايدي} ↼ يطلع ايدي الشخص
{اليوزر} ↼ يطلع يوزر الشخص
{الرتبه} ↼ يطلع رتبته الشخص
{التفاعل} ↼ يطلع تفاعل الشخص
{الرسائل} ↼ يطلع كم رسالة عند الشخص
{التعديل} ↼ يطلع كم مره عدل الشخص
{البايو} ↼ يطلع البايو اللي كاتبه
{تعليق} ↼ يطلع تعليق عشوائي
{الانشاء} ↼ يطلع انشاء الحساب

قناة اشكال الايدي https://t.me/scatteredda
'''
      await message.reply_text(reply)
      r.set(f'{chat.id}:addCustomIDG:{user.id}{Dev_Zaid}', 1)
      return True


   if text == 'تفعيل الايدي':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} عذراً الامر يخص ↤〖 الادمن 〗فقط .')
     else:
       if not r.get(f'{chat.id}:disableID:{Dev_Zaid}'):
         return await message.reply_text(f'{k} بواسطة ↤ {user.mention_html()}\n{k} الايدي مفعل من قبل')
       else:
         r.delete(f'{chat.id}:disableID:{Dev_Zaid}')
         return await message.reply_text(f'{k} بواسطة ↤ {user.mention_html()}\n{k} ابشر فعلت الايدي')

   if text == 'تعطيل الايدي':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} عذراً الامر يخص ↤〖 الادمن 〗فقط .')
     else:
       if r.get(f'{chat.id}:disableID:{Dev_Zaid}'):
         return await message.reply_text(f'{k} بواسطة ↤ {user.mention_html()}\n{k} الايدي معطل من قبل')
       else:
         r.set(f'{chat.id}:disableID:{Dev_Zaid}',1)
         return await message.reply_text(f'{k} بواسطة ↤ {user.mention_html()}\n{k} ابشر عطلت الايدي')

   if text == 'تفعيل افتاري':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} عذراً الامر يخص ↤〖 الادمن 〗فقط .')
     else:
       if not r.get(f'{chat.id}:disableAV:{Dev_Zaid}'):
         return await message.reply_text(f'{k} بواسطة ↤ {user.mention_html()}\n{k} افتار مفعل من قبل')
       else:
         r.delete(f'{chat.id}:disableAV:{Dev_Zaid}')
         return await message.reply_text(f'{k} بواسطة ↤ {user.mention_html()}\n{k} ابشر فعلت افتار')

   if text == 'تعطيل افتاري':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} عذراً الامر يخص ↤〖 الادمن 〗فقط .')
     else:
       if r.get(f'{chat.id}:disableAV:{Dev_Zaid}'):
         return await message.reply_text(f'{k} بواسطة ↤ {user.mention_html()}\n{k} افتار معطل من قبل')
       else:
         r.set(f'{chat.id}:disableAV:{Dev_Zaid}',1)
         return await message.reply_text(f'{k} بواسطة ↤ {user.mention_html()}\n{k} ابشر عطلت افتار')

   if text == 'تعطيل الايدي بالصوره':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} عذراً الامر يخص ↤〖 الادمن 〗فقط .')
     else:
       if r.get(f'{chat.id}:disableIDPHOTO:{Dev_Zaid}'):
         return await message.reply_text(f'{k} بواسطة ↤ {user.mention_html()}\n{k} الايدي بالصوره معطل من قبل')
       else:
         r.set(f'{chat.id}:disableIDPHOTO:{Dev_Zaid}',1)
         return await message.reply_text(f'{k} بواسطة ↤ {user.mention_html()}\n{k} ابشر عطلت الايدي بالصوره')

   if text == 'تفعيل الايدي بالصوره':
     if not admin_pls(user.id,chat.id):
       return await message.reply_text(f'{k} عذراً الامر يخص ↤〖 الادمن 〗فقط .')
     else:
       if not r.get(f'{chat.id}:disableIDPHOTO:{Dev_Zaid}'):
         return await message.reply_text(f'{k} بواسطة ↤ {user.mention_html()}\n{k} الايدي بالصوره مفعل من قبل')
       else:
         r.delete(f'{chat.id}:disableIDPHOTO:{Dev_Zaid}')
         return await message.reply_text(f'{k} بواسطة ↤ {user.mention_html()}\n{k} ابشر فعلت الايدي بالصوره')

   if text == "لقبي":
     try:
       _cm = await context.bot.get_chat_member(chat.id, user.id)
       title = getattr(_cm, 'custom_title', None)
     except:
       title = None
     if not title:
       return await message.reply_text(f"{k} ماعندك لقب")
     else:
       return await message.reply_text(f"{k} لقبك ↢ ( {title} )")

   if (text == 'ايدي' or text.lower() == 'ا') and message.reply_to_message and message.reply_to_message.from_user:
       return await message.reply_text(f'الايدي ↢ ( `{message.reply_to_message.from_user.id}` )')

   if (text == 'ايدي' or text.lower() == 'id') and not message.reply_to_message:
      if r.get(f'{chat.id}:disableID:{Dev_Zaid}'):  return
      if r.get(f'{chat.id}:customID:{Dev_Zaid}'):
         id = r.get(f'{chat.id}:customID:{Dev_Zaid}')
      else:
         if r.get(f'customID:{Dev_Zaid}'):
           id = r.get(f'customID:{Dev_Zaid}')
         else:
           id = '''
𖡋 𝐔𝐒𝐄 ⌯  {اليوزر}
𖡋 𝐌𝐒𝐆 ⌯  {الرسائل}
𖡋 𝐒𝐓𝐀 ⌯  {الرتبه}
𖡋 𝐈𝐃 ⌯  {الايدي}
𖡋 𝐄𝐃𝐈𝐓 ⌯  {التعديل}
𖡋 𝐂𝐑  ⌯  {الانشاء}
{البايو}'''
      if user.usernames:
         username = ''
         for i in user.usernames: username += f"@{i.username} "
      elif user.username:
         username = f'@{user.username}'
      else:
         username = 'مافي يوزر'
      rank = get_rank(user.id, chat.id)
      msg = int(r.get(f'{Dev_Zaid}{chat.id}:TotalMsgs:{user.id}') or 0)
      msgs = f"{msg}"
      iD = f'`{user.id}`'
      if not r.get(f'{chat.id}:TotalEDMsgs:{user.id}{Dev_Zaid}'):
         edits = 0
      else:
         edit = int(r.get(f'{chat.id}:TotalEDMsgs:{user.id}{Dev_Zaid}') or 0)
         edits = f"{edit}"
      name = user.first_name
      create = get_creation_date(user.id)
      try:
        get_chat = await context.bot.get_chat(user.id)
        bio = get_chat.bio or 'مافي بايو'
      except:
        bio = 'مافي بايو'
      if msg > 10000:
        tfa3l = 'اسطورة التلي'
      elif msg > 5000:
        tfa3l = 'اسطورة التفاعل'
      elif msg > 2500:
        tfa3l = 'متفاعل'
      elif msg > 750:
        tfa3l = 'تفاعل متوسط'
      elif msg > 500:
        tfa3l = 'يجي منك'
      elif msg > 50:
        tfa3l = 'شد حيلك'
      else:
        tfa3l = 'تفاعل صفر'
      comment = random.choice(comments)
      text = id.replace('{الاسم}', name).replace('{اليوزر}', username).replace('{الرسائل}',str(msgs)).replace('{التعديل}', str(edits)).replace('{الانشاء}', create).replace('{البايو}', f'{bio}').replace('{الايدي}', iD).replace('{الرتبه}', rank).replace('{التفاعل}', tfa3l).replace('{تعليق}', comment)
      if r.get(f'{chat.id}:disableIDPHOTO:{Dev_Zaid}'):
         return await message.reply_text(text, disable_web_page_preview=True)
      else:
         if user.photo:
           try:
             _photos = await context.bot.get_user_profile_photos(user.id, limit=1)
             if _photos.total_count > 0:
               photo_file_id = _photos.photos[0][-1].file_id
               return await message.reply_photo(photo_file_id, caption=text)
           except:
             pass
         return await message.reply_text(text, disable_web_page_preview=True)


async def addContact(update: Update, context: ContextTypes.DEFAULT_TYPE):
  message = update.message
  user = update.effective_user
  chat = update.effective_chat
  if not message or not user or not chat: return
  new_members = message.new_chat_members or []
  for me in new_members:
    if not user.id == me.id:
      if not r.get(f'{chat.id}TotalContacts{user.id}{Dev_Zaid}'):
        r.set(f'{chat.id}TotalContacts{user.id}{Dev_Zaid}',1)
      else:
        co = int(r.get(f'{chat.id}TotalContacts{user.id}{Dev_Zaid}') or 0)
        r.set(f'{chat.id}TotalContacts{user.id}{Dev_Zaid}',co+1)



async def setIDHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await set_id(update, context, k)


async def set_id(update, context, k):
    message = update.message
    chat = update.effective_chat
    user = update.effective_user
    if not message or not chat or not user: return
    if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):  return
    if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return
    if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return
    if r.get(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}'):  return
    if r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}'):  return
    text = message.text
    if r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}'):
       text = r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}')
    if r.get(f'Custom:{Dev_Zaid}&text={text}'):
       text = r.get(f'Custom:{Dev_Zaid}&text={text}')






def register(app):
    """Register id handlers."""
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(
        filters.ALL & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
        rankGetHandler
    ), group=18)
    app.add_handler(MessageHandler(
        filters.TEXT & (filters.ChatType.GROUPS | filters.ChatType.PRIVATE),
        setIDHandler
    ), group=41)
