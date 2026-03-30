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




from io import BytesIO
from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ChatPermissions, InputMediaAudio, InputMediaVideo, InputMediaPhoto,
    InputMediaDocument, InputTextMessageContent, InlineQueryResultArticle,
    InlineQueryResultAudio)
from telegram.constants import ParseMode, ChatMemberStatus, ChatType
from telegram.error import BadRequest, RetryAfter, Forbidden
from telegram.ext import ContextTypes, MessageHandler, filters
import asyncio

from config import *
from .all import list_UwU
from helpers.Ranks import *
from helpers.quran import *
from helpers.memes import *

class _DummyClient:
    @staticmethod
    def on_callback_query(*args, **kwargs):
        def decorator(func): return func
        return decorator
    @staticmethod
    def on_chat_member_updated(*args, **kwargs):
        def decorator(func): return func
        return decorator
    @staticmethod
    def on_raw_update(*args, **kwargs):
        def decorator(func): return func
        return decorator

Client = _DummyClient()

###########################################################################
###########################################################################
'''
def kick_from_group(app: Client, m: Update, _, __):
   try:
      name = re.search(r"first_name='([^']+)'", str(_)).group(1)
      title = re.search(r"title='([^']+)'", str(__)).group(1)
      get = app.get_me()
      if 'types.ChannelParticipantBanned' in str(m) and '"is_self": true' in str(m):
        r.delete(f'{chat.id}:enable:{Dev_Zaid}', int(f'-100{message.channel_id}'))
        r.srem(f'enablelist:{Dev_Zaid}', int(f'-100{message.channel_id}'))
      else:
        return False
      text = '{k} تم طرد البوت من مجموعة:\n\n'
      text += f'{k} اسم الي طردني : [{name}](tg://user?id={message.new_participant.kicked_by})\n'
      text += f'{k} ايدي الي طردني : {message.new_participant.kicked_by}\n'
      text += f'\n{k} معلومات المجموعة: \n'
      text += f'\n{k} ايدي المجموعة: `-100{message.channel_id}`'
      text += f'\n{k} اسم المجموعه: {title}'
      text += '\n{k} تم مسح جميع بيانات المجموعة'
      text += '\n\n༄'
      if r.get(f'DevGroup:{Dev_Zaid}'):
        app.send_message(int(r.get(f'DevGroup:{Dev_Zaid}')),text,disable_web_page_preview=True)
      else:
        for dev in get_devs_br():
          try:
            app.send_message(int(dev), text, disable_web_page_preview=True)
            await asyncio.sleep(0.05)
          except:
            pass
   except Exception as e:
     print (e)
''' 
## الردود
async def globalHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
   await global_filter(update, context)

async def global_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
   message = update.message
   chat = update.effective_chat
   user = update.effective_user
   if not message or not chat or not user:
       return
   if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return
   if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return
   if r.get(f'{chat.id}:lock_global:{Dev_Zaid}'):  return
   if r.get(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}'):  return
   if r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}'):  return
   if r.get(f'{chat.id}:addFilterG:{user.id}{Dev_Zaid}'):  return
   if r.get(f'{chat.id}:delFilterG:{user.id}{Dev_Zaid}'):  return
   if r.get(f'{chat.id}:addFilter2GG:{user.id}{Dev_Zaid}'):  return
   text = message.text or ''
   name = r.get(f'{Dev_Zaid}:BotName') or NAME
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{text}:filter:{Dev_Zaid}'):
     get = r.get(f'{text}:filter:{Dev_Zaid}')
     type = re.search(r'type=([^&]+)', get).group(1)
     userID = str(user.id)
     userNAME = str(user.first_name)
     userUSERNAME = "@"+user.username if user.username else "مافي يوزر"
     userMENTION = user.mention_html()
     if type == 'text':
        return await message.reply_text(get.split('&text=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION), disable_web_page_preview=True)
     
     if type == 'photo':
        photo = re.search(r'photo=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        return await message.reply_photo(photo, caption=cpt)
     
     if type == 'video':
        video = re.search(r'video=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        return await message.reply_video(video, caption=cpt)
     
     if type == 'voice':
        voice = re.search(r'voice=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        return await message.reply_voice(voice, caption=cpt)
     
     if type == 'animation':
        animation = re.search(r'animation=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        return await message.reply_animation(animation, caption=cpt)
     
     if type == 'audio':
        audio = re.search(r'audio=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        return await message.reply_audio(audio, caption=cpt)
     
     if type == 'doc':
        doc = re.search(r'doc=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        return await message.reply_document(doc, caption=cpt)

     if type == 'sticker':
        return await message.reply_sticker(get.split('&sticker=')[1])
   
   
   
   if text == 'المطور':
     id = int(r.get(f'{Dev_Zaid}botowner') or 0)
     bio = None
     reply_markup = InlineKeyboardMarkup(
       [[InlineKeyboardButton("مستخدم", user_id=id)]]
     )
     return await message.reply_animation(
       'https://telegra.ph/file/d9127c65922817d127f04.mp4',
       caption=bio, reply_markup=reply_markup
     )
        
        
        
async def filtersHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
   await get_filter(update, context)

async def get_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
   message = update.message
   chat = update.effective_chat
   user = update.effective_user
   if not message or not chat or not user:
       return
   if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return 
   if r.get(f'{chat.id}:addFilter:{user.id}{Dev_Zaid}'):  return
   if r.get(f'{chat.id}:delFilter:{user.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:lock_filter:{Dev_Zaid}'):  return 
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}'):  return 
   text = message.text or ''
   name = r.get(f'{Dev_Zaid}:BotName') or NAME
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{text}:filter:{Dev_Zaid}{chat.id}'):
     get = r.get(f'{text}:filter:{Dev_Zaid}{chat.id}')
     type = re.search(r'type=([^&]+)', get).group(1)
     userID = str(user.id)
     userNAME = str(user.first_name)
     userUSERNAME = "@"+user.username if user.username else "مافي يوزر"
     userMENTION = user.mention_html()
     if type == 'text':
         await message.reply_text(get.split('&text=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION), disable_web_page_preview=True)
     
     if type == 'photo':
        photo = re.search(r'photo=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        await message.reply_photo(photo, caption=cpt)
     
     if type == 'video':
        video = re.search(r'video=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        await message.reply_video(video, caption=cpt)
     
     if type == 'voice':
        voice = re.search(r'voice=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        await message.reply_voice(voice, caption=cpt)
     
     if type == 'animation':
        animation = re.search(r'animation=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        await message.reply_animation(animation, caption=cpt)
     
     if type == 'audio':
        audio = re.search(r'audio=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        await message.reply_audio(audio, caption=cpt)
     
     if type == 'doc':
        doc = re.search(r'doc=([^&]+)', get).group(1)
        caption = get.split('&caption=')[1].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION)
        if caption == 'None':
           cpt = None
        else:
           cpt = caption
        await message.reply_document(doc, caption=cpt)

     if type == 'sticker':
         await message.reply_sticker(get.split('&sticker=')[1])
     else:
       cap+=f"\n`{None}`"
     if False:
       reply_markup= InlineKeyboardMarkup (
       [[InlineKeyboardButton ("مستخدم", user_id=id)]]
       )
     else:
       reply_markup=None
     if False:
       return await message.reply_text(cap,reply_markup=reply_markup)
     else:
       get_user = None
       photo = None
       hash = photo.access_hash
       if r.get(f"{hash}:{id}"):
         return await message.reply_animation(r.get(f"{hash}:{id}"), caption=cap, reply_markup=reply_markup) 
       video = photo.video_sizes[0] if photo.video_sizes else None
       if video:
         file = BytesIO()
         if False:
           file.write(byte)
           file.name = f'{id}vid.mp4'
           a= message.reply_animation(file, caption=cap,reply_markup=reply_markup)
           return r.set(f"{hash}:{id}", a.animation.file_id, ex=120)
       else:
         if False:
           return await message.reply_photo(photo.file_id, caption=cap, reply_markup=reply_markup)
      



async def globalRandomupdate(update: Update, context: ContextTypes.DEFAULT_TYPE):
   await get_rngp(update, context)
   
async def get_rngp(update: Update, context: ContextTypes.DEFAULT_TYPE):
   message = update.message
   chat = update.effective_chat
   user = update.effective_user
   if not message or not chat or not user:
       return
   if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return
   if r.get(f'{chat.id}:lock_global:{Dev_Zaid}'):  return 
   
   if user:
     if r.get(f'{chat.id}:addFilterRG:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:delFilterRG:{user.id}{Dev_Zaid}'):  return 
     if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return
     if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
   
   text = message.text or ''
   if not text: return
   name = r.get(f'{Dev_Zaid}:BotName') or NAME
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   userID = str(user.id)
   userNAME = str(user.first_name)
   userUSERNAME = "@"+user.username if user.username else "مافي يوزر"
   userMENTION = user.mention_html()
   if r.get(f'{text}:randomFilter:{Dev_Zaid}'):
     if r.smembers(f'{text}:randomfilter:{Dev_Zaid}'):
       list = r.smembers(f'{text}:randomfilter:{Dev_Zaid}')
       return await message.reply_text(random.sample(list,1)[0].replace('{اسم_البوت}',name).replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION), disable_web_page_preview=True)
   name2 = ' '.join(i for i in name)
   
   
   sb = [
"عييييييييب","عيب","ياكلب عيب","يا قليل التربيه","يا قليل الادب","؟؟؟؟؟؟","ياليت تتأدب","بقص لسانك","حاضر","ياخي عيب","؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟","استغفر الله",
   ]
   lovem = [
"يلبيييه",
"اكثر",
"يعمري",
"اعشقك",
"بدينا كذب",
"احلى من يحبني",
"يحظي والله",
"اكثر اكثر اكثرر",
"يروحي",
"اموت فيك",]
   zg = [
"عييييييييب","عيب","زق بوجهك","يا قليل التربيه","يا قليل الادب","؟؟؟؟؟؟","ياليت تتأدب","بقص لسانك","حاضر","ياخي عيب","؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟؟",]
   mm = [
"ابركها من ساعة","احبك","اكثر","ترا ازعجتنا","انقلع","طيب","مو اكثر مني","وبعدين ؟","جت من الله","توكل بس"]
   bot_r = ["أيوه؟","نعم؟","امر","حاضر","لبيك","بأمرك","ايه يا أهلا","هلا","نعم؟ 🧚‍♀️","لبيك يسيدي"]
   bot_name = ["لبيك 🧚‍♀️","أيوه؟ 🧚","نعم؟","حاضر","امر","هلا والله","وينك عيني","لبيك يسيدي","ايه يا أهلا","نعم؟ 🌸"]
   if text == 'بوت':
      await message.reply_text(random.choice(bot_r))
   
   if text == name:
     await message.reply_text(random.choice(bot_name))
     
   '''
   if text in list_UwU:
     await message.reply_text(random.choice(sb))
   '''
   
   if text == 'احبك':
     await message.reply_text(random.choice(lovem))
   
   if text == 'اكرهك':
     await message.reply_text(random.choice(mm))
   
   if text == 'كليزق' or text == 'كلزق':
     await message.reply_text(random.choice(zg))
   
   if text.startswith('سورة ') or text.startswith('سوره '):
      soura = text.split(None,1)[1].replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٰ','').replace('ة','ه')
      if f'سورة {soura}' in TheHolyQuran:
        title = random.choice(["﴿ سَبِّحِ اسمَ رَبِّكَ الأَعلَى ﴾","﴿ وَلَلآخِرَةُ خَيرٌ لَكَ مِنَ الأولى ﴾","﴿ وَكانَ ذلِكَ عَلَى اللَّهِ يَسيرًا ﴾","﴿ لِمَن شاءَ مِنكُم أَن يَتَقَدَّمَ أَو يَتَأَخَّرَ ﴾","﴿ فَمَن عَفا وَأَصلَحَ فَأَجرُهُ عَلَى اللَّهِ ﴾","﴿ هُوَ أَهلُ التَّقوى وَأَهلُ المَغفِرَةِ ﴾","﴿ هَل جَزاءُ الإِحسانِ إِلَّا الإِحسانُ ﴾","﴿ وَلا يَظلِمُ رَبُّكَ أَحَدًا ﴾","﴿ وَمَن يُؤمِن بِاللَّهِ يَهدِ قَلبَهُ ﴾","﴿ وَكانَ رَبُّكَ قَديرًا ﴾","﴿ وَتَطمَئِنُّ قُلوبُهُم بِذِكرِ اللَّهِ ﴾","﴿ سَيَهديهِم وَيُصلِحُ بالَهُم ﴾","﴿ وَوَجَدَكَ ضالًّا فَهَدى ﴾","﴿ فَاسعَوا إِلى ذِكرِ اللَّهِ ﴾","( إِنّ السّاعَةَ آتِيَةٌ أَكَادُ أُخْفِيهَا )","﴿وَلا تَكونوا كَالَّذينَ نَسُوا اللَّهَ فَأَنساهُم أَنفُسَهُم﴾."," ‏﴿أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ﴾ ","﴿ وَقُلْ رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا ﴾♡.","‏{وَعَسَىٰ أَن تَكْرَهُوا شَيْئًا وَهُوَ خَيْرٌ لَّكُمْ}","{ لاتحزَن إِنَّ الله مَعَنا }"])
        return await message.reply_audio(
          MaherAlmaikulai[f"سورة {soura}"],
          caption=f'سورة {soura}',
          reply_markup=InlineKeyboardMarkup (
            [
            [
              InlineKeyboardButton (title,url='https://t.me/scatteredda')
            ],
            [
              InlineKeyboardButton ('بصوت سعد الغامدي',callback_data=f'{user.id}quSaad={MaherAlmaikulai[f"سورة {soura}"].split("MaherSounds/")[1]}')
            ],
            [
              InlineKeyboardButton ('بصوت عبد الباسط عبد الصمد',callback_data=f'{user.id}quBaset={MaherAlmaikulai[f"سورة {soura}"].split("MaherSounds/")[1]}')
            ],
            [
              InlineKeyboardButton ('بصوت مشاري راشد العفاسي',callback_data=f'{user.id}qu3fasy={MaherAlmaikulai[f"سورة {soura}"].split("MaherSounds/")[1]}')
            ]
            ]
          )
        )
   
   if text == 'ميمز':
     randomMeme = random.choice(memes_sa)
     return await message.reply_audio(
     randomMeme["url"],caption=randomMeme["title"],
     reply_markup=InlineKeyboardMarkup (
       [
         [InlineKeyboardButton ('🇸🇾',callback_data=f'{user.id}memes_sy'),InlineKeyboardButton ('🇪🇬',callback_data=f'{user.id}memes_eg')],
         [InlineKeyboardButton ('🇸🇦',callback_data=f'{user.id}memes_sa'),InlineKeyboardButton ('🇦🇪',callback_data=f'{user.id}memes_ae')],
         [InlineKeyboardButton ('🇺🇸',callback_data=f'{user.id}memes_us'),InlineKeyboardButton ('🇮🇶',callback_data=f'{user.id}memes_iq'),],
         [InlineKeyboardButton ('🧚‍♀️',url='https://t.me/scatteredda')],
       ]
     )
     )
   #https://raw.githubusercontent.com/maknon/Quran/main/pages-douri/604.png
   if (text.startswith('قرآن ') or text.startswith('قران ')) and re.findall('[0-9]+', text):
     page = int(re.findall('[0-9]+', text)[0])
     if page <= 604:
        title = random.choice(["﴿ سَبِّحِ اسمَ رَبِّكَ الأَعلَى ﴾","﴿ وَلَلآخِرَةُ خَيرٌ لَكَ مِنَ الأولى ﴾","﴿ وَكانَ ذلِكَ عَلَى اللَّهِ يَسيرًا ﴾","﴿ لِمَن شاءَ مِنكُم أَن يَتَقَدَّمَ أَو يَتَأَخَّرَ ﴾","﴿ فَمَن عَفا وَأَصلَحَ فَأَجرُهُ عَلَى اللَّهِ ﴾","﴿ هُوَ أَهلُ التَّقوى وَأَهلُ المَغفِرَةِ ﴾","﴿ هَل جَزاءُ الإِحسانِ إِلَّا الإِحسانُ ﴾","﴿ وَلا يَظلِمُ رَبُّكَ أَحَدًا ﴾","﴿ وَمَن يُؤمِن بِاللَّهِ يَهدِ قَلبَهُ ﴾","﴿ وَكانَ رَبُّكَ قَديرًا ﴾","﴿ وَتَطمَئِنُّ قُلوبُهُم بِذِكرِ اللَّهِ ﴾","﴿ سَيَهديهِم وَيُصلِحُ بالَهُم ﴾","﴿ وَوَجَدَكَ ضالًّا فَهَدى ﴾","﴿ فَاسعَوا إِلى ذِكرِ اللَّهِ ﴾","( إِنّ السّاعَةَ آتِيَةٌ أَكَادُ أُخْفِيهَا )","﴿وَلا تَكونوا كَالَّذينَ نَسُوا اللَّهَ فَأَنساهُم أَنفُسَهُم﴾."," ‏﴿أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ﴾ ","﴿ وَقُلْ رَبِّ ارْحَمْهُمَا كَمَا رَبَّيَانِي صَغِيرًا ﴾♡.","‏{وَعَسَىٰ أَن تَكْرَهُوا شَيْئًا وَهُوَ خَيْرٌ لَّكُمْ}","{ لاتحزَن إِنَّ الله مَعَنا }"])
        return await message.reply_photo(f'https://raw.githubusercontent.com/maknon/Quran/main/pages-douri/{page}.png',reply_markup=InlineKeyboardMarkup (
          [[
            InlineKeyboardButton (title,url='https://t.me/scatteredda')
          ]]
        ))
       

async def memes(update: Update, context: ContextTypes.DEFAULT_TYPE):
   query = update.callback_query
   if not query: return
   user = update.effective_user
   data = query.data
   meme_list = None
   if str(user.id) in data:
     if data.endswith('sy'): meme_list = memes_sy
     elif data.endswith('eg'): meme_list = memes_eg
     elif data.endswith('sa'): meme_list = memes_sa
     elif data.endswith('ae'): meme_list = memes_ae
     elif data.endswith('us'): meme_list = memes_us
     elif data.endswith('iq'): meme_list = memes_iq
     if not meme_list: return
     randomMeme = random.choice(meme_list)
     try:
       await query.answer()
       return await query.edit_message_media(
         media=InputMediaAudio(media=randomMeme["url"], caption=randomMeme["title"]),
         reply_markup=query.message.reply_markup)
     except:
       try:
         await query.message.reply_audio(randomMeme["url"], caption=randomMeme["title"])
       except: pass


async def quranCallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
   query = update.callback_query
   if not query: return
   user = update.effective_user
   data = query.data
   soura = data.split('=')[1] if '=' in data else None
   if not soura: return
   title = random.choice(["﴿ سَبِّحِ اسمَ رَبِّكَ الأَعلَى ﴾","﴿ وَلَلآخِرَةُ خَيرٌ لَكَ مِنَ الأولى ﴾","﴿ وَكانَ ذلِكَ عَلَى اللَّهِ يَسيرًا ﴾","﴿ فَمَن عَفا وَأَصلَحَ فَأَجرُهُ عَلَى اللَّهِ ﴾","﴿ هُوَ أَهلُ التَّقوى وَأَهلُ المَغفِرَةِ ﴾","﴿ هَل جَزاءُ الإِحسانِ إِلَّا الإِحسانُ ﴾","﴿ وَمَن يُؤمِن بِاللَّهِ يَهدِ قَلبَهُ ﴾","﴿ وَتَطمَئِنُّ قُلوبُهُم بِذِكرِ اللَّهِ ﴾","{ لاتحزَن إِنَّ الله مَعَنا }"])
   uid = str(user.id)
   if data.startswith(f'{uid}quSaad'):
      url = f'https://t.me/SaadSounds/{soura}'
      btns = [[InlineKeyboardButton('بصوت ماهر المعيقلي', callback_data=f'{uid}quMaher={soura}')],
              [InlineKeyboardButton('بصوت عبد الباسط', callback_data=f'{uid}quBaset={soura}')],
              [InlineKeyboardButton('بصوت العفاسي', callback_data=f'{uid}qu3fasy={soura}')],
              [InlineKeyboardButton(title, url='https://t.me/scatteredda')]]
   elif data.startswith(f'{uid}quMaher'):
      url = f'https://t.me/MaherSounds/{soura}'
      btns = [[InlineKeyboardButton('بصوت سعد الغامدي', callback_data=f'{uid}quSaad={soura}')],
              [InlineKeyboardButton('بصوت عبد الباسط', callback_data=f'{uid}quBaset={soura}')],
              [InlineKeyboardButton('بصوت العفاسي', callback_data=f'{uid}qu3fasy={soura}')],
              [InlineKeyboardButton(title, url='https://t.me/scatteredda')]]
   elif data.startswith(f'{uid}qu3fasy'):
      url = f'https://t.me/Al3afasy/{soura}'
      btns = [[InlineKeyboardButton('بصوت سعد الغامدي', callback_data=f'{uid}quSaad={soura}')],
              [InlineKeyboardButton('بصوت عبد الباسط', callback_data=f'{uid}quBaset={soura}')],
              [InlineKeyboardButton('بصوت ماهر المعيقلي', callback_data=f'{uid}quMaher={soura}')],
              [InlineKeyboardButton(title, url='https://t.me/scatteredda')]]
   elif data.startswith(f'{uid}quBaset'):
      url = f'https://t.me/AbdAlbasetS/{soura}'
      btns = [[InlineKeyboardButton('بصوت سعد الغامدي', callback_data=f'{uid}quSaad={soura}')],
              [InlineKeyboardButton('بصوت العفاسي', callback_data=f'{uid}qu3fasy={soura}')],
              [InlineKeyboardButton('بصوت ماهر المعيقلي', callback_data=f'{uid}quMaher={soura}')],
              [InlineKeyboardButton(title, url='https://t.me/scatteredda')]]
   else:
      return
   try:
      await query.answer()
      await query.edit_message_media(
        media=InputMediaAudio(media=url, caption=query.message.caption or ''),
        reply_markup=InlineKeyboardMarkup(btns)
      )
   except Exception as e:
      print(f'quranCallback error: {e}')


async def randomfiltersHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
   await get_rn_filter(update, context)
   
   
async def get_rn_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
   message = update.message
   chat = update.effective_chat
   user = update.effective_user
   if not message or not chat or not user: return
   if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):  return
   if r.get(f'{chat.id}:lock_filter:{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return
   if user:
     if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return
     if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
     if r.get(f'{chat.id}:addFilter:{user.id}{Dev_Zaid}'):  return
     if r.get(f'{chat.id}:delFilter:{user.id}{Dev_Zaid}'):  return 
     if r.get(f'{chat.id}:addFilter2:{user.id}{Dev_Zaid}'):  return 
     if r.get(f'{chat.id}:delFilterR:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:addFilterR:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:addFilterR2:{user.id}{Dev_Zaid}'):  return 
   text = message.text or ''
   if not text: return
   name = r.get(f'{Dev_Zaid}:BotName') or NAME
   userID = str(user.id)
   userNAME = str(user.first_name)
   userUSERNAME = "@"+user.username if user.username else "مافي يوزر"
   userMENTION = user.mention_html()
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{text}:randomFilter:{chat.id}{Dev_Zaid}'):
       list = r.smembers(f'{text}:randomfilter:{chat.id}{Dev_Zaid}')
       return await message.reply_text(random.sample(list,1)[0].replace("<USER_ID>",userID).replace("<USER_NAME>",userNAME).replace("<USER_USERNAME>",userUSERNAME).replace("<USER_MENTION>",userMENTION), disable_web_page_preview=True)
     

async def kick_from_gp(update: Update, context: ContextTypes.DEFAULT_TYPE):
   message = update.message
   chat = update.effective_chat
   user = update.effective_user
   if not message or not chat or not user: return
   if message.left_chat_member and message.left_chat_member.id == int(Dev_Zaid):
        k = r.get(f'{Dev_Zaid}:botkey') or '☆'
        text = f'{k} من「 {user.mention_html()} 」\n'
        usrr = '@'+user.username if user.username else 'مافيه'
        text += f'{k} يوزره : {usrr}\n'
        text += f'{k} ايديه : `{user.id}`\n'
        text += f'\n{k} قام بطرد البوت من المجموعة :\n\n'
        text += f'{k} اسم المجموعة : {chat.title}\n'
        chatusr = '@'+chat.username if chat.username else 'مافيه'
        text += f'{k} يوزر المجموعة : {chatusr}\n'
        text += f'{k} ايدي المجموعة : `{chat.id}`'
        r.srem(f'enablelist:{Dev_Zaid}', chat.id)
        r.delete(f'{chat.id}:enable:{Dev_Zaid}')
        if r.smembers(f'enablelist:{Dev_Zaid}'):
          text += f'\n{k} عدد المجموعات الآن : {len(r.smembers(f"enablelist:{Dev_Zaid}"))}\n'
        text += f'\n{k} تم مسح جميع بيانات المجموعة'
        text += '\n\n☆'
        if r.get(f'DevGroup:{Dev_Zaid}'):
            pass
          # context.bot.send_message(int(r.get(f'DevGroup:{Dev_Zaid}')),text,disable_web_page_preview=True)
        else:
          for dev in get_devs_br():
                 try:
                    # context.bot.send_message(int(dev), text, disable_web_page_preview=True)
                    await asyncio.sleep(0.05)
                 except:
                    pass

async def ChatMemberUpdate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    await get_bot_status(update, context, k)
    
async def get_bot_status(update, context, k):
  message = update.message or update.callback_query
  chat = update.effective_chat
  user = update.effective_user
  if not chat: return
  try:
    if message.new_chat_member.status == ChatMemberStatus.MEMBER:
       if message.new_chat_member.user.id == context.bot.id:
         if r.get(f'{chat.id}:enable:{Dev_Zaid}'):
             text = f'{k} من「 {user.mention_html()} 」\n'
             text += f'{k} تم تعطيل المجموعة تلقائياً\n☆'
             # context.bot.send_message(chat.id, text)
             text = f'{k} من「 {user.mention_html()} 」\n'
             usrr = '@'+user.username if user.username else 'مافيه'
             text += f'{k} يوزره : {usrr}\n'
             text += f'{k} ايديه : `{user.id}`\n'
             text += f'\n{k} قام بتنزيل البوت من الأدمن :\n\n'
             text += f'{k} اسم المجموعة : {chat.title}\n'
             chatusr = '@'+chat.username if chat.username else 'مافيه'
             text += f'{k} يوزر المجموعة : {chatusr}\n'
             text += f'{k} ايدي المجموعة : `{chat.id}`'             
             r.srem(f'enablelist:{Dev_Zaid}', chat.id)
             r.delete(f'{chat.id}:enable:{Dev_Zaid}')
             if r.smembers(f'enablelist:{Dev_Zaid}'):
               text += f'\n{k} عدد المجموعات الآن : {len(r.smembers(f"enablelist:{Dev_Zaid}"))}\n'
             text += f'\n{k} تم مسح جميع بيانات المجموعة'
             text += '\n\n☆'
             if r.get(f'DevGroup:{Dev_Zaid}'):
                 pass
                   # context.bot.send_message(int(r.get(f'DevGroup:{Dev_Zaid}')),text)
             else:
               for dev in get_devs_br():
                 try:
                    # context.bot.send_message(int(dev), text, disable_web_page_preview=True)
                    await asyncio.sleep(0.05)
                 except:
                    pass
              
                
    if message.new_chat_member.status == ChatMemberStatus.ADMINISTRATOR:
       if message.new_chat_member.user.id == context.bot.id:
          if r.get(f'{chat.id}:enable:{Dev_Zaid}'):
             priv = message.new_chat_member.privileges
             if not priv.can_manage_chat or not priv.can_delete_messages or not priv.can_restrict_members or not priv.can_pin_messages or not priv.can_invite_users:
                text = f'{k} من「 {user.mention_html()} 」\n'
                text += f'{k} تم تعطيل المجموعة تلقائياً\n☆'
                # context.bot.send_message(chat.id, text)
                r.delete(f'{chat.id}:enable:{Dev_Zaid}')
                text = f'{k} من「 {user.mention_html()} 」\n'
                usrr = '@'+user.username if user.username else 'مافيه'
                text += f'{k} يوزره : {usrr}\n'
                text += f'{k} ايديه : `{user.id}`\n'
                text += f'\n{k} قام بتعديل صلاحية البوت بمجموعة :\n\n'
                text += f'{k} اسم المجموعة : {chat.title}\n'
                chatusr = '@'+chat.username if chat.username else 'مافيه'
                text += f'{k} يوزر المجموعة : {chatusr}\n'
                text += f'{k} ايدي المجموعة : `{chat.id}`'
                if r.smembers(f'enablelist:{Dev_Zaid}'):
                  text += f'\n{k} عدد المجموعات الآن : {len(r.smembers(f"enablelist:{Dev_Zaid}"))}\n'
                text += f'\n{k} تم مسح جميع بيانات المجموعة'
                text += '\n\n☆'
                if r.get(f'DevGroup:{Dev_Zaid}'):
                    pass
                   # context.bot.send_message(int(r.get(f'DevGroup:{Dev_Zaid}')),text,disable_web_page_preview=True)
                else:
                  for dev in get_devs_br():
                    try:
                      # context.bot.send_message(int(dev), text, disable_web_page_preview=True)
                      await asyncio.sleep(0.05)
                    except:
                      pass
                return True
                
          if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):
             if r.get(f'DisableBot:{Dev_Zaid}'):
               return # context.bot.send_message(chat.id, f'{k} تم تعطيل البوت الخدمي من المطور')
             priv = message.new_chat_member.privileges
             if priv.can_manage_chat and priv.can_delete_messages and priv.can_restrict_members and priv.can_pin_messages and priv.can_invite_users:
                text = f'{k} من「 {user.mention_html()} 」\n'
                text += f'{k} تم تفعيل المجموعة تلقائياً\n☆'
                # context.bot.send_message(chat.id, text, reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ('Commands', url=f'https://t.me/{botUsername}?start=Commands')]]))
                r.set(f'{chat.id}:enable:{Dev_Zaid}', 1)
                r.sadd(f'enablelist:{Dev_Zaid}', chat.id)
                r.set(f'{chat.id}:rankOWNER:{user.id}{Dev_Zaid}', 1)
                r.sadd(f'{chat.id}:listOWNER:{Dev_Zaid}', user.id)
                for member in await context.bot.get_chat_administrators(chat.id):
                   if not member.user.is_bot :
                      if member.status == ChatMemberStatus.OWNER:
                         r.set(f'{chat.id}:rankGOWNER:{member.user.id}{Dev_Zaid}', 1)
                         r.sadd(f'{chat.id}:listGOWNER:{Dev_Zaid}', member.user.id)
                         r.sadd(f'{member.user.id}:groups', chat.id)
                      if member.status == ChatMemberStatus.ADMINISTRATOR:
                         r.set(f'{chat.id}:rankADMIN:{member.user.id}{Dev_Zaid}', 1)
                         r.sadd(f'{chat.id}:listADMIN:{Dev_Zaid}', member.user.id)
                get = await context.bot.get_chat(chat.id)
                text = f'{k} من「 {user.mention_html()} 」\n'
                usrr = '@'+user.username if user.username else 'مافيه'
                text += f'{k} يوزره : {usrr}\n'
                text += f'{k} ايديه : `{user.id}`\n'
                text += f'\n{k} تم تفعيل البوت بمجموعة جديدة :\n\n'
                text += f'{k} اسم المجموعة : {chat.title}\n'
                chatusr = '@'+chat.username if chat.username else 'مافيه'
                text += f'{k} يوزر المجموعة : {chatusr}\n'
                text += f'{k} ايدي المجموعة : `{chat.id}`'
                if get.invite_link:
                  reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton (chat.title,url=get.invite_link)]])
                else:
                  reply_markup=None
                if r.smembers(f'enablelist:{Dev_Zaid}'):
                   text += f'\n{k} عدد المجموعات الآن : {len(r.smembers(f"enablelist:{Dev_Zaid}"))}\n'
                text += '\n\n☆'
                if r.get(f'DevGroup:{Dev_Zaid}'):
                    pass
                   # context.bot.send_message(int(r.get(f'DevGroup:{Dev_Zaid}')),text,reply_markup=reply_markup,disable_web_page_preview=True)
                else:
                  for dev in get_devs_br():
                    try:
                      # context.bot.send_message(int(dev), text, disable_web_page_preview=True,reply_markup=reply_markup)  
                      await asyncio.sleep(0.05)
                    except:
                      pass
  except:
    pass
    
                

    
    
async def EnableAndDisablegroup(update: Update, context: ContextTypes.DEFAULT_TYPE):
  message = update.message
  chat = update.effective_chat
  user = update.effective_user
  if not message or not chat or not user: return
  text = message.text or ''
  k = r.get(f'{Dev_Zaid}:botkey') or '☆'
  if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
  if text == 'تفعيل':
    _cm2 = await context.bot.get_chat_member(chat.id, user.id)
    _status = str(_cm2.status).split('.')[-1].lower()
    if _status not in ['owner', 'administrator'] and not owner_pls(user.id,chat.id):
       return await message.reply_text(f'ادري حلم الاعضاء تفعيل البوتات بس اسف')
    if r.get(f'{chat.id}:enable:{Dev_Zaid}'):
        return await message.reply_text(f'{k} المجموعة مفعلة من قبل يالطيب')
    if r.get(f'DisableBot:{Dev_Zaid}'):
       return await context.bot.send_message(chat.id, f'{k} تم تعطيل البوت الخدمي من المطور')
    # Privilege check skipped - PTB handles permissions at runtime
    else:
        r.set(f'{chat.id}:enable:{Dev_Zaid}', 1)
        r.sadd(f'enablelist:{Dev_Zaid}', chat.id)
        r.set(f'{chat.id}:rankOWNER:{user.id}{Dev_Zaid}', 1)
        r.sadd(f'{chat.id}:listOWNER:{Dev_Zaid}', user.id)
        await message.reply_text(f'{k} من「 {user.mention_html()} 」\n{k} ابشر تم تفعيل المجموعة ورفعت كل الادمن\n☆', reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ('Commands', url=f'https://t.me/{botUsername}?start=Commands')]]))
        for member in (await context.bot.get_chat_administrators(chat.id)):
          if not member.user.is_bot :
            mstatus = str(member.status).split('.')[-1].lower()
            if mstatus == 'owner':
              r.set(f'{chat.id}:rankGOWNER:{member.user.id}{Dev_Zaid}', 1)
              r.sadd(f'{chat.id}:listGOWNER:{Dev_Zaid}', member.user.id)
              r.sadd(f'{member.user.id}:groups',chat.id)
            elif mstatus == 'administrator':
              r.set(f'{chat.id}:rankADMIN:{member.user.id}{Dev_Zaid}', 1)
              r.sadd(f'{chat.id}:listADMIN:{Dev_Zaid}', member.user.id)
        usrr = '@'+user.username if user.username else 'مافيه'
        text += f'{k} يوزره : {usrr}\n'
        text += f'{k} ايديه : `{user.id}`\n'
        text += f'\n{k} تم تفعيل البوت بمجموعة جديدة :\n\n'
        text += f'{k} اسم المجموعة : {chat.title}\n'
        chatusr = '@'+chat.username if chat.username else 'مافيه'
        text += f'{k} يوزر المجموعة : {chatusr}\n'
        text += f'{k} ايدي المجموعة : `{chat.id}`'
        if r.smembers(f'enablelist:{Dev_Zaid}'):
           text += f'\n{k} عدد المجموعات الآن : {len(r.smembers(f"enablelist:{Dev_Zaid}"))}\n'
        text += '\n\n☆'
        reply_markup=None
        try:
           invite = await context.bot.export_chat_invite_link(chat.id)
           if invite: reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton (chat.title,url=invite)]])
        except: pass
        if r.get(f'DevGroup:{Dev_Zaid}'):
                   await context.bot.send_message(int(r.get(f'DevGroup:{Dev_Zaid}')),text,reply_markup=reply_markup,disable_web_page_preview=True)
        else:
               for dev in get_devs_br():
                 try:
                    await context.bot.send_message(int(dev), text, disable_web_page_preview=True,reply_markup=reply_markup)
                    await asyncio.sleep(0.05)
                 except:
                    pass
  
  if text == 'تعطيل':
    _cm = await context.bot.get_chat_member(chat.id, user.id)
    if _cm.status not in ['creator','administrator'] and not owner_pls(user.id,chat.id):
       return await message.reply_text('ادري حلم الاعضاء تعطيل البوتات بس اسف')
    else:
      if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):
        return False
      else:
        r.delete(f'{chat.id}:enable:{Dev_Zaid}')
        r.srem(f'enablelist:{Dev_Zaid}', chat.id)
        await message.reply_text(f'{k} من「 {user.mention_html()} 」\n{k} تم تعطيل المجموعة\n☆')
        text = f'{k} من「 {user.mention_html()} 」\n'
        usrr = '@'+user.username if user.username else 'مافيه'
        text += f'{k} يوزره : {usrr}\n'
        text += f'{k} ايديه : `{user.id}`\n'
        text += f'\n{k} تم تعطيل البوت بمجموعة جديدة :\n\n'
        text += f'{k} اسم المجموعة : {chat.title}\n'
        chatusr = '@'+chat.username if chat.username else 'مافيه'
        text += f'{k} يوزر المجموعة : {chatusr}\n'
        text += f'{k} ايدي المجموعة : `{chat.id}`'
        if r.smembers(f'enablelist:{Dev_Zaid}'):
           text += f'\n{k} عدد المجموعات الآن : {len(r.smembers(f"enablelist:{Dev_Zaid}"))}\n'
        text += '\n\n☆'
        if r.get(f'DevGroup:{Dev_Zaid}'):
                   await context.bot.send_message(int(r.get(f'DevGroup:{Dev_Zaid}')),text)
        else:
               for dev in get_devs_br():
                 try:
                    await context.bot.send_message(int(dev), text, disable_web_page_preview=True)
                    await asyncio.sleep(0.05)
                 except:
                    pass
  
  name = r.get(f'{Dev_Zaid}:BotName') or NAME
  if text == f'{name} اطلعي' or text == f'{name} اطلع':
    leave_vids = [
  {'vid':'https://t.me/D7BotResources/154','caption':'غدرتو فيني'},
  {'vid':'https://t.me/D7BotResources/155','caption':':('},
  {'vid':'https://t.me/D7BotResources/156','caption':'يلا خلي البوتات الثانيه تدلعكم'},
  {'vid':'https://t.me/D7BotResources/157','caption':'اسف لي'},
  {'vid':'https://t.me/D7BotResources/158','caption':'قلي منهو لجل عينه تغيرت'},
  {'vid':'https://t.me/D7BotResources/159','caption':'واخيرا برتاح منكم يا نشبه العمر'},]
    if owner_pls(user.id,chat.id):
      r.delete(f'{chat.id}:enable:{Dev_Zaid}')
      r.srem(f'enablelist:{Dev_Zaid}', chat.id)
      vid = random.choice(leave_vids)
      await message.reply_video(vid['vid'], caption=vid['caption'])
      text = f'{k} من「 {user.mention_html()} 」\n'
      usrr = '@'+user.username if user.username else 'مافيه'
      text += f'{k} يوزره : {usrr}\n'
      text += f'{k} ايديه : `{user.id}`\n'
      text += f'\n{k} طلعت من المجموعة بأمر منه :\n\n'
      text += f'{k} اسم المجموعة : {chat.title}\n'
      chatusr = '@'+chat.username if chat.username else 'مافيه'
      text += f'{k} يوزر المجموعة : {chatusr}\n'
      text += f'{k} ايدي المجموعة : `{chat.id}`'
      if r.smembers(f'enablelist:{Dev_Zaid}'):
        text += f'\n{k} عدد المجموعات الآن : {len(r.smembers(f"enablelist:{Dev_Zaid}"))}\n'
      text += '\n\n☆'
      await context.bot.leave_chat(chat.id)
      if r.get(f'DevGroup:{Dev_Zaid}'):
        await context.bot.send_message(int(r.get(f'DevGroup:{Dev_Zaid}')),text)
      else:
        for dev in get_devs_br():
          try:
            await context.bot.send_message(int(dev), text, disable_web_page_preview=True)
          except:
            pass
      
          
     

def register(app):
    """Register group_update handlers."""
    from telegram.ext import MessageHandler, ChatMemberHandler, CallbackQueryHandler, filters
    app.add_handler(MessageHandler(
        filters.ALL & filters.ChatType.GROUPS,
        globalHandler
    ), group=17)
    app.add_handler(MessageHandler(
        filters.ALL & filters.ChatType.GROUPS,
        filtersHandler
    ), group=38)
    app.add_handler(MessageHandler(
        filters.ALL & filters.ChatType.GROUPS,
        randomfiltersHandler
    ), group=39)
    app.add_handler(MessageHandler(
        filters.ALL & filters.ChatType.GROUPS,
        EnableAndDisablegroup
    ), group=40)
    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.GROUPS,
        globalRandomupdate
    ), group=41)
    app.add_handler(CallbackQueryHandler(
        memes, pattern=r'.*memes_(sy|eg|sa|ae|us|iq)$'
    ))
    app.add_handler(CallbackQueryHandler(
        quranCallback, pattern=r'.*qu(Saad|Maher|3fasy|Baset)=.*'
    ))
    try:
        app.add_handler(ChatMemberHandler(ChatMemberUpdate))
    except Exception as e:
        pass
