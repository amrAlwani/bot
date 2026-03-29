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

import yt_dlp,os, requests, re, time, random, json 
from yt_dlp import YoutubeDL
try:
    from pytube import YouTube
except ImportError:
    YouTube = None
try:
    from youtube_search import YoutubeSearch as Y88F8
except ImportError:
    Y88F8 = None



try:
    from shazamio import Shazam
except ImportError:
    Shazam = None

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
from PIL import Image, ImageFilter

# Configurable limits (seconds / bytes). Can be adjusted via environment variables.
MAX_MEDIA_DURATION = int(os.environ.get("MAX_MEDIA_DURATION", "7200"))  # default 2 hours
MAX_SHAZAM_DURATION = int(os.environ.get("MAX_SHAZAM_DURATION", "300"))  # default 5 minutes
MAX_SHAZAM_FILESIZE = int(os.environ.get("MAX_SHAZAM_FILESIZE", "26214400"))  # default 25 MB

# yt-dlp performance tunables (can be set via environment)
YTDLP_MAX_HEIGHT = int(os.environ.get("YTDLP_MAX_HEIGHT", "720"))
YTDLP_CONCURRENT_FRAGMENTS = int(os.environ.get("YTDLP_CONCURRENT_FRAGMENTS", "4"))
YTDLP_FRAGMENT_RETRIES = int(os.environ.get("YTDLP_FRAGMENT_RETRIES", "3"))
YTDLP_USE_EXTERNAL_DOWNLOADER = os.environ.get("YTDLP_USE_EXTERNAL_DOWNLOADER", "false").lower() in ("1", "true", "yes")
YTDLP_EXTERNAL_DOWNLOADER = os.environ.get("YTDLP_EXTERNAL_DOWNLOADER", "aria2c")
YTDLP_EXTERNAL_DOWNLOADER_ARGS = os.environ.get("YTDLP_EXTERNAL_DOWNLOADER_ARGS", "-x 16 -k 1M").split()


def ytdl_opts(format=None, outtmpl=None):
  """Return merged yt-dlp options with performance tuning applied."""
  opts = {
    "quiet": True,
    "no_warnings": True,
    "retries": 3,
    "fragment_retries": YTDLP_FRAGMENT_RETRIES,
    "concurrent_fragment_downloads": YTDLP_CONCURRENT_FRAGMENTS,
  }
  if YTDLP_USE_EXTERNAL_DOWNLOADER:
    opts["external_downloader"] = YTDLP_EXTERNAL_DOWNLOADER
    opts["external_downloader_args"] = YTDLP_EXTERNAL_DOWNLOADER_ARGS
  if format:
    # reduce video resolution to limit size/speed if requested
    if "best" in format and "mp4" in format:
      # prefer height-limited mp4 when downloading video+audio
      opts["format"] = format.replace("best[ext=mp4]", f"bestvideo[height<={YTDLP_MAX_HEIGHT}][ext=mp4]")
    else:
      opts["format"] = format
  if outtmpl:
    opts["outtmpl"] = outtmpl
  return opts

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


#from pySmartDL import SmartDL

shazam = Shazam() if Shazam else None

def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":")))
    )
    
def Find(text):
  m = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»“”‘’]))"
  url = re.findall(m,text)  
  return [x[0] for x in url]

async def ytdownloaderHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'scatteredda'
    await yt_func(update, context, k, channel)
    
async def yt_func(update, context, k, channel):
    
   message = update.message
    
   chat = update.effective_chat
    
   user = update.effective_user
   if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):
        return False 
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return False
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return False 
   if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return False 
   text = message.text
   if isLockCommand(user.id, chat.id, text): return
   rep = InlineKeyboardMarkup (
     [[
       InlineKeyboardButton ('🧚‍♀️', url=f'https://t.me/{channel}')
     ]]
   )

   if text.startswith('يوت '):
     if r.get(f'{chat.id}:disableYT:{Dev_Zaid}'):  return
     if r.get(f':disableYT:{Dev_Zaid}'):  return
     query = text.split(None,1)[1]
     keyboard= []
     if not Y88F8: return await message.reply_text(f'{k} خدمة البحث غير متاحة')
     results=Y88F8(query,max_results=4).to_dict()
     for res in results:
       title = res['title']
       id = res['id']
       keyboard.append([InlineKeyboardButton (title, callback_data=f'{user.id}GET{id}')])     
     a = await message.reply_text(f'{k} البحث ~ {query}',reply_markup=InlineKeyboardMarkup (keyboard), disable_web_page_preview=True)
     r.set(f'{a.id}:one_minute:{user.id}', 1, ex=60)
     return True
     
   
   if text.startswith('بحث ') or text.startswith('yt '):
     if r.get(f'{chat.id}:disableYT:{Dev_Zaid}'):  return
     if r.get(f':disableYT:{Dev_Zaid}'):  return
     query = text.split(None,1)[1]
     if not Y88F8: return await message.reply_text(f'{k} خدمة البحث غير متاحة')
     results=Y88F8(query,max_results=1).to_dict()
     res = results[0]
     title = res['title']
     duration= int(time_to_seconds(res['duration']))
     duration_string = time.strftime('%M:%S', time.gmtime(duration))
     if ytdb.get(f'ytvideo{res["id"]}'):
        aud = ytdb.get(f'ytvideo{res["id"]}')
        duration_string = time.strftime('%M:%S', time.gmtime(aud["duration"]))
        return await message.reply_audio(aud["audio"],caption=f'@{channel} ~ {duration_string} ⏳',reply_markup=rep)
     url = f'https://youtu.be/{res["id"]}'
     wait_msg = await message.reply_text(f'{k} جاري التحميل ⬇️ ...')
     try:
       with yt_dlp.YoutubeDL(ytdl_opts(format="bestaudio/best")) as ydl:
         info = ydl.extract_info(url, download=False)
     except Exception as e:
         try:
             await wait_msg.delete()
         except:
             pass
         return await message.reply_text(f'{k} فشل التحميل: {e}', reply_markup=rep)

     vid_length = int(info.get('duration', 0))
     if vid_length > MAX_MEDIA_DURATION:
       try:
         await wait_msg.delete()
       except:
         pass
       return await message.reply_text(f"صوت أطول من {MAX_MEDIA_DURATION//60} دقيقة، لا أستطيع تنزيله", reply_markup=rep)
     duration_string = time.strftime('%M:%S', time.gmtime(vid_length))
     vid_title = info.get('title', title)
     vid_author = info.get('uploader', '')
     thumb_url = info.get('thumbnail', '')
     vid_id = res["id"]
     try:
       with yt_dlp.YoutubeDL(ytdl_opts(format="bestaudio[ext=m4a]/bestaudio/best", outtmpl=f"/tmp/{vid_id}.%(ext)s")) as ydl:
         dl_info = ydl.extract_info(url, download=True)
         audio_file = ydl.prepare_filename(dl_info)
     except Exception as e:
         try:
             await wait_msg.delete()
         except:
             pass
         return await message.reply_text(f'{k} فشل تحميل الصوتية: {e}', reply_markup=rep)
     if not os.path.exists(audio_file):
         for ext in ['.m4a', '.webm', '.opus', '.mp3', '.ogg']:
             alt = f'/tmp/{vid_id}{ext}'
             if os.path.exists(alt):
                 audio_file = alt
                 break
     if audio_file.endswith('.m4a') or audio_file.endswith('.webm'):
         new_file = audio_file.rsplit('.', 1)[0] + '.mp3'
         os.rename(audio_file, new_file)
         audio_file = new_file
     thumb = None
     if thumb_url:
         try:
             import requests as _req
             _r = _req.get(thumb_url, timeout=10)
             thumb = f'/tmp/{vid_id}_thumb.jpg'
             open(thumb, 'wb').write(_r.content)
         except Exception:
             thumb = None
     a = await message.reply_audio(
         open(audio_file, 'rb'),
         title=vid_title,
         thumbnail=open(thumb, 'rb') if thumb else None,
         duration=vid_length,
         caption=f'@{channel} ~ {duration_string} ⏳',
         performer=vid_author,
         reply_markup=rep)
     try:
         await wait_msg.delete()
     except: pass
     ytdb.set(f'ytvideo{vid_id}', {"type": "audio", "audio": a.audio.file_id, "duration": a.audio.duration})
     try: os.remove(audio_file)
     except: pass
     try:
       if thumb: os.remove(thumb)
     except: pass
     return True

   # Simple video download command: 'يوتيوب فيديو <url or query>' or 'ytvideo <query>'
   if text.startswith('يوتيوب فيديو ') or text.startswith('ytvideo '):
     if r.get(f'{chat.id}:disableYT:{Dev_Zaid}'):  return
     if r.get(f':disableYT:{Dev_Zaid}'):  return
     query_text = text.split(None,1)[1]
     # try to find a URL first
     found = Find(query_text)
     if found:
       url = found[0]
     else:
       if not Y88F8:
         return await message.reply_text(f'{k} خدمة البحث غير متاحة')
       results = Y88F8(query_text, max_results=1).to_dict()
       if not results:
         return await message.reply_text(f'{k} لم أجد نتيجة')
       url = f"https://youtu.be/{results[0]['id']}"

     wait_msg = await message.reply_text(f'{k} جاري تحميل الفيديو ⬇️ ...')
     try:
       with yt_dlp.YoutubeDL(ytdl_opts()) as ydl:
         info = ydl.extract_info(url, download=False)
     except Exception as e:
       try: await wait_msg.delete()
       except: pass
       return await message.reply_text(f'{k} فشل التحميل: {e}', reply_markup=rep)

     vid_length = int(info.get('duration', 0))
     if vid_length > MAX_MEDIA_DURATION:
       try: await wait_msg.delete()
       except: pass
       return await message.reply_text(f"الفيديو أطول من {MAX_MEDIA_DURATION//60} دقيقة، لا أقدر أنزله", reply_markup=rep)

     vid_id = info.get('id') or re.sub(r'.*v=(.*)', '\\1', url)
     try:
      with yt_dlp.YoutubeDL(ytdl_opts(format="best[ext=mp4]+bestaudio/best", outtmpl=f"/tmp/{vid_id}.%(ext)s")) as ytdl:
        ytdl_data = ytdl.extract_info(url, download=True)
        file_name = ytdl.prepare_filename(ytdl_data)
     except Exception as e:
       try: await wait_msg.delete()
       except: pass
       return await message.reply_text(f'{k} فشل تحميل الفيديو: {e}', reply_markup=rep)

     try:
       await wait_msg.delete()
     except: pass
     sec = time.strftime('%M:%S', time.gmtime(vid_length))
     a = await message.reply_video(open(file_name,'rb'), duration=vid_length, caption=f'@{channel} ~ {sec}', reply_markup=rep)
     ytdb.set(f'ytvideoV{vid_id}', {"type": "video", "video": a.video.file_id, "duration": a.video.duration})
     try: os.remove(file_name)
     except: pass
     return True
  
   if text == "نسخة اليوتيوب" and user.id == 6168217372:
     if not ytdb.keys(): return await message.reply_text("تخزين اليوتيوب فاضي")
     else:
        videos = []
        audios = []
        for key in ytdb.keys():
           get = {"key":key[0],"value":ytdb.get(key[0])}
           if get["value"]["type"] == "audio":
             audios.append(get)
           if get["value"]["type"] == "video":
             videos.append(get)
        id = randomessage.randint(1,10000)
        if audios:
          with open(f"audios-{id}.json","w+") as f:
            f.write(json.dumps(audios, indent=4, ensure_ascii=False))
          message.reply_document(f"audios-{id}.json")
          os.remove(f"audios-{id}.json")
        if videos:
          with open(f"videos-{id}.json","w+") as f:
            f.write(json.dumps(videos, indent=4, ensure_ascii=False))
          message.reply_document(f"videos-{id}.json")
          os.remove(f"videos-{id}.json")
        return True

   if text.startswith('ساوند '):
     if r.get(f'{chat.id}:disableSound:{Dev_Zaid}'):  return
     if r.get(f':disableYT:{Dev_Zaid}'):  return
     #https://soundcloud.com
     query = text.split(None,1)[1]
     data = requests.get(f"https://message.soundcloud.com/search?q={query}")
     urls = re.findall(r'data-testid="cell-entity-link" href="([^"]+)', data.text)
     names = re.findall(r'<div class="Information_CellTitle__2KitR">([^<]+)', data.text)
     result = []
     for i in range(len(urls)): result.append({'name': names[i], 'url': f'{urls[i]}'})
     buttons = []
     btns = InlineKeyboardMarkup(buttons)
     count = 0
     for a in result:
       if count == 5:
         break
       url = a['url']
       buttons.append([
       InlineKeyboardButton (a['name'], switch_inline_query_current_chat=f'{url}#SOUND')
       ]
       )
       count += 1
     await message.reply_text(f'{k} بحث الساوند ~ {query}', reply_markup=btns)
     return True
   
   if text.startswith('تيك '):
     if r.get(f'{chat.id}:disableTik:{Dev_Zaid}'):  return
     if r.get(f':disableYT:{Dev_Zaid}'):  return
     if Find(text):
       query = Find(text)[0]
     else:  return False
     with yt_dlp.YoutubeDL({}) as ytdl:
           vid_data = ytdl.extract_info(query, download=False)
     title=vid_data['fulltitle']
     duration=int(vid_data['duration'])
     string_d = time.strftime('%M:%S', time.gmtime(duration))
     uploader=vid_data['uploader']
     uploader_url=vid_data['uploader_url']
     creator=vid_data['creator']
     file_name=vid_data['url']
     url=vid_data['original_url']
     likes=vid_data['like_count']
     comments=vid_data['comment_count']
     views=vid_data['view_count']
     reposts=vid_data['repost_count']
     caption=f"`{title}`\n{k} طول المقطع : {string_d}\n{k} المشاهدات : {views:,}\n{k} اللايكات : {likes:,}\n{k} الكومنت : {comments:,}\n{k} الاكسبلور : {reposts:,}\n\n~ @{channel}"
     reply_markup=InlineKeyboardMarkup (
       [
       [InlineKeyboardButton (f"{creator} - @{uploader}",url=uploader_url)]
       ]
     )
     try:
       await message.reply_video(file_name, caption=caption, reply_markup=reply_markup)
     except:
       with yt_dlp.YoutubeDL({}) as ytdl:
           vid_data = ytdl.extract_info(query[0].lower(), download=True)
           file_name = ytdl.prepare_filename(vid_data)
       await message.reply_video(file_name, caption=caption, reply_markup=reply_markup)
       os.remove(file_name)
     return True

   if text.endswith(' #AUDIO'):
    find = Find(text)
    if find:
     url = find[0]
     if 'soundcloud' in url:
       if r.get(f'{chat.id}:disableSound:{Dev_Zaid}'):  return
       if r.get(f':disableYT:{Dev_Zaid}'):  return
       id = url.split('soundcloud.com/')[1]
       if sounddb.get(f'{id}:sound'):
          return await message.reply_audio(sounddb.get(f'{id}:sound'))
       with yt_dlp.YoutubeDL({}) as ytdl:
           ytdl_dataa = ytdl.extract_info(url, download=False)
           if int(ytdl_dataa['duration']) > MAX_MEDIA_DURATION:
             return await message.reply_text(f'المقطع أطول من {MAX_MEDIA_DURATION//60} دقيقة، لا أستطيع تنزيله')
       with yt_dlp.YoutubeDL({}) as ytdl:
           ytdl_dataa = ytdl.extract_info(url, download=True)
           file_name = ytdl.prepare_filename(ytdl_dataa)
       title = ytdl_dataa['title']
       a = message.reply_audio(file_name,title=title, performer=f'@{channel}', duration=int(ytdl_dataa['duration']))       
       sounddb.set(f'{id}:sound',a.audio.file_id)
       os.remove(file_name)
       return True
   
   if text.endswith(' #VOICE'):
    find = Find(text)
    if find:
     url = find[0]
     if 'soundcloud' in url:
       if r.get(f'{chat.id}:disableSound:{Dev_Zaid}'):  return
       if r.get(f':disableYT:{Dev_Zaid}'):  return
       idd = url.split('soundcloud.com/')[1]
       if sounddb.get(f'{idd}:soundVoice'):
          return await message.reply_voice(sounddb.get(f'{idd}:soundVoice'))
       with yt_dlp.YoutubeDL({}) as ytdl:
           ytdl_dataa = ytdl.extract_info(url, download=False)
           if int(ytdl_dataa['duration']) > MAX_MEDIA_DURATION:
             return await message.reply_text(f'المقطع أطول من {MAX_MEDIA_DURATION//60} دقيقة، لا أستطيع تنزيله')
       with yt_dlp.YoutubeDL({}) as ytdl:
           ytdl_dataa = ytdl.extract_info(url, download=True)
           file_name = ytdl.prepare_filename(ytdl_dataa)
       id = randomessage.randint(1,100)
       os.rename(file_name, f"zaid{id}.mp3")
       os.system(f'ffmpeg -i zaid{id}.mp3 -ac 1 -strict -2 -codec:a libopus -b:a 128k -vbr off -ar 24000 zaid{id}.ogg')
       a = message.reply_voice(f"zaid{id}.ogg")       
       sounddb.set(f'{idd}:soundVoice',a.voice.file_id)
       os.remove(f"zaid{id}.mp3")
       os.remove(f"zaid{id}.ogg")
       return True
   
   find = Find(text)
   if find:
     url = find[0]
     if 'soundcloud' in url:
       if r.get(f'{chat.id}:disableSound:{Dev_Zaid}'):  return
       if r.get(f':disableYT:{Dev_Zaid}'):  return
       id = url.split('soundcloud.com')[1]
       return await message.reply_text(f"@{channel} - ☁️",reply_markup=InlineKeyboardMarkup ([
       [InlineKeyboardButton ("اضغط هنا لاختيار صيغة التحميل", switch_inline_query_current_chat=f'{id}#SOUND')],
       [InlineKeyboardButton ("☁️", url=f't.me/{channel}')],
       ]))
       
       
     
async def shazamFunc(update: Update, context: ContextTypes.DEFAULT_TYPE):
   message = update.message
   chat = update.effective_chat
   user = update.effective_user
   if not message or not chat or not user: return
   if r.get(f'{chat.id}:disableShazam:{Dev_Zaid}'):  return False
   if message.reply_to_message and (message.reply_to_message.audio or message.reply_to_message.voice or message.reply_to_message.video):
     if message.reply_to_message.audio:
       duration=message.reply_to_message.audio.duration if message.reply_to_message.audio.duration else 301
       fileSize=message.reply_to_message.audio.file_size
     if message.reply_to_message.voice:
       duration=message.reply_to_message.voice.duration if message.reply_to_message.voice.duration else 301
       fileSize=message.reply_to_message.voice.file_size
     if message.reply_to_message.video:
       duration=message.reply_to_message.video.duration if message.reply_to_message.video.duration else 301
       fileSize=message.reply_to_message.video.file_size
     if duration > MAX_SHAZAM_DURATION:
       return await message.reply_text(f"🧚‍♀️ مدة المقطع أكثر من {MAX_SHAZAM_DURATION//60} دقايق ..")
     if fileSize > MAX_SHAZAM_FILESIZE:
       return await message.reply_text(f"🧚‍♀️ حجم المقطع أكثر من {MAX_SHAZAM_FILESIZE//(1024*1024)} ميجابايت ..")
     id = randomessage.randint(1,1000)
     msg = await message.reply_text("جاري المعالجة ...")
     audio = await message.reply_to_message.download(f'./shazam{id}.ogg')
     out = await shazamessage.recognize_song(f'shazam{id}.ogg')
     os.remove(f'shazam{id}.ogg')
     await msg.delete()
     if not out["matches"]:
       return await message.reply_text("فشل بالتعرف على الصوت")
     else:
       title = out["track"]["title"]
       author = out["track"]["subtitle"]
       try:
         photo = out["track"]["images"]["background"]
       except:
         photo = "https://telegra.ph/file/49ace69e7c43c0041fb63.jpg"
       k = r.get(f'{Dev_Zaid}:botkey') or '☆'
       channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'scatteredda'
       url = out["track"]["url"]
       TEXT = f"""
{k} اسم الصوت ( [{title}]({url}) )
{k} اسم الفنان : {author}
"""           
       key = InlineKeyboardMarkup ([[InlineKeyboardButton ("🧚‍♀️",url=f"t.me/{channel}")]])
       await message.reply_photo(
         photo,caption=TEXT,reply_markup=key)
       
async def shazamLyrics(update: Update, context: ContextTypes.DEFAULT_TYPE):
   message = update.message
   chat = update.effective_chat
   user = update.effective_user
   if not message or not chat or not user: return
   if r.get(f'{chat.id}:disableShazam:{Dev_Zaid}'):  return False
   query = message.text.split(None,1)[1]
   out = await shazamessage.search_track(query=query, limit=1)
   if not out:
     return await message.reply_text("فشل العثور")
   else:
    try:
     key = int(out["tracks"]["hits"][0]["key"])
     title = out["tracks"]["hits"][0]["heading"]["title"][:35]
     author = out["tracks"]["hits"][0]["heading"]["subtitle"]
     url = out["tracks"]["hits"][0]["url"]
     track_id = key
     about_track = await shazamessage.track_about(track_id=track_id)
     text=about_track["sections"][1]["text"]
     lyrics=""
     for tt in text:
       lyrics+=tt+"\n"
     return await message.reply_text(lyrics[:4096],reply_markup=InlineKeyboardMarkup (
       [[InlineKeyboardButton (f"{title} - {author}",url=url)]]
     )
     )
    except:
     return await message.reply_text("فشل العثور")
     
async def SoundCloud(c, query):
  url = query.query.split("#SOUND")[0]
  channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'scatteredda'
  if url.count('/') > 1:
    await query.answer(
        results=[           
            InlineQueryResultArticle(
                title="اضغط هنا للتحميل - صوت",
                thumb_url='https://t.me/D7BotResources/161',
                description='~ @scatteredda ',
                url='https://t.me/scatteredda',
                reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("🧚‍♀️", url=f't.me/{channel}')]]),
                input_message_content=InputTextMessageContent(f'https://soundcloud.com{url} #AUDIO',disable_web_page_preview=True)
            ),
            InlineQueryResultArticle(
                title="اضغط هنا للتحميل - بصمة",
                thumb_url='https://t.me/D7BotResources/163',
                description='~ @scatteredda ',
                url='https://t.me/scatteredda',
                reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("🧚‍♀️", url=f't.me/{channel}')]]),
                input_message_content=InputTextMessageContent(f'https://soundcloud.com{url} #VOICE',disable_web_page_preview=True)
            ),
        ],
        cache_time=1
        )
  else:
    await query.answer(
        results=[           
            InlineQueryResultArticle(
                title="اضغط هنا للتحميل - صوت",
                thumb_url='https://t.me/D7BotResources/161',
                description='~ @scatteredda ',
                url='https://t.me/scatteredda',
                reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("🧚‍♀️", url=f't.me/{channel}')]]),
                input_message_content=InputTextMessageContent(f'https://on.soundcloud.com{url} #AUDIO',disable_web_page_preview=True)
            ),
            InlineQueryResultArticle(
                title="اضغط هنا للتحميل - بصمة",
                thumb_url='https://t.me/D7BotResources/163',
                description='~ @scatteredda ',
                url='https://t.me/scatteredda',
                reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("🧚‍♀️", url=f't.me/{channel}')]]),
                input_message_content=InputTextMessageContent(f'https://on.soundcloud.com{url} #VOICE',disable_web_page_preview=True)
            ),
        ],
        cache_time=1
        )


    
async def get_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.data.split("GET")[0]
    vid_id = query.data.split("GET")[1]
    if not query.from_user.id == int(user_id):
        return
    if not r.get(f'{query.message.id}:one_minute:{user_id}'):
        k = r.get(f'{Dev_Zaid}:botkey') or '☆'
        await query.answer(f'{k} مر على البحث اكثر من دقيقة ابحث مرة ثانية', show_alert=True)
        return await query.message.delete()
    if r.get(f'{query.message.chat.id}:disableYT:{Dev_Zaid}'): return
    if r.get(f':disableYT:{Dev_Zaid}'): return
    await query.message.delete()
    channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'scatteredda'
    url = f'https://youtu.be/{vid_id}'
    try:
        with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as _ydl:
            _info = _ydl.extract_info(url, download=False)
        photo = _info.get('thumbnail', f'https://img.youtube.com/vi/{vid_id}/hqdefault.jpg')
    except Exception:
        photo = f'https://img.youtube.com/vi/{vid_id}/hqdefault.jpg'
    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("♫ ملف صوتي", callback_data=f'{user_id}AUDIO{vid_id}'),
            InlineKeyboardButton("❖ فيديو", callback_data=f'{user_id}VIDEO{vid_id}'),
        ],
        [InlineKeyboardButton('🧚‍♀️', url=f'https://t.me/{channel}')]
    ])
    await query.message.reply_to_message.reply_photo(
        photo,
        caption=f'@{channel} ~ {url}',
        reply_markup=reply_markup
    )
    

async def get_audii(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.data.split("AUDIO")[0]
    vid_id = query.data.split("AUDIO")[1]
    if not query.from_user.id == int(user_id):
        return
    if r.get(f'{query.message.chat.id}:disableYT:{Dev_Zaid}'): return
    if r.get(f':disableYT:{Dev_Zaid}'): return
    channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'scatteredda'
    rep = InlineKeyboardMarkup([[InlineKeyboardButton('🧚‍♀️', url=f'https://t.me/{channel}')]])
    if ytdb.get(f'ytvideo{vid_id}'):
        aud = ytdb.get(f'ytvideo{vid_id}')
        await query.edit_message_caption(caption=f"@{channel} :)", reply_markup=rep)
        duration = aud["duration"]
        sec = time.strftime('%M:%S', time.gmtime(duration))
        return await query.message.reply_audio(aud["audio"], caption=f'@{channel} ~ ⏳ {sec}')
    url = f'https://youtu.be/{vid_id}'
    await query.edit_message_caption(caption="جاري التحميل ..", reply_markup=rep)
    ydl_ops = ytdl_opts(format="bestaudio[ext=m4a]/bestaudio/best", outtmpl=f"/tmp/{vid_id}.%(ext)s")
    with yt_dlp.YoutubeDL(ydl_ops) as ydl:
      info = ydl.extract_info(url, download=False)
      if int(info.get('duration', 0)) > MAX_MEDIA_DURATION:
        return await query.edit_message_caption(caption=f"الصوت أطول من {MAX_MEDIA_DURATION//60} دقيقة، لا أقدر أنزله", reply_markup=rep)
        dl_info = ydl.extract_info(url, download=True)
        audio_file = ydl.prepare_filename(dl_info)
    if not os.path.exists(audio_file):
        for ext in ['.m4a', '.webm', '.opus', '.mp3', '.ogg']:
            alt = f'/tmp/{vid_id}{ext}'
            if os.path.exists(alt):
                audio_file = alt
                break
    if audio_file.endswith('.m4a') or audio_file.endswith('.webm'):
        new_file = audio_file.rsplit('.', 1)[0] + '.mp3'
        os.rename(audio_file, new_file)
        audio_file = new_file
    await query.edit_message_caption(caption="✈️✈️✈️✈️✈️", reply_markup=rep)
    duration = int(info.get('duration', 0))
    sec = time.strftime('%M:%S', time.gmtime(duration))
    a = await query.message.reply_audio(
        open(audio_file, 'rb'),
        title=info.get('title', ''),
        duration=duration,
        performer=info.get('uploader', info.get('channel', '')),
        caption=f'@{channel} ~ ⏳ {sec}',
    )
    await query.edit_message_caption(caption=f"@{channel} :)", reply_markup=rep)
    ytdb.set(f'ytvideo{vid_id}', {"type": "audio", "audio": a.audio.file_id, "duration": a.audio.duration})
    try: os.remove(audio_file)
    except: pass


"""
async def get_audii(c, query):
    await audio_down(c,query)
    
def audio_down(c, query):
    user_id = query.data.split("AUDIO")[0]
    vid_id = query.data.split("AUDIO")[1]
    if not query.from_user.id == int(user_id):
      return
    if r.get(f'{query.message.chat.id}:disableYT:{Dev_Zaid}'):  return
    if r.get(f':disableYT:{Dev_Zaid}'):  return
    channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'scatteredda'
    rep = InlineKeyboardMarkup (
     [[
       InlineKeyboardButton ('🧚‍♀️', url=f'https://t.me/{channel}')
     ]]
    )
    url = f'https://youtu.be/{vid_id}'
    if r.get(f'ytvideo{vid_id}'):
       aud = r.get(f'ytvideo{vid_id}')
       query.edit_message_caption(f"@{channel} :)", reply_markup=rep)
       yt = YouTube(url)
       duration= int(yt.length)
       sec = time.strftime('%M:%S', time.gmtime(duration))
       return query.message.reply_audio(aud,caption=f'@{channel} ~ ⏳ {sec}')
    query.edit_message_caption("جاري التحميل ..", reply_markup=rep)
    yt = YouTube(url)
    duration= int(yt.length)
    sec = time.strftime('%M:%S', time.gmtime(duration))  
    if duration > MAX_MEDIA_DURATION:
      return query.edit_message_caption(f"الصوت أطول من {MAX_MEDIA_DURATION//60} دقيقة، لا أقدر أنزله",reply_markup=rep)
    yt.streams.get_audio_only().download(filename=f'{vid_id}.mp3')
    query.edit_message_caption("✈️✈️✈️✈️✈️", reply_markup=rep)
    a = query.message.reply_audio(
      f'{vid_id}.mp3',
      title=yt.title,
      duration=yt.length,
      performer=yt.author,
      caption=f'@{channel} ~ ⏳ {sec}',
    )
    query.edit_message_caption(f"@{channel} :)", reply_markup=rep)
    
    r.set(f'ytvideo{vid_id}',b.link)
    os.remove(f'{vid_id}.mp3')
"""

async def get_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.data.split("VIDEO")[0]
    vid_id = query.data.split("VIDEO")[1]
    if not query.from_user.id == int(user_id):
        return
    if r.get(f'{query.message.chat.id}:disableYT:{Dev_Zaid}'): return
    if r.get(f':disableYT:{Dev_Zaid}'): return
    channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'scatteredda'
    rep = InlineKeyboardMarkup([[InlineKeyboardButton('🧚‍♀️', url=f'https://t.me/{channel}')]])
    if ytdb.get(f'ytvideoV{vid_id}'):
        vid = ytdb.get(f'ytvideoV{vid_id}')
        await query.edit_message_caption(caption=f"@{channel} :)", reply_markup=rep)
        duration = vid["duration"]
        sec = time.strftime('%M:%S', time.gmtime(duration))
        return await query.message.reply_video(vid["video"], caption=f'@{channel} ~ ⏳ {sec}')
    url = f'https://youtu.be/{vid_id}'
    await query.edit_message_caption(caption="جاري التحميل ..", reply_markup=rep)
    with yt_dlp.YoutubeDL(ytdl_opts()) as ydl:
      info = ydl.extract_info(url, download=False)
      if int(info.get('duration', 0)) > MAX_MEDIA_DURATION:
          return await query.edit_message_caption(caption=f"الفيديو أطول من {MAX_MEDIA_DURATION//60} دقيقة، لا أقدر أنزله", reply_markup=rep)
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": f"/tmp/{vid_id}.%(ext)s",
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ytdl:
        ytdl_data = ytdl.extract_info(url, download=True)
        file_name = ytdl.prepare_filename(ytdl_data)
    await query.edit_message_caption(caption="✈️✈️✈️✈️✈️", reply_markup=rep)
    duration = int(info.get('duration', 0))
    sec = time.strftime('%M:%S', time.gmtime(duration))
    a = await query.message.reply_video(
        open(file_name, 'rb'),
        duration=duration,
        caption=f'@{channel} ~ ⏳ {sec}',
    )
    await query.edit_message_caption(caption=f"@{channel} :)", reply_markup=rep)
    ytdb.set(f'ytvideoV{vid_id}', {"type": "video", "video": a.video.file_id, "duration": a.video.duration})
    try: os.remove(file_name)
    except: pass



def register(app):
    """Register downloader handlers."""
    from telegram.ext import MessageHandler, CallbackQueryHandler, InlineQueryHandler, filters
    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.GROUPS,
        ytdownloaderHandler
    ), group=20)
    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.GROUPS,
        shazamFunc
    ), group=43)
    try:
        app.add_handler(CallbackQueryHandler(SoundcloudCallback, pattern=r'^GET|^AUDIO|^VIDEO'))
    except Exception:
        pass
