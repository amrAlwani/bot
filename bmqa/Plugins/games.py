'''
A
[ = This plugin is a part from R3D Source code = ]
{"Developer":"https://t.me/bo_poq"}

'''
import random,re, time, akinator, string
 



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
from helpers.games import *
from helpers.Ranks import isLockCommand

class _DummyClient:
    @staticmethod
    def on_callback_query(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

Client = _DummyClient()
users_demon = {}
def is_what_percent_of(num_a, num_b):
    return (num_a / num_b) * 100

def get_top(users):
   users = [tuple(i.items()) for i in users]
   top = sorted(users, key=lambda i: i[-1][-1], reverse=True)
   top = [dict(i) for i in top]
   return top

async def gamesHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    k = r.get(f'{Dev_Zaid}:botkey') or '☆'
    channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'scatteredda'
    await gamesFunc(update, context, k, channel)

async def diceFunc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    chat = update.effective_chat
    user = update.effective_user
    if not message or not chat or not user: return
    if r.get(f'{chat.id}:disableGames:{Dev_Zaid}'):  return False
    if message.dice.emoji == "🎲":
      k = r.get(f'{Dev_Zaid}:botkey') or '☆'
      if message.dice.value == 6:
        await asyncio.sleep(3)
        ra = 100
        if r.get(f'{user.id}:Floos'):
           get = int(r.get(f'{user.id}:Floos'))
           r.set(f'{user.id}:Floos',get+ra)
           floos = int(r.get(f'{user.id}:Floos'))
        else:
           floos = ra
           r.set(f'{user.id}:Floos',ra)
        return await message.reply_text(f'''
صح عليك فزت **[بالنرد]({'#'})** ⁪⁬⁪⁪⁬⁮⁪⁬⁪⁬⁮✔
💸فلوسك: `{floos}` ريال
☆
''', disable_web_page_preview=True)
      else:
        await asyncio.sleep(3)
        return await message.reply_text(f"{k} للأسف خسرت بالنرد")
   

async def gamesFunc(update, context, k,channel):
   message = update.message
   chat = update.effective_chat
   user = update.effective_user
   if not message or not chat or not user:
       return
   if not r.get(f'{chat.id}:enable:{Dev_Zaid}'):
       return
   if r.get(f'{user.id}:gbangames:{Dev_Zaid}'):  return 
   if r.get(f'{user.id}:mute:{chat.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:addCustom:{user.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}addCustomG:{user.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:delCustom:{user.id}{Dev_Zaid}') or r.get(f'{chat.id}:delCustomG:{user.id}{Dev_Zaid}'):  return 
   if r.get(f'{chat.id}:mute:{Dev_Zaid}') and not admin_pls(user.id,chat.id):  return
   if r.get(f'{user.id}:mute:{Dev_Zaid}'):  return 
   text = message.text
   name = r.get(f'{Dev_Zaid}:BotName') if r.get(f'{Dev_Zaid}:BotName') else 'فوق'
   if text.startswith(f'{name} '):
      text = text.replace(f'{name} ','')
   if r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}'):
     text = r.get(f'{chat.id}:Custom:{chat.id}{Dev_Zaid}&text={text}')
   if r.get(f'Custom:{Dev_Zaid}&text={text}'):
     text = r.get(f'Custom:{Dev_Zaid}&text={text}')
   if r.get(f'{chat.id}:disableGames:{Dev_Zaid}'):  return
   
   if r.get(f'{user.id}:toTrans:{chat.id}{Dev_Zaid}'):
      if not re.findall('[0-9]+', text): 
        r.delete(f'{user.id}:toTrans:{chat.id}{Dev_Zaid}')
        return await message.reply_text(f'{k} لازم يكون ارقام')
      acc_id = int(re.findall('[0-9]+', text)[0])
      acc_id_from = int(r.get(f'{user.id}:bankID'))
      if acc_id == acc_id_from:
        r.delete(f'{user.id}:toTrans:{chat.id}{Dev_Zaid}')
        return await message.reply_text(f'{k} مافيك تحول لنفسك')
      floos_to_trans = int(r.get(f'{user.id}:toTrans:{chat.id}{Dev_Zaid}'))
      r.delete(f'{user.id}:toTrans:{chat.id}{Dev_Zaid}')
      if not r.sismember('BankList', user.id):
        return await message.reply_text(f'{k} ماعندك حساب بنكي ارسل ↢ ( `انشاء حساب بنكي` )')
      if not r.get(f'{user.id}:Floos'):
        floos = 0
      else:
        floos = int(r.get(f'{user.id}:Floos'))
      if floos_to_trans > floos:
        return await message.reply_text(f'{k} فلوسك ماتكفي')
      else:
        if not r.get(f'{acc_id}:getAccBank'):
          return await message.reply_text(f'{k} مافي حساب بنكي كذا')
        else:
          id_to = int(r.get(f'{acc_id}:getAccBank'))
          if not r.sismember('BankList', id_to):
            return await message.reply_text(f'{k} ماعنده حساب بأي بنك')
          if r.get(f'{id_to}:bankName'):
            name_to = r.get(f'{id_to}:bankName')[:10]
          else:
            name_to = str(r.get(f'{id_to}:bankName') or id_to)
            r.set(f'{id_to}:bankName',name_to)
          if floos_to_trans == floos:
            r.delete(f'{user.id}:Floos')
          else:
            r.set(f'{user.id}:Floos',floos-floos_to_trans)
          bank_to = r.get(f'{id_to}:bankType')
          bank_from = r.get(f'{user.id}:bankType')
          name_from = r.get(f'{user.id}:bankName')[:10] or user.first_name[:10]
          mention_from = f'[{name_from}](tg://user?id={user.id})'
          mention_to = f'[{name_to}](tg://user?id={id_to})'
          if not r.get(f'{id_to}:Floos'):
            floos_to = 0
          else:
            floos_to = int(r.get(f'{id_to}:Floos'))
          txt = 'حوالة صادرة\n\nمن: {}\nحساب رقم: {}\nبنك: {}\nالى: {}\nحساب رقم: {}\nبنك: {}'.format(mention_from,acc_id_from,bank_from,mention_to,acc_id,bank_to)
          if bank_from != bank_to:
             floos_to_tran = int(floos_to_trans-floos_to_trans/10)
             txt += '\nخصمت 10% ضريبة بنك الى بنك'
             txt += f'\nالمبلغ: {floos_to_tran} ريال 💸'
          else:
             floos_to_tran = floos_to_trans
             txt += f'\nالمبلغ: {floos_to_tran} ريال 💸'
          r.set(f'{id_to}:Floos',floos_to+floos_to_tran)
          return await message.reply_text(txt, disable_web_page_preview=True)

   if r.get(f'{user.id}:createBank:{chat.id}'):
     r.delete(f'{user.id}:createBank:{chat.id}')
     if r.get(f'{user.id}:bankID'):
       id = int(r.get(f'{user.id}:bankID'))
       floos_to_add = 0
     else:
       id = '4'
       floos_to_add = 2000
       for a in range(15):
         id += str(random.randint(1,9))
     if not r.get(f'{user.id}:Floos'):
       floos = 0
     else:
       floos = int(r.get(f'{user.id}:Floos'))
     '''
     if not text in ['الاهلي','راجحي', 'الانماء','عبد الفتاح السيسي']:
       return await message.reply_text(f'{k} مافيه بنك بهالاسم')
     '''
     if not text in ['الاهلي','راجحي', 'الانماء']:
       return await message.reply_text(f'{k} مافيه بنك بهالاسم')
     card = random.choice(['الاهلي كارد','الراجحي كارد','الإنماء كارد','مدى كارد'])
     if text == 'الاهلي':
        r.set(f'{user.id}:bankType', 'الاهلي')
        r.set(f'{user.id}:bankID', int(id))
        r.set(f'{user.id}:bankCard',card)
     if text == 'راجحي':
        r.set(f'{user.id}:bankType', 'راجحي')
        r.set(f'{user.id}:bankID', int(id))
        r.set(f'{user.id}:bankCard',card)
     if text == 'الانماء':
        r.set(f'{user.id}:bankType', 'الانماء')
        r.set(f'{user.id}:bankID', int(id))
        r.set(f'{user.id}:bankCard',card)
     '''
     if text == 'عبد الفتاح السيسي':
        r.set(f'{user.id}:bankType', 'بلحة الدولي')
        r.set(f'{user.id}:bankID', int(id))
        r.set(f'{user.id}:bankCard','بطاقة تموين')
        card = 'بطاقة تموين'
        r.sadd('BankList', user.id)
        r.set(f'{id}:getAccBank', user.id)
        fff = floos + floos_to_add
        r.set(f'{user.id}:Floos',fff)
        r.set(f'{user.id}:bankName',user.first_name)
        await message.reply_text(f'• وسوينا لك حساب في بنك {text}\n\n{k} رقم حسابك ↢ ( `{id}` )\n{k} نوع البطاقة ↢ ( {card} )\n{k} فلوسك ↢ ( {fff} ريال 💸 )\n\n{k} هتدفع!! هتشوف الي مشفتهوش، دا لو هتدفع!، انما ببلاش دا انا معرفش حاجة اسمها ببلاش')
        if r.get(f'DevGroup:{Dev_Zaid}'):
          return pass  # send_message removed
        else:
          return 
     '''
     r.sadd('BankList', user.id)
     r.set(f'{id}:getAccBank', user.id)
     fff = floos + floos_to_add
     r.set(f'{user.id}:Floos',fff)
     r.set(f'{user.id}:bankName',user.first_name)
     await message.reply_text(f'• وسوينا لك حساب في بنك {text}\n\n{k} رقم حسابك ↢ ( `{id}` )\n{k} نوع البطاقة ↢ ( {card} )\n{k} فلوسك ↢ ( {fff} ريال 💸 )')
     if r.get(f'DevGroup:{Dev_Zaid}'):
         pass  # send_message removed
   
   if text == 'توب' or text == 'التوب':
     await message.reply_text(f'{k} اهلين فيك في قوائم التوب\nللاستفسار - @{channel}',
     reply_markup=InlineKeyboardMarkup (
       [
       [
         InlineKeyboardButton ('توب الفلوس 💸', callback_data=f'topfloos:{user.id}'),
         InlineKeyboardButton ('توب الحرامية 💰', callback_data=f'topzrf:{user.id}'),
       ],
       [
        InlineKeyboardButton ('🧚‍♀️',url=f't.me/{channel}')
       ]
       ]
     ))
   
   if text == 'توب الفلوس':
     if not r.smembers('BankList'):
       return await message.reply_text(f'{k} مافيه حسابات بالبنك')
     else:
       rep = InlineKeyboardMarkup (
         [[InlineKeyboardButton ('🧚‍♀️', url=f't.me/{channel}')]]
       )
       if r.get('BankTop'):
          text = r.get('BankTop')
          if not r.get(f'{user.id}:Floos'):
            floos = 0
          else:
            floos = int(r.get(f'{user.id}:Floos'))
          get = r.ttl('BankTop')
          wait = time.strftime('%M:%S', time.gmtime(get))
          text += '\n━━━━━━━━━'
          text += f'\n# You ) {floos:,} 💸 l {user.first_name}'
          text += f'\n\n[قوانين التُوب](https://t.me/{botUsername}?start=rules)'
          text += f'\n\nالقائمة تتحدث بعد {wait} دقيقة'
          return await message.reply_text(text, disable_web_page_preview=True,reply_markup=rep)
       else:
          users = []
          ccc = 0
          for user in r.smembers('BankList'):
            ccc += 1
            id = int(user)
            if r.get(f'{id}:bankName'):
              name = r.get(f'{id}:bankName')[:10]
            else:
              try:
                name = str(id)
                r.set(f'{id}:bankName',name)
              except:
                name = 'INVALID_NAME'
                r.set(f'{id}:bankName',name)
            if not r.get(f'{id}:Floos'):
              floos = 0
            else:
              floos = int(r.get(f'{id}:Floos'))
            users.append({'name':name, 'money':floos})
          top = get_top(users)
          text = 'توب 20 اغنى اشخاص:\n\n'
          count = 0
          for user in top:
            count += 1
            if count == 21:
              break 
            emoji = get_emoji_bank(count)
            floos = user['money']
            name = user ['name']
            text += f'**{emoji}{floos:,}** 💸 l {name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}\n'
          r.set('BankTop',text,ex=300)
          if not r.get(f'{user.id}:Floos'):
            floos_from_user = 0
          else:
            floos_from_user = int(r.get(f'{user.id}:Floos'))
          text += '\n━━━━━━━━━'
          text += f'\n# You ) {floos_from_user:,} 💸 l {user.first_name}'
          text += f'\n\n[قوانين التُوب](https://t.me/{botUsername}?start=rules)'
          get = r.ttl('BankTop')
          wait = time.strftime('%M:%S', time.gmtime(get))
          text += f'\n\nالقائمة تتحدث بعد {wait} دقيقة'
          return await message.reply_text(text,disable_web_page_preview=True,reply_markup=rep)
   
   
   if text == 'توب الحراميه' or text == 'توب الحرامية' or text == 'توب الزرف':
     if not r.smembers('BankList'):
       return await message.reply_text(f'{k} مافيه حسابات بالبنك')
     else:
       rep = InlineKeyboardMarkup (
         [[InlineKeyboardButton ('🧚‍♀️', url=f't.me/{channel}')]]
       )
       if r.get('BankTopZRF'):
          text = r.get('BankTopZRF')
          if not r.get(f'{user.id}:Zrf'):
            zrf = 0
          else:
            zrf = int(r.get(f'{user.id}:Zrf'))
          get = r.ttl('BankTopZRF')
          wait = time.strftime('%M:%S', time.gmtime(get))
          text += '\n━━━━━━━━━'
          text += f'\n# You ) {zrf:,} 💰 l {user.first_name}'
          text += f'\n\n[قوانين التُوب](https://t.me/{botUsername}?start=rules)'
          text += f'\n\nالقائمة تتحدث بعد {wait} دقيقة'
          return await message.reply_text(text, disable_web_page_preview=True,reply_markup=rep)
       else:
          users = []
          ccc = 0
          for user in r.smembers('BankList'):
            ccc += 1
            id = int(user)
            if r.get(f'{id}:bankName'):
              name = r.get(f'{id}:bankName')[:10]
            else:
              try:
                name = str(id)
                r.set(f'{id}:bankName',name)
              except:
                name = 'INVALID_NAME'
                r.set(f'{id}:bankName',name)
            if not r.get(f'{id}:Zrf'):
              zrf = 0
            else:
              zrf = int(r.get(f'{id}:Zrf'))
            users.append({'name':name, 'money':zrf})
          top = get_top(users)
          text = 'توب 20 اكثر الحراميه زرفًا:\n\n'
          count = 0
          for user in top:
            count += 1
            if count == 21:
              break 
            emoji = get_emoji_bank(count)
            floos = user['money']
            name = user ['name']
            text += f'**{emoji}{floos:,}** 💰 l⁪⁬⁪⁬⁮⁪⁬⁪⁬⁮{name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}\n'
          r.set('BankTopZRF',text,ex=300)
          if not r.get(f'{user.id}:Zrf'):
            floos_from_user = 0
          else:
            floos_from_user = int(r.get(f'{user.id}:Zrf'))
          text += '\n━━━━━━━━━'
          text += f'\n# You ) {floos_from_user:,} 💰 l {user.first_name}'
          text += f'\n\n[قوانين التُوب](https://t.me/{botUsername}?start=rules)'
          get = r.ttl('BankTopZRF')
          wait = time.strftime('%M:%S', time.gmtime(get))
          text += f'\n\nالقائمة تتحدث بعد {wait} دقيقة'
          await message.reply_text(text,disable_web_page_preview=True,reply_markup=rep)
   
   if text == 'زواجات' or text == 'توب زواجات' or text == 'توب الزواجات':
     if not r.smembers(f'{chat.id}:zwag:{Dev_Zaid}'):
        return await message.reply_text(f'{k} محد متزوج بالقروب')
     else:
        #r.sadd(f'{chat.id}:zwag:{Dev_Zaid}', f'{message.reply_to_message.from_user.id}--{user.id}&&floos={floos}')
        users = []
        ccc = 0
        for marriage in r.smembers(f'{chat.id}:zwag:{Dev_Zaid}'):
           user_id_1 = int(marriage.split('--')[0])
           user_id_2 = int(marriage.split('--')[1].split('&&')[0])
           money = int(marriage.split('&&floos=')[1])
           ccc += 1
           if r.get(f'{user_id_1}:bankName'):
              name_1 = r.get(f'{user_id_1}:bankName')[:10]
           else:
              try:
                name_1 = str(id)[:10]
                r.set(f'{user_id_1}:bankName',name_1)
              except:
                name_1 = 'INVALID_NAME'
                r.set(f'{user_id_1}:bankName',name_1)
           if r.get(f'{user_id_2}:bankName'):
              name_2 = r.get(f'{user_id_2}:bankName')[:10]
           else:
              try:
                name_2 = str(id)[:10]
                r.set(f'{user_id_2}:bankName',name_2)
              except:
                name_2 = 'INVALID_NAME'
                r.set(f'{user_id_2}:bankName',name_2)
           users.append({'name_1':name_1, 'name_2':name_2,'money':money})
        top = get_top(users)
        text = 'توب 20 اغلى زواجات بالقروب:\n\n'
        count = 0
        for user in top:
          count += 1
          if count == 21:
            break 
          emoji = get_emoji_bank(count)
          money = user['money']
          name_1 = user['name_1']
          name_2 = user['name_2']
          text += f'**{emoji}**👫 ⁪⁬⁪⁬⁮⁪⁬⁪⁬⁮{name_1} 💕 {name_2} |\n**💸 {money:,}**\n'
        text += f'\n\n[قوانين التُوب](https://t.me/{botUsername}?start=rules)'
        return await message.reply_text(text, disable_web_page_preview=True)
           
   
   '''
   if text == 'تصفير التوب':
     if devp_pls(user.id,chat.id):
       if not r.get('BankTop'):
         return await message.reply_text('اكتب توب الفلوس وارجع حاول')
       if not r.get('BankTopZRF'):
         return await message.reply_text('اكتب توب الحراميه وارجع حاول')
       else:
         await message.reply_text(f'{k} ابشر صفرت التوب')
         users = []
         ccc = 0
         for user in r.smembers('BankList'):
            ccc += 1
            id = int(user)
            if r.get(f'{id}:bankName'):
              name = r.get(f'{id}:bankName')[:10]
            else:
              try:
                name = str(id)
                r.set(f'{id}:bankName',name)
              except:
                name = 'INVALID_NAME'
                r.set(f'{id}:bankName',name)
            if not r.get(f'{id}:Zrf'):
              zrf = 0
            else:
              zrf = int(r.get(f'{id}:Zrf'))
            users.append({'name':name, 'money':zrf})
         top = get_top(users)
         text = ''
         count = 0
         for user in top:
            count += 1
            if count == 3:
              break 
            emoji = get_emoji_bank(count)
            floos = user['money']
            name = user ['name']
            text += f'{emoji}{floos} 💰 l {name}\n'
         r.set(f'BankTopLastZrf',text)
         users = []
         ccc = 0
         for user in r.smembers('BankList'):
            ccc += 1
            id = int(user)
            if r.get(f'{id}:bankName'):
              name = r.get(f'{id}:bankName')[:10]
            else:
              try:
                name = str(id)
                r.set(f'{id}:bankName',name)
              except:
                name = 'INVALID_NAME'
                r.set(f'{id}:bankName',name)
            if not r.get(f'{id}:Floos'):
              floos = 0
            else:
              floos = int(r.get(f'{id}:Floos'))
         users.append({'name':name, 'money':floos})
         top = get_top(users)
         text = ''
         count = 0
         for user in top:
            count += 1
            if count == 3:
              break 
            emoji = get_emoji_bank(count)
            floos = user['money']
            name = user ['name']
            text += f'**{emoji}{floos}** 💸 l {name}\n'
         r.set(f'BankTopLast',text)
         keys = r.keys('*:Floos')
         for a in keys:
           r.delete(a)
   '''
   
   if text == 'حسابي':
     if not r.sismember('BankList', user.id):
       return await message.reply_text(f'{k} ماعندك حساب بنكي ارسل ↢ ( `انشاء حساب بنكي` )')
     else:
       card = r.get(f'{user.id}:bankCard')
       id = int(r.get(f'{user.id}:bankID'))
       bank = r.get(f'{user.id}:bankType')
       if not r.get(f'{user.id}:Floos'):
         floos = 0
       else:
         floos = int(r.get(f'{user.id}:Floos'))
       if r.get(f'{user.id}:bankName'):
         name = r.get(f'{user.id}:bankName')
       else:
         name = user.first_name
       await message.reply_text(f'''{k} الاسم ↢ ⁪⁬⁪⁬⁮⁪⁬⁪⁬⁮{name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}
{k} الحساب ↢ `{id}`
{k} بنك ↢ ( {bank} )
{k} نوع ↢ ( {card} )
{k} الرصيد ↢ ( {floos} ريال 💸 )
☆''')
   
   if text == 'انشاء حساب بنكي':
     if r.sismember('BankList', user.id):
       bank = r.get(f'{user.id}:bankType')
       acc_id = int(r.get(f'{user.id}:bankID'))
       return await message.reply_text(f'{k} عندك حساب في بنك {bank}\n\n{k} لتفاصيل اكثر اكتب\n{k} `حساب {acc_id}`')
     else:
       r.set(f'{user.id}:createBank:{chat.id}',1,ex=300)
       '''
       return await message.reply_text(f'– عشان تسوي حساب لازم تختار بنك\n\n{k} `الاهلي`\n{k} `راجحي`\n{k} `الانماء`\n{k} `عبد الفتاح السيسي`\n\n- اضغط للنسخ')
       '''
       return await message.reply_text(f'– عشان تسوي حساب لازم تختار بنك\n\n{k} `الاهلي`\n{k} `راجحي`\n{k} `الانماء`\n\n- اضغط للنسخ')
       
   
   if text == 'مسح حسابي':
     if not r.sismember('BankList', user.id):
       return await message.reply_text(f'{k} ماعندك حساب بنكي')
     else:
       r.srem('BankList', user.id)
       await message.reply_text(f'{k} تم حذف حسابك البنكي')
   
   if text.startswith('حساب ') and len(text.split()) == 2 and re.findall('[0-9]+', text):
      acc_id = int(re.findall('[0-9]+', text)[0])
      if r.get(f'{acc_id}:getAccBank'):
         id = int(r.get(f'{acc_id}:getAccBank'))
         if r.get(f'{id}:bankName'):
           name = r.get(f'{id}:bankName')[:10]
         else:
           gett = None
           name = "مستخدم"
           r.set(f'{id}:bankName',name)
         bank = r.get(f'{id}:bankType')
         card = r.get(f'{id}:bankCard')
         if not r.get(f'{id}:Floos'):
           floos = 0
         else:
           floos = int(r.get(f'{id}:Floos'))
         await message.reply_text(f'''
{k} الاسم ↢ ⁪⁬⁪⁬⁮⁪⁬⁪⁬⁮{name.replace("*","").replace("`","").replace("|","").replace("#","").replace("<","").replace(">","").replace("_","")}
{k} الحساب ↢ `{acc_id}`
{k} بنك ↢ ( {bank} )
{k} نوع ↢ ( {card} )
{k} الرصيد ↢ ( `{floos}` ريال 💸 )
☆
''')
   
   if text.startswith('تحويل ') and len(text.split()) == 2 and re.findall('[0-9]+', text):
      floos_to_trans = int(re.findall('[0-9]+', text)[0])
      if not r.get(f'{user.id}:Floos'):
        floos = 0
      else:
        floos = int(r.get(f'{user.id}:Floos'))
      if floos_to_trans < 200:
        return await message.reply_text(f'{k} الحد الادنى المسموح هو 200 ريال')
      else:
        if floos_to_trans > floos:
          return await message.reply_text(f'{k} فلوسك ماتكفي')
        if not r.sismember('BankList', user.id):
          return await message.reply_text(f'{k} ماعندك حساب بنكي ارسل ↢ ( `انشاء حساب بنكي` )')
        else:
          r.set(f'{user.id}:toTrans:{chat.id}{Dev_Zaid}',floos_to_trans, ex=600)
          return await message.reply_text(f'{k} ارسل الحين رقم حساب البنكي الي تبي تحول له')
   
      
      
   if text.startswith('حظ ') and len(text.split()) == 2 and re.findall('[0-9]+', text):
     if not r.sismember('BankList', user.id):
       return await message.reply_text(f'{k} ماعندك حساب بنكي ارسل ↢ ( `انشاء حساب بنكي` )')
     if r.get(f'{user.id}:BankWaitHZ'):
       get = r.ttl(f'{user.id}:BankWaitHZ')
       wait = time.strftime('%M:%S', time.gmtime(get))
       return await message.reply_text(f'{k} مايمديك تلعب لعبة الحظ الحين ! \n{k} تعال بعد {wait} دقيقة')
     else:
       if not r.get(f'{user.id}:Floos'):
         floos = 0
       else:
         floos = int(r.get(f'{user.id}:Floos'))
       floos_to_hz = int(re.findall('[0-9]+', text)[0])
       if floos_to_hz == 0:
         return await message.reply_text(f'{k} مايمدي تلعب بالصفر')
       if floos_to_hz > floos:
         return await message.reply_text(f'{k} فلوسك ماتكفي')
       else:
         r.set(f'{user.id}:BankWaitHZ',1,ex=600)
         hzz = random.choice(['yes','no'])
         if hzz == 'yes':
           fls = floos_to_hz
           floos_com = floos+fls
           r.set(f'{user.id}:Floos', floos+fls)
           return await message.reply_text(f'{k} مبروك فزت بالحظ !\n{k} فلوسك قبل ↢ ( **{floos}** ريال 💸 )\n{k} فلوسك الحين ↢ ( **{floos_com}** ريال 💸 )')
         else:
           fls = floos-floos_to_hz
           if fls == 0:
              r.delete(f'{user.id}:Floos')
           else:
              r.set(f'{user.id}:Floos', fls)
           return await message.reply_text(f'{k} للأسف خسرت بالحظ !\n{k} فلوسك قبل ↢ ( **{floos}** ريال 💸 )\n{k} فلوسك الحين ↢ ( **{fls}** ريال 💸 )')
   
   
   if text == "حظ فلوسي":
     if not r.sismember('BankList', user.id):
       return await message.reply_text(f'{k} ماعندك حساب بنكي ارسل ↢ ( `انشاء حساب بنكي` )')
     if r.get(f'{user.id}:BankWaitHZ'):
       get = r.ttl(f'{user.id}:BankWaitHZ')
       wait = time.strftime('%M:%S', time.gmtime(get))
       return await message.reply_text(f'{k} مايمديك تلعب لعبة الحظ الحين ! \n{k} تعال بعد {wait} دقيقة')
     else:
       if not r.get(f'{user.id}:Floos'):
         floos = 0
       else:
         floos = int(r.get(f'{user.id}:Floos'))
       floos_to_hz = floos
       if floos_to_hz == 0:
         return await message.reply_text(f'{k} مايمدي تلعب بالصفر')
       else:
         r.set(f'{user.id}:BankWaitHZ',1,ex=600)
         hzz = random.choice(['yes','no'])
         if hzz == 'yes':
           fls = floos_to_hz
           floos_com = floos+fls
           r.set(f'{user.id}:Floos', floos+fls)
           return await message.reply_text(f'{k} مبروك فزت بالحظ !\n{k} فلوسك قبل ↢ ( **{floos}** ريال 💸 )\n{k} فلوسك الحين ↢ ( **{floos_com}** ريال 💸 )')
         else:
           fls = floos-floos_to_hz
           if fls == 0:
              r.delete(f'{user.id}:Floos')
           else:
              r.set(f'{user.id}:Floos', fls)
           return await message.reply_text(f'{k} للأسف خسرت بالحظ !\n{k} فلوسك قبل ↢ ( "**{floos}** ريال 💸 )\n{k} فلوسك الحين ↢ ( **{fls}** ريال 💸 )')

   if text == 'عجله' or text == 'عجلة':
     if not r.sismember('BankList', user.id):
       return await message.reply_text(f'{k} ماعندك حساب بنكي ارسل ↢ ( `انشاء حساب بنكي` )')
     else:
       if r.get(f'{user.id}:BankWait3JL'):
         get = r.ttl(f'{user.id}:BankWait3JL')
         wait = time.strftime('%M:%S', time.gmtime(get))
         return await message.reply_text(f'{k} مايمديك تلعب عجلة الحين ! \n{k} تعال بعد {wait} دقيقة')
       else:
         r.set(f'{user.id}:BankWait3JL',1,ex=300)
         rep = await message.reply_text(f'{k} حلف العجلة بعد ٣ ثواني',reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ('³',callback_data='None')]]))
         await asyncio.sleep(1)
         rep.edit_text(f'{k} حلف العجلة بعد ثانيتين',reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ('²',callback_data='None')]]))
         await asyncio.sleep(1)
         rep.edit_text(f'{k} حلف العجلة بعد ثانية',reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ('¹',callback_data='None')]]))
         await asyncio.sleep(1)
         emojis_3jl = [
         '💸','💸','💸','💸','💸','💸','💸',
         '💸','💸','💸','💸','💸','💸','💸',
         '⚡','⚡','⚡','⚡','⚡','⚡','⚡',
         '⚡','⚡','⚡','⚡','⚡','⚡','⚡',
         '💣','💣','💣','💣','💣','💣','💣',
         '💣','💣','💣','💣','💣','💣','💣',
         '🍒','🍒','🍒','🍒','🍒','🍒','🍒',
         '🍒','🍒','🍒','🍒','🍒','🍒','🍒',
         '💎','💎','💎','💎','💎','💎','💎',
         '💎','💎','💎','💎','💎','💎','💎'
         ]
         emoji1 = random.choice(emojis_3jl)
         emoji2 = random.choice(emojis_3jl)
         emoji3 = random.choice(emojis_3jl)
         reply_ma = InlineKeyboardMarkup (
           [
             [
               InlineKeyboardButton (emoji1, callback_data='None'),
               InlineKeyboardButton (emoji2, callback_data='None'),
               InlineKeyboardButton (emoji3, callback_data='None'),
             ],
             [
               InlineKeyboardButton ('🫦', url=f't.me/{channel}')
             ]
           ]
         )
         if emoji1 == emoji2 and emoji2 == emoji3:
            chance = random.choice([100000, 200000, 300000])
            if not r.get(f'{user.id}:Floos'):
              floos = 0
            else:
              floos = int(r.get(f'{user.id}:Floos'))
            rep.edit_text(f'{k} فزت بعجلة الحظ!\n\n{k} مبلغ الربح ( {chance} ريال 💸 )\n{k} فلوسك قبل ( `{floos}` ريال 💸 )\n{k} فلوسك الحين ( `{floos+chance}` ريال 💸 )',reply_markup=reply_ma)
            r.set(f'{user.id}:Floos', floos+chance)
         else:
            chance = random.randint(100,1000)
            if not r.get(f'{user.id}:Floos'):
              floos = 0
            else:
              floos = int(r.get(f'{user.id}:Floos'))
            rep.edit_text(f'{k} للأسف خسرت بعجلة الحظ!\n\n{k} خذ {chance} ريال عشان ماتصيح\n{k} فلوسك قبل ( `{floos}` ريال 💸 )\n{k} فلوسك الحين ( `{floos+chance}` ريال 💸 )',reply_markup=reply_ma)
            r.set(f'{user.id}:Floos', floos+chance)
           
   if text.startswith('استثمار ') and len(text.split()) == 2 and re.findall('[0-9]+', text):
     if not r.sismember('BankList', user.id):
       return await message.reply_text(f'{k} ماعندك حساب بنكي ارسل ↢ ( `انشاء حساب بنكي` )')
     if r.get(f'{user.id}:BankWaitEST'):
       get = r.ttl(f'{user.id}:BankWaitEST')
       wait = time.strftime('%M:%S', time.gmtime(get))
       return await message.reply_text(f'{k} مايمديك تستثمر الحين ! \n{k} تعال بعد {wait} دقيقة')
     else:
       if not r.get(f'{user.id}:Floos'):
         floos = 0
       else:
         floos = int(r.get(f'{user.id}:Floos'))
       floos_to_est = int(re.findall('[0-9]+', text)[0])
       if floos_to_est == 0:
         return await message.reply_text(f'{k} مايمدي تلعب بالصفر')
       if floos_to_est > floos:
         return await message.reply_text(f'{k} فلوسك ماتكفي')
       if floos_to_est < 2000:
         return await message.reply_text(f'{k} للأسف لازم تستثمر ب 2000 ريال عالأقل')
       else:
         r.set(f'{user.id}:BankWaitEST',1,ex=300)
         one = int(floos_to_est/random.randint(1,9))
         rb7 = int(is_what_percent_of(one,floos_to_est))
         r.set(f'{user.id}:Floos',floos+one)
         await message.reply_text(f'''
{k}  استثمار ناجح!
{k} نسبة الربح ↢ {rb7}%
{k} مبلغ الربح ↢ ( `{one}` ريال )
{k} فلوسك صارت ↢ ( `{floos+one}` ريال 💸 )
''')
   
   if text == "استثمار فلوسي":
     if not r.sismember('BankList', user.id):
       return await message.reply_text(f'{k} ماعندك حساب بنكي ارسل ↢ ( `انشاء حساب بنكي` )')
     if r.get(f'{user.id}:BankWaitEST'):
       get = r.ttl(f'{user.id}:BankWaitEST')
       wait = time.strftime('%M:%S', time.gmtime(get))
       return await message.reply_text(f'{k} مايمديك تستثمر الحين ! \n{k} تعال بعد {wait} دقيقة')
     else:
       if not r.get(f'{user.id}:Floos'):
         floos = 0
       else:
         floos = int(r.get(f'{user.id}:Floos'))
       floos_to_est = floos
       if floos_to_est == 0:
         return await message.reply_text(f'{k} مايمدي تستثمر بالصفر')
       if floos_to_est < 2000:
         return await message.reply_text(f'{k} للأسف لازم تستثمر ب 2000 ريال عالأقل')
       else:
         r.set(f'{user.id}:BankWaitEST',1,ex=300)
         one = int(floos_to_est/random.randint(1,9))
         rb7 = int(is_what_percent_of(one,floos_to_est))
         r.set(f'{user.id}:Floos',floos+one)
         await message.reply_text(f'''
{k}  استثمار ناجح!
{k} نسبة الربح ↢ {rb7}%
{k} مبلغ الربح ↢ ( `{one}` ريال )
{k} فلوسك صارت ↢ ( `{floos+one}` ريال 💸 )
''')
   
   if text == 'كنز':
     if not r.sismember('BankList', user.id):
       return await message.reply_text(f'{k} ماعندك حساب بنكي ارسل ↢ ( `انشاء حساب بنكي` )')
     if r.get(f'{user.id}:BankWaitKNZ'):
       get = r.ttl(f'{user.id}:BankWaitKNZ')
       wait = time.strftime('%M:%S', time.gmtime(get))
       return await message.reply_text(f'{k} كنزك بينزل بعد {wait} دقيقة')
     else:
       if not r.get(f'{user.id}:Floos'):
          floos = 0
       else:
          floos = int(r.get(f'{user.id}:Floos'))
       knz = random.choice(knzs)
       money = knz['credit']
       name = knz['name']
       r.set(f'{user.id}:BankWaitKNZ',1, ex=600)
       r.set(f'{user.id}:Floos', floos+money)
       fls = floos+money
       return await message.reply_text(f'اشعار ايداع {user.mention_html()}⁪⁬⁪⁬⁮⁪⁬⁪\nالمبلغ: **{money}** ريال\nالكنز: {name}\nنوع العملية: ربح كنز\nرصيدك الحين: **{fls}** ريال 💸')

   if text == 'بخشيش':
     if not r.sismember('BankList', user.id):
       return await message.reply_text(f'{k} ماعندك حساب بنكي ارسل ↢ ( `انشاء حساب بنكي` )')
     if r.get(f'{user.id}:BankWaitB5'):
       get = r.ttl(f'{user.id}:BankWaitB5')
       wait = time.strftime('%M:%S', time.gmtime(get))
       return await message.reply_text(f'{k} مايمدي اعطيك بخشيش الحين\n{k} تعال بعد {wait} دقيقة')
     else:
       b5 = random.randint(5,1000)
       r.set(f'{user.id}:BankWaitB5',1, ex=300)
       if not r.get(f'{user.id}:Floos'):
          floos = 0
       else:
          floos = int(r.get(f'{user.id}:Floos'))
       r.set(f'{user.id}:Floos', floos+b5)
       await message.reply_text(f'{k} دلعتك وعطيتك {b5} ريال 💸')
       
   if text == 'راتب':
     if not r.sismember('BankList', user.id):
       return await message.reply_text(f'{k} ماعندك حساب بنكي ارسل ↢ ( `انشاء حساب بنكي` )')
     if r.get(f'{user.id}:BankWait'):
       get = r.ttl(f'{user.id}:BankWait')
       wait = time.strftime('%M:%S', time.gmtime(get))
       return await message.reply_text(f'{k} راتبك بينزل بعد {wait} دقيقة')
     else:
       job = random.choice(jobs)
       money = job['credit']
       name = job['name']
       r.set(f'{user.id}:BankWait',1, ex=300)
       if not r.get(f'{user.id}:Floos'):
          floos = 0
       else:
          floos = int(r.get(f'{user.id}:Floos'))
       r.set(f'{user.id}:Floos', floos+money)
       fls = floos+money
       await message.reply_text(f'اشعار ايداع⁪⁬⁪⁬⁮⁪⁬⁪ {user.mention_html()}\nالمبلغ: **{money}** ريال\nوظيفتك: {name}\nنوع العملية: اضافة راتب\nرصيدك الحين: **{fls}** ريال 💸')
   
   if text == 'زرف' and message.reply_to_message and message.reply_to_message.from_user:
     if message.reply_to_message.from_user.id == int(Dev_Zaid):
       return await message.reply_text('?')
     if not r.sismember('BankList', user.id):
       return await message.reply_text(f'{k} ماعندك حساب بنكي ارسل ↢ ( `انشاء حساب بنكي` )')
     if not r.sismember('BankList', message.reply_to_message.from_user.id):
       return await message.reply_text(f'{k} ماعنده حساب بنكي')
     if message.reply_to_message.from_user.id == user.id:
       return await message.reply_text('تبي تزرف نفسك؟')
     if r.get(f'{user.id}:BankWaitZRF'):
       get = r.ttl(f'{user.id}:BankWaitZRF')
       wait = time.strftime('%M:%S', time.gmtime(get))
       return await message.reply_text(f'{k} يولد انحش الشرطة للحين تدور عنك\n{k} يمديك تزرف مره ثانيه بعد {wait}')
     if r.get(f'{message.reply_to_message.from_user.id}:BankWaitMZROF'):
       get = r.ttl(f'{message.reply_to_message.from_user.id}:BankWaitMZROF')
       wait = time.strftime('%M:%S', time.gmtime(get))
       return await message.reply_text(f'{k} ذا المسكين مزروف قبل شوي\n{k} يمديك تزرفه بعد {wait}')
     if not r.get(f'{message.reply_to_message.from_user.id}:Floos'):
       return await message.reply_text(f'{k} مطفر مامعه ولا ريال')
     if int(r.get(f'{message.reply_to_message.from_user.id}:Floos')) < 2000:
       return await message.reply_text(f'{k} مايمديك تزرفه لان فلوسه اقل من 2000 ريال')
     else:
       zrf = random.randint(50,1000)
       r.set(f'{user.id}:BankWaitZRF',1,ex=300)
       r.set(f'{message.reply_to_message.from_user.id}:BankWaitMZROF',1,ex=300)
       floos = int(r.get(f'{message.reply_to_message.from_user.id}:Floos'))
       r.set(f'{message.reply_to_message.from_user.id}:Floos',floos-zrf)
       await message.reply_text(f'{k} خذ يالحرامي زرفته {zrf} ريال 💸')
       if not r.get(f'{user.id}:Floos'):
         floos_from_user = 0
       else:
         floos_from_user = int(r.get(f'{user.id}:Floos'))
       r.set(f'{user.id}:Floos',floos_from_user+zrf)
       r.sadd('BankZrf',user.id)
       if r.get(f'{user.id}:Zrf'):
          zrff = int(r.get(f'{user.id}:Zrf'))
       else:
          zrff = 0
       r.set(f'{user.id}:Zrf',zrff+zrf)
       try:
         pass
       except:
         pass
       
  
   if text == 'تصفير البنك':
     if devp_pls(user.id,chat.id):
        return await message.reply_text(f'{k} متأكد تبي تصفر البنك ؟',reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ('اي', callback_data='yes:del:bank')],[InlineKeyboardButton ('لا', callback_data='no:del:bank')]]))
   
   if text == 'فلوسي':
     if not r.get(f'{user.id}:Floos'):
        await message.reply_text(f'{k} ماعندك فلوس ارسل الالعاب وابدا جمع الفلوس')
     else:
        floos = int(r.get(f'{user.id}:Floos'))
        return await message.reply_text(f'{k} فلوسك `{floos}` ريال 💸')
   
   if text == 'فلوس':
     if not message.reply_to_message:
       if not r.get(f'{user.id}:Floos'):
         return await message.reply_text(f'{k} ماعندك فلوس ارسل الالعاب وابدا جمع الفلوس')
       else:
         floos = int(r.get(f'{user.id}:Floos'))
       return await message.reply_text(f'{k} فلوسك `{floos}` ريال 💸')
     else:
       if not r.get(f'{message.reply_to_message.from_user.id}:Floos'):
         floos = 0
       else:
         floos = int(r.get(f'{message.reply_to_message.from_user.id}:Floos'))
       return await message.reply_text(f'{k} فلوسه ↢ ( {floos} ريال 💸 )')
   
   if text.startswith('بيع فلوسي ') and len(text.split()) == 3 and re.findall('[0-9]+', text):
     if not r.get(f'{user.id}:Floos'):
        await message.reply_text(f'{k} للاسف انت مطفر عندك 0 ريال')
     else:
        floos_to_sale = int(re.findall('[0-9]+', text)[0])
        floos = int(r.get(f'{user.id}:Floos'))
        if floos_to_sale == 0:
         return await message.reply_text(f'{k} مايمدي تبيع صفر')
        if floos_to_sale > floos:
          return await message.reply_text(f'{k} للاسف انت مطفر عندك {floos} ريال')
        if floos_to_sale == floos:
           r.delete(f'{user.id}:Floos')
        else:
           r.set(f'{user.id}:Floos',floos-floos_to_sale)
        get = int(r.get(f'{chat.id}:TotalMsgs:{user.id}{Dev_Zaid}'))
        rsayl = floos_to_sale * 20
        r.set(f'{chat.id}:TotalMsgs:{user.id}{Dev_Zaid}', get+rsayl)
        await message.reply_text(f'{k} بعت ( {floos_to_sale} ريال 💸 ) من فلوسك\n{k} مجموع رسايلك الحين ( {get + rsayl} )\n☆')
   
   if text.startswith('اضف فلوس ') and len(text.split()) == 3 and re.findall('[0-9]+', text):
     if dev2_pls(user.id,chat.id):
       if message.reply_to_message and message.reply_to_message.from_user:
          floos_to_add = int(re.findall('[0-9]+', text)[0])
          if not r.get(f'{message.reply_to_message.from_user.id}:Floos'):
             r.set(f'{message.reply_to_message.from_user.id}:Floos',floos_to_add)
          else:
             floos = int(r.get(f'{message.reply_to_message.from_user.id}:Floos'))
             r.set(f'{message.reply_to_message.from_user.id}:Floos',floos_to_add+floos)
          user_mention = f'<a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>'
          await message.reply_text(f'「 {user_mention} 」\n{k} ضفت له ( {floos_to_add} ) ريال 💸', parse_mode=ParseMode.HTML)
   
   
   if text == 'استخراج الاكواد':
      if devp_pls(user.id,chat.id):
         if r.get(f'{Dev_Zaid}:codeWait'):
           t = r.ttl(f'{Dev_Zaid}:codeWait')
           wait = time.strftime('%H:%M:%S', time.gmtime(t))
           return await message.reply_text(f'{k} استخرجت اكواد الكشط من شوي تعال بعد {wait}')
         else:
           txt = 'اكواد الكشط:\n'
           ccc = 1
           for none in range(10):
             code = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
             r.set(f'{code}:CodeBank:{Dev_Zaid}',1,ex=7200)
             txt += f'{ccc} ) `{code}`\n'
             ccc += 1
           r.set(f'{Dev_Zaid}:codeWait',1,ex=7200)
           txt += '\n~ الأكواد صالحة لساعتين فقط .'
           txt += '\n༄'
           return await message.reply_text(txt)
   
   if text.startswith('كشط ') and len(text.split()) == 2:
     code = text.split()[1]
     if not r.get(f'{code}:CodeBank:{Dev_Zaid}'):
       return await message.reply_text(f'{k} الكود منتهي الصلاحيه او تابع لبوت ثاني')
     if r.get(f'{user.id}:BankWaitKSHT:{Dev_Zaid}'):
       t = r.ttl(f'{user.id}:BankWaitKSHT:{Dev_Zaid}')
       wait = time.strftime('%H:%M:%S', time.gmtime(t))
       return await message.reply_text(f'{k} كشطت كود من شوي تعال بعد {wait}')
     else:
       r.delete(f'{code}:CodeBank:{Dev_Zaid}')
     if not r.get(f'{user.id}:Floos'):
       floos_from_user = 0
     else:
       floos_from_user = int(r.get(f'{user.id}:Floos'))
     chance = random.choice([1000000000, 2000000000, 3000000000])
     r.set(f'{user.id}:Floos',floos_from_user+chance)
     await message.reply_text(f'{k} مبرووووك 🏆\n{k} كشطت الكود واخذت ( {chance} ريال 💸 )\n{k} فلوسك قبل ( `{floos_from_user}` ريال 💸 )\n{k} فلوسك الحين ( `{floos_from_user+chance}` ريال 💸 )')
     r.set(f'{user.id}:BankWaitKSHT:{Dev_Zaid}',1,ex=7200)
     if r.get(f'DevGroup:{Dev_Zaid}'):
       alert = f'𖡋 𝐍𝐀𝐌𝐄 ⌯ {user.mention_html()}\n𖡋 𝐈𝐃 ⌯ `{user.id}`\n\nكشط الكود `{code}` وأخذ {chance} ريال 💸'
       pass
     if message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.is_bot:
       return False
     if r.get(f'{user.id}:marriedMan:{chat.id}{Dev_Zaid}'):
       getUser = None
       mention = [مستخدم]
       return await message.reply_text(f'「 {mention} 」 \n{k} تعاليييي زوجك بيخونك')
     if r.get(f'{user.id}:marriedWomen:{chat.id}{Dev_Zaid}'):
       getUser = None
       mention = [مستخدم]
       return await message.reply_text(f'「 {mention} 」 \n{k} تعال زوجتك بتخونك')
     if not r.get(f'{user.id}:Floos'):
       floos_from_user = 0
     else:
       floos_from_user = int(r.get(f'{user.id}:Floos'))
     floos = int(re.findall('[0-9]+', text)[0])
     if floos > floos_from_user:
       return await message.reply_text('مطفر فلوسك ماتكفي')
     else:
       if r.get(f'{message.reply_to_message.from_user.id}:marriedWomen:{chat.id}{Dev_Zaid}'):
         return await message.reply_text('「 {} 」 \n{} مو سنقل دورلك غيرها\n༄'.format(f'<a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>',k))
       if r.get(f'{message.reply_to_message.from_user.id}:marriedMan:{chat.id}{Dev_Zaid}'):
         return await message.reply_text('「 {} 」 \n{} مو سنقل دورلك غيره\n༄'.format(f'<a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>',k))
       else:
         if floos < 50000:
           return await message.reply_text('لازم المهر اقل شي 50 ألف ريال')
         else:
           if floos == floos_from_user:
             r.delete(f'{user.id}:Floos')
           else:
             r.set(f'{user.id}:Floos',floos_from_user-floos)
           r.set(f'{user.id}:marriedMan:{chat.id}{Dev_Zaid}',message.reply_to_message.from_user.id)
           r.set(f'{message.reply_to_message.from_user.id}:marriedWomen:{chat.id}{Dev_Zaid}',user.id)
           to_marry = '''
💒 وثيقة زواج

{k} 👰 العروس ↢ ( {one} )
{k} 🤵 العريس ↢ ( {two} )
'''
           to_marry += f'\n{k} 💸 المهر ↢ ( `{floos}` ريال )\n༄'
           r.set(f'{user.id}:MARRYTEXT:{chat.id}{Dev_Zaid}',to_marry)
           r.set(f'{message.reply_to_message.from_user.id}:MARRYTEXT:{chat.id}{Dev_Zaid}',to_marry)
           r.set(f'{user.id}:MARRYMONEY:{chat.id}{Dev_Zaid}',floos)
           r.set(f'{message.reply_to_message.from_user.id}:MARRYMONEY:{chat.id}{Dev_Zaid}',floos)
           r.sadd(f'{chat.id}:zwag:{Dev_Zaid}', f'{message.reply_to_message.from_user.id}--{user.id}&&floos={floos}')
           return await message.reply_text(f'''
{k} باركووو للعرسان 

{k} 👰 العروس ↢ ( {f'<a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>'} )
{k} 🤵 العريس ↢ ( {user.mention_html()} )

{k} 💸 المهر ↢ ( `{floos}` ريال )
☆
''')
           
           
   if text == 'زواجي':
     if not r.get(f'{user.id}:MARRYTEXT:{chat.id}{Dev_Zaid}'):
       return await message.reply_text(f'{k} انت سنقل')
     else:
       if r.get(f'{user.id}:marriedMan:{chat.id}{Dev_Zaid}'):
         getUser = None
         txt = r.get(f'{user.id}:MARRYTEXT:{chat.id}{Dev_Zaid}').format(k=k,two=user.mention_html(),one="مستخدم")
         return await message.reply_text(txt)
       if r.get(f'{user.id}:marriedWomen:{chat.id}{Dev_Zaid}'):
         getUser = None
         txt = r.get(f'{user.id}:MARRYTEXT:{chat.id}{Dev_Zaid}').format(k=k,two="مستخدم",one=user.mention_html())
         return await message.reply_text(txt)         
   
   if text == "سورس" or text == "السورس":
    return await message.reply_photo(
        "https://gcdnb.pbrd.co/images/bOMz1R4wG9xF.jpg",
        caption="سورس فلير حماية الكروبات، ارفعه مشرف بكروبك واحميها:",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("الدخول البوت 💥", url="https://t.me/scatteredda")]]
        )
    )
   
   if text== 'طلاق' and r.get(f'{user.id}:marriedMan:{chat.id}{Dev_Zaid}'):
     getUser = None
     floos = int(r.get(f'{user.id}:MARRYMONEY:{chat.id}{Dev_Zaid}'))
     r.srem(f'{chat.id}:zwag:{Dev_Zaid}', f'{0}--{user.id}&&floos={floos}')
     if not r.get(f'{0}:Floos'):
       floos_from_whife = 0
     else:
       floos_from_whife = int(r.get(f'{0}:Floos'))
     r.set(f'{0}:Floos', floos_from_whife+floos)
     r.delete(f'{user.id}:marriedMan:{chat.id}{Dev_Zaid}')
     r.delete(f'{0}:marriedWomen:{chat.id}{Dev_Zaid}')
     r.delete(f'{0}:MARRYTEXT:{chat.id}{Dev_Zaid}')
     r.delete(f'{user.id}:MARRYTEXT:{chat.id}{Dev_Zaid}')
     r.delete(f'{user.id}:MARRYMONEY:{chat.id}{Dev_Zaid}')
     r.delete(f'{0}:MARRYMONEY:{chat.id}{Dev_Zaid}')
     return await message.reply_text(f'{k} طلقتك من 「 {getUser.mention_html()} 」\n{k} ضفت ( {floos} ريال 💸 ) لفلوسها')
     
   
   if text== 'خلع' and r.get(f'{user.id}:marriedWomen:{chat.id}{Dev_Zaid}'):
     getUser = None
     floos = int(r.get(f'{user.id}:MARRYMONEY:{chat.id}{Dev_Zaid}'))
     r.srem(f'{chat.id}:zwag:{Dev_Zaid}', f'{user.id}--{0}&&floos={floos}')
     if not r.get(f'{0}:Floos'):
       floos_from_has = 0
     else:
       floos_from_has = int(r.get(f'{0}:Floos'))
     r.set(f'{0}:Floos', floos_from_has+floos)
     r.delete(f'{0}:marriedMan:{chat.id}{Dev_Zaid}')
     r.delete(f'{user.id}:marriedWomen:{chat.id}{Dev_Zaid}')
     r.delete(f'{0}:MARRYTEXT:{chat.id}{Dev_Zaid}')
     r.delete(f'{user.id}:MARRYTEXT:{chat.id}{Dev_Zaid}')
     r.delete(f'{user.id}:MARRYMONEY:{chat.id}{Dev_Zaid}')
     r.delete(f'{0}:MARRYMONEY:{chat.id}{Dev_Zaid}')
     return await message.reply_text(f'{k} خلعتك من 「 {getUser.mention_html()} 」\n{k} ورجعت له المهر ( {floos} ريال 💸 )')

   if text == 'كت' or text == 'تويت' or text == 'كت تويت':
      return await message.reply_text(random.choice(cut))
   
   if text == 'جمل':
     gmla = random.choice(gomal)
     r.set(f'{chat.id}:game:{Dev_Zaid}', gmla.replace(" '",""), ex=600)
     await message.reply_text(f'الجملة ↢ ( {gmla} )\n{k} اكتبها بدون فواصل')
   
   if r.get(f'{chat.id}:gameEmoji:{Dev_Zaid}'):
     if text == r.get(f'{chat.id}:gameEmoji:{Dev_Zaid}'):
        ra = random.randint(1,5)
        t = r.ttl(f'{chat.id}:gameEmoji:{Dev_Zaid}')
        timeo = f"{20 - int(t)}.{random.randint(1,9)}"
        r.delete(f'{chat.id}:gameEmoji:{Dev_Zaid}')
        if r.get(f'{user.id}:Floos'):
           get = int(r.get(f'{user.id}:Floos'))
           r.set(f'{user.id}:Floos',get+ra)
           floos = int(r.get(f'{user.id}:Floos'))
        else:
           floos = ra
           r.set(f'{user.id}:Floos',ra)
        return await message.reply_text(f'''
صح عليك ⁪⁬⁪⁬⁮⁪⁬⁪⁬⁮✔
⏰الوقت: {timeo} ثانية
💸فلوسك: {floos} ريال
☆
''')
   
   if r.get(f'{chat.id}:game5tm:{user.id}{Dev_Zaid}'):
    try:
     if int(text) == r.get(f'{chat.id}:game5tm:{user.id}{Dev_Zaid}'):
        ra = random.randint(1,5)
        t = r.ttl(f'{chat.id}:game5tm:{user.id}{Dev_Zaid}')
        timeo = f"{600 - int(t)}.{random.randint(1,9)}"
        r.delete(f'{chat.id}:game5tm:{user.id}{Dev_Zaid}')
        if r.get(f'{user.id}:Floos'):
           get = int(r.get(f'{user.id}:Floos'))
           r.set(f'{user.id}:Floos',get+ra)
           floos = int(r.get(f'{user.id}:Floos'))
        else:
           floos = ra
           r.set(f'{user.id}:Floos',ra)
        return await message.reply_text(f'''
صح عليك ⁪⁬⁪⁬⁮⁪⁬⁪⁬⁮✔
⏰الوقت: {timeo} ثانية
💸فلوسك: {floos} ريال
☆
''')
     else:
        r.delete(f'{chat.id}:game5tm:{user.id}{Dev_Zaid}')
        return await message.reply_text(f'{k} اجابتك خطأ')
    except:
     pass

   if r.get(f'{chat.id}:game:{Dev_Zaid}'):
     if text == r.get(f'{chat.id}:game:{Dev_Zaid}'):
        ra = random.randint(1,5)
        t = r.ttl(f'{chat.id}:game:{Dev_Zaid}')
        timeo = f"{600 - int(t)}.{random.randint(1,9)}"
        r.delete(f'{chat.id}:game:{Dev_Zaid}')
        if r.get(f'{user.id}:Floos'):
           get = int(r.get(f'{user.id}:Floos'))
           r.set(f'{user.id}:Floos',get+ra)
           floos = int(r.get(f'{user.id}:Floos'))
        else:
           floos = ra
           r.set(f'{user.id}:Floos',ra)
        await message.reply_text(f'''
صح عليك ⁪⁬⁪⁬⁮⁪⁬⁪⁬⁮✔
⏰الوقت: {timeo} ثانية
💸فلوسك: {floos} ريال
☆
''')
        return True
     
   
   if text == 'ترتيب':
     name = random.choice(trteep)
     name1 = name
     name = re.sub('سحور', 'س ر و ح', name)
     name = re.sub('سياره', 'ه ر س ي ا', name)
     name = re.sub('استقبال', 'ل ب ا ت ق س ا', name)
     name = re.sub('قنافه', 'ه ق ا ن ف', name)
     name = re.sub('ايفون', 'و ن ف ا', name)
     name = re.sub('بطاطس', 'ب ط ا ط س', name)
     name = re.sub('مطبخ', 'خ ب ط م', name)
     name = re.sub('كرستيانو', 'س ت ا ن و ك ر ي', name)
     name = re.sub('دجاجه', 'ج ج ا د ه', name)
     name = re.sub('مدرسه', 'ه م د ر س', name)
     name = re.sub('الوان', 'ن ا و ا ل', name)
     name = re.sub('غرفه', 'غ ه ر ف', name)
     name = re.sub('ثلاجه', 'ج ه ت ل ا', name)
     name = re.sub('قهوه', 'ه ق ه و', name)
     name = re.sub('سفينه', 'ه ن ف ي س', name)
     name = re.sub('مصر', 'ر م ص', name)
     name = re.sub('محطه', 'ه ط م ح', name)
     name = re.sub('طياره', 'ر ا ط ي ه', name)
     name = re.sub('رادار', 'ر ا ر ا د', name)
     name = re.sub('منزل', 'ن ز م ل', name)
     name = re.sub('مستشفى', 'ى ش س ف ت م', name)
     name = re.sub('كهرباء', 'ر ب ك ه ا ء', name)
     name = re.sub('تفاحه', 'ح ه ا ت ف', name)
     name = re.sub('اخطبوط', 'ط ب و ا خ ط', name)
     name = re.sub('سنترال', 'ن ر ت ل ا س', name)
     name = re.sub('فرنسا', 'ن ف ر س ا', name)
     name = re.sub('برتقاله', 'ر ت ق ب ا ه ل', name)
     name = re.sub('تفاح', 'ح ف ا ت', name)
     name = re.sub('مطرقه', 'ه ط م ر ق', name)
     name = re.sub('هريسه', 'س ه ر ي ه', name)
     name = re.sub('لبانه', 'ب ن ل ه ا', name)
     name = re.sub('شباك', 'ب ش ا ك', name)
     name = re.sub('باص', 'ص ا ب', name)
     name = re.sub('سمكه', 'ك س م ه', name)
     name = re.sub('ذباب', 'ب ا ب ذ', name)
     name = re.sub('تلفاز', 'ت ف ل ز ا', name)
     name = re.sub('حاسوب', 'س ا ح و ب', name)
     name = re.sub('انترنت', 'ا ت ن ر ن ت', name)
     name = re.sub('ساحه', 'ح ا ه س', name)
     name = re.sub('جسر', 'ر ج س', name)
     r.set(f'{chat.id}:game:{Dev_Zaid}', name1,ex=600)
     await message.reply_text(f'رتب ↢ {name}')
     return True
   
   if text == 'ايموجي':
      if r.get(f'{chat.id}:gameEmoji:{Dev_Zaid}'):
        return await message.reply_text(f'{k} معليش في لعبة ايموجي شغالة الحين حاول بعد 20 ثانية\n\n{k} في حال ماتبي تكملها ارسل سكب')
      ran = random.choice(emojis_pics)
      emoji = ran['emoji']
      photo = ran['photo']
      a = await message.reply_photo(photo,caption='اسرع واحد يرسل الايموجي')
      r.delete(f'{chat.id}:game:{Dev_Zaid}')
      await asyncio.sleep(3)
      r.set(f'{chat.id}:gameEmoji:{Dev_Zaid}', emoji,ex=20)
      a.edit_media(media=InputMediaPhoto (media='https://telegra.ph/file/b53b14951a50d7f75c39e.jpg', caption='ارسل الايموجي الحين'))
      return True
   
   if text == 'سكب':
      if r.get(f'{chat.id}:gameEmoji:{Dev_Zaid}'):
         r.delete(f'{chat.id}:gameEmoji:{Dev_Zaid}')
         await message.reply_text(f'{k} سكبت لعبه الايموجي')
         return True
   
   if text == 'انقليزي':
     name = random.choice(english)
     name1 = name
     name = re.sub("ذئب", "wolf", name)
     name = re.sub("معلومات", "information", name)
     name = re.sub("قنوات", "channels", name)
     name = re.sub("مجموعات", "groups", name)
     name = re.sub("كتاب", "book", name)
     name = re.sub("تفاحه", "apple", name)
     name = re.sub("مصر", "egypt", name)
     name = re.sub("فلوس", "money", name)
     name = re.sub("اعلم", "i know", name)
     name = re.sub("تمساح", "crocodile", name)
     name = re.sub("مختلف", "different", name)
     name = re.sub("ذكي", "intelligent", name)
     name = re.sub("كلب", "dog", name)
     name = re.sub("صقر", "falcon", name)
     name = re.sub("مشكله", "error", name)
     name = re.sub("كمبيوتر", "computer", name)
     name = re.sub("اصدقاء", "friends", name)
     name = re.sub("منضده", "table", name)
     r.set(f'{chat.id}:game:{Dev_Zaid}', name1,ex=600)
     await message.reply_text(f'اكتب معنى ↢ ( {name} )')
     return True
   
   if text == 'معاني':
     name = random.choice(m3any)
     name1 = name
     name = re.sub("قرد", "🐒", name)
     name = re.sub("دجاجه", "🐔", name)
     name = re.sub("بطريق", "🐧", name)
     name = re.sub("ضفدع", "🐸", name)
     name = re.sub("بومه", "🦉", name)
     name = re.sub("نحله", "🐝", name)
     name = re.sub("ديك", "🐓", name)
     name = re.sub("جمل", "🐫", name)
     name = re.sub("بقره", "🐄", name)
     name = re.sub("دولفين", "🐳", name)
     name = re.sub("تمساح", "🐊", name)
     name = re.sub("قرش", "🦈", name)
     name = re.sub("نمر", "🐅", name)
     name = re.sub("اخطبوط", "🐙", name)
     name = re.sub("سمكه", "🐟", name)
     name = re.sub("خفاش", "🦇", name)
     name = re.sub("اسد", "🦁", name)
     name = re.sub("فأر", "🐭", name)
     name = re.sub("ذئب", "🐺", name)
     name = re.sub("فراشه", "🦋", name)
     name = re.sub("عقرب", "🦂", name)
     name = re.sub("زرافه", "🦒", name)
     name = re.sub("قنفذ", "🦔", name)
     name = re.sub("تفاحه", "🍎", name)
     name = re.sub("باذنجان", "🍆", name)
     name = re.sub("قوس قزح", "🌈", name)
     name = re.sub("بزازه", "🍼", name)
     name = re.sub("بطيخ", "🍉", name)
     name = re.sub("وزه", "🦆", name)
     name = re.sub("كتكوت", "🐣", name)
     r.set(f'{chat.id}:game:{Dev_Zaid}', name1,ex=600)
     await message.reply_text(f'ايش معنى الايموجي ↢ ( {name} )')
     return True
   
   if text == 'احسب':
     name = random.choice(Maths)
     name1 = name
     name = re.sub("200", "250 - 50 = ?", name)
     name = re.sub("605", "655 - 50 = ?", name)
     name = re.sub("210", "247 - 37 = ?", name)
     name = re.sub("128", "168 - 40 = ?", name)
     name = re.sub("126", "202 - 76 = ?", name)
     name = re.sub("263", "31297 ÷ 119 = ?", name)
     name = re.sub("150", "246 - 96 = ?", name)
     name = re.sub("2000", "200 × 10 = ?", name)
     name = re.sub("40", "95 - 55 = ?", name)
     name = re.sub("242", "276 - 34 = ?", name)
     name = re.sub("14", "29 - 15 = ?", name)
     name = re.sub("13", "16 - 3 = ?", name)
     name = re.sub("1000", "956 + 44 = ?", name)
     name = re.sub("810", "767 + 43 = ?", name)
     name = re.sub("110", "77 + 33 = ?", name)
     name = re.sub("830", "745 + 85 = ?", name)
     name = re.sub("111", "66 + 45 = ?", name)
     name = re.sub("92", "61 + 31 = ?", name)
     name = re.sub("1110", "988 + 122 = ?", name)
     name = re.sub("6800", "85 × 80 = ?", name)
     name = re.sub("1554", "777 × 2 = ?", name)
     name = re.sub("920", "92 × 10 = ?", name)
     name = re.sub("1740", "87 × 20 = ?", name)
     name = re.sub("1140", "76 × 15 = ?", name)
     name = re.sub("1056", "88 × 12 = ?", name)
     name = re.sub("331", "243 + 88 = ?", name)
     name = re.sub("162", "250 - 88 = ?", name)
     name = re.sub("245", "290 - 45 = ?", name)
     name = re.sub("900", "975 - 75 = ?", name)
     name = re.sub("791", "878 - 87= ?", name)
     name = re.sub("0", "99 - 99 = ?", name)
     name = re.sub("57", "77 - 20 = ?", name)
     name = re.sub("220", "250 - 30 = ?", name)
     r.set(f'{chat.id}:game:{Dev_Zaid}', name1,ex=600)
     await message.reply_text(f'{name}')
     return True
   
   if text == 'عربي':
     name = random.choice(Arab)
     name1 = name
     name = re.sub("اناث", "انثى", name)
     name = re.sub("ثيران", "ثور", name)
     name = re.sub("دروس", "درس", name)
     name = re.sub("فحص", "فحوص", name)
     name = re.sub("رجال", "رجل", name)
     name = re.sub("كتب", "كتاب", name)
     name = re.sub("ضغوط", "ضغط", name)
     name = re.sub("صف", "صفوف", name)
     name = re.sub("عصفور", "عصافير", name)
     name = re.sub("لصوص", "لص", name)
     name = re.sub("تماسيح", "تمساح", name)
     name = re.sub("ملك", "ملوك", name)
     name = re.sub("فصل", "فصول", name)
     name = re.sub("كلاب", "كلب", name)
     name = re.sub("صقور", "صقر", name)
     name = re.sub("عقد", "عقود", name)
     name = re.sub("بحور", "بحر", name)
     name = re.sub("هاتف", "هواتف", name)
     name = re.sub("حدائق", "حديقه", name)
     name = re.sub("مسرح", "مسارح", name)
     name = re.sub("جرائم", "جريمة", name)
     name = re.sub("مدارس", "مدرسة", name)
     name = re.sub("منزل", "منازل", name)
     name = re.sub("كرسي", "كراسي", name)
     name = re.sub("مناطق", "منطقة", name)
     name = re.sub("بيوت", "بيت", name)
     name = re.sub("بنك", "بنوك", name)
     name = re.sub("علم", "علوم", name)
     name = re.sub("وظائف", "وظيفة", name)
     name = re.sub("طلاب", "طالب", name)
     name = re.sub("مراحل", "مرحلة", name)
     name = re.sub("فنانين", "فنان", name)
     name = re.sub("صواريخ", "صاروخ", name)
     r.set(f'{chat.id}:game:{Dev_Zaid}', name1,ex=600)
     await message.reply_text(f'اكتب جمع او مفرد ↢ ( {name} )')
     return True
   
   if text == 'كلمات':
     name = random.choice(words)
     '''
     name1 = name
     name = re.sub("ذئب", "ذئب", name)
     name = re.sub("معلومات", "معلومات", name)
     name = re.sub("قنوات", "قنوات", name)
     name = re.sub("مجموعات", "مجموعات", name)
     name = re.sub("كتاب", "كتاب", name)
     name = re.sub("تفاحه", "تفاحه", name)
     name = re.sub("مصر", "مصر", name)
     name = re.sub("فلوس", "فلوس", name)
     name = re.sub("اعلم", "اعلم", name)
     name = re.sub("تمساح", "تمساح", name)
     name = re.sub("مختلف", "مختلف", name)
     name = re.sub("ذكي", "ذكي", name)
     name = re.sub("كلب", "كلب", name)
     name = re.sub("صقر", "صقر", name)
     name = re.sub("مشكله", "مشكله", name)
     name = re.sub("كمبيوتر", "كمبيوتر", name)
     name = re.sub("اصدقاء", "اصدقاء", name)
     name = re.sub("منضده", "منضده", name)
     name = re.sub("سائق", "سائق", name)
     name = re.sub("جبل", "جبل", name)
     name = re.sub("مفتاح", "مفتاح", name)
     name = re.sub("يساوي", "يساوي", name)
     name = re.sub("انتبه", "انتبه", name)
     name = re.sub("موقد", "موقد", name)
     name = re.sub("مكتئب", "مكتئب", name)
     name = re.sub("انسان", "انسان", name)
     name = re.sub("ضفدع", "ضفدع", name)
     name = re.sub("عشق", "عشق", name)
     name = re.sub("منزل", "منزل", name)
     name = re.sub("طلاب", "طلاب", name)
     name = re.sub("فنان", "فنان", name)
     name = re.sub("صاروخ", "صاروخ", name)
     '''
     r.set(f'{chat.id}:game:{Dev_Zaid}', name,ex=600)
     await message.reply_text(f'الكلمة ↢ ( {name} )')
     return True

   if text == 'تفكيك':
     tfkeek = random.choice(trteep)
     name = ' '.join(a for a in tfkeek)
     r.set(f'{chat.id}:game:{Dev_Zaid}', name,ex=600)
     await message.reply_text(f'فكك ↢ ( {tfkeek} )')
     return True
   
   
   if text == 'عواصم':
     country=random.choice(countries)
     name = country['name']
     capital=country['capital']
     r.set(f'{chat.id}:game:{Dev_Zaid}', capital,ex=600)
     await message.reply_text(f'{k} ايش عاصمة {name} ؟')
     return True
   
   if text == 'اكمل':
     name = random.choice(mthal)
     name1 = name
     name = re.sub("اخوات", "لو قلبك مات متجيش على اتنين ... ", name)
     name = re.sub("زيهم", "اى ياعمهم اشتكيلك منهم تعمل ... ", name)
     name = re.sub("شمعتك", "دارى على ... تقيد", name)
     name = re.sub("داره", "من خرج من ... قل مقداره", name)
     name = re.sub("الوالدين", "رضا ... احسن من ابوك وامك", name)
     name = re.sub("الرءوس", "اذا تطاول الايدي تساوت ... ", name)
     name = re.sub("مرايه", "فى الوش ... وفى القفه سلايه", name)
     name = re.sub("حدو", "الشئ اللى يزيد عن ...  ينقلب لضدو", name)
     name = re.sub("رجالها", "مايجبها الا  ... ", name)
     name = re.sub("عدوك", "امشى عدل يحتار ... فيك", name)
     name = re.sub("الزبيب", "ضرب الحبيب زى اكل  ... ", name)
     name = re.sub("الغراب", "ياما جاب ...  لامه", name)
     name = re.sub("ماتو", "اللى اغتشو ... ", name)
     name = re.sub("اتمكن", "اتمسكن لحد ما ... ", name)
     name = re.sub("زجاج", "اللى بيتو من ... مايحدفش الناس بالطوب", name)
     name = re.sub("فار", "لو غاب القط العب يا ... ", name)
     name = re.sub("شهر", "امشي ... ولا تعدى نهر", name)
     name = re.sub("القتيل", "يقتل ... ويمشى فى جنازته", name)
     name = re.sub("الغطاس", "المايه تكدب ... ", name)
     name = re.sub("يكحلها", "جه ... عماها", name)
     name = re.sub("امه", "القرد فى عين ... غزال", name)
     r.set(f'{chat.id}:game:{Dev_Zaid}', name1 ,ex=600)
     await message.reply_text(f'اكمل ↢ ( {name} ؟ )')
     return True
   
   if text == 'احكام':
     if r.get(f'{chat.id}:AHKAMGAME:{Dev_Zaid}'):
       return await message.reply_text(f"{k} معليش في لعبة احكام شغالة الحين حاول بعد دقيقة")
     await message.reply_text(f'''
{k} بدينا لعبة احكام واضفت اسمك 
{k} اللي يبي يلعب يرسل كلمة ( انا ) 

{k} اللي عليك انت صاحب اللعبة ترسل ( تم ) اذا اكتمل العدد
☆
''')
     r.delete(f'{chat.id}:ListAhkam:{Dev_Zaid}')
     r.set(f'{chat.id}:AHKAMGAME:{Dev_Zaid}',user.id,ex=120)
     r.sadd(f'{chat.id}:ListAhkam:{Dev_Zaid}',user.id)
     return True
     
   if text == 'انا' and r.get(f'{chat.id}:AHKAMGAME:{Dev_Zaid}'):
     if r.sismember(f'{chat.id}:ListAhkam:{Dev_Zaid}',user.id):
       return await message.reply_text(f"{k} اسمك موجود بالقائمة")
     else:
       await message.reply_text(f"{k} ضفت اسمك للقائمة")
       r.sadd(f'{chat.id}:ListAhkam:{Dev_Zaid}',user.id)
       return True
  
   if text == 'تم' and r.get(f'{chat.id}:AHKAMGAME:{Dev_Zaid}') and user.id == int(r.get(f'{chat.id}:AHKAMGAME:{Dev_Zaid}')):
     if len(r.smembers(f'{chat.id}:ListAhkam:{Dev_Zaid}')) == 1:
       return await message.reply_text(f"{k} مافيه لاعبين")
     else:
       ids = [elem for elem in r.smembers(f'{chat.id}:ListAhkam:{Dev_Zaid}')]
       id = random.choice(ids)
       getUser = None
       _user_mention = '[مستخدم]'
       await message.reply_text(f"{k} تم اختيار ( ⁪⁬⁪⁬{_user_mention} ) للحكم عليه")
       r.delete(f'{chat.id}:ListAhkam:{Dev_Zaid}')
       r.delete(f'{chat.id}:AHKAMGAME:{Dev_Zaid}')
       return True
   
   
   if text == 'روليت':
     if r.get(f'{chat.id}:ROLETGAME:{Dev_Zaid}'):
       return await message.reply_text(f"{k} معليش في لعبة روليت شغالة الحين حاول بعد دقيقة")
     await message.reply_text(f'''
{k} بدينا لعبة الروليت واضفت اسمك 
{k} اللي يبي يلعب يرسل كلمة ( انا ) 

{k} اللي عليك انت صاحب اللعبة ترسل ( تم ) اذا اكتمل العدد
☆
''')
     r.delete(f'{chat.id}:ListRolet:{Dev_Zaid}')
     r.set(f'{chat.id}:ROLETGAME:{Dev_Zaid}',user.id,ex=120)
     r.sadd(f'{chat.id}:ListRolet:{Dev_Zaid}',user.id)
     return True
     
   if text == 'انا' and r.get(f'{chat.id}:ROLETGAME:{Dev_Zaid}'):
     if r.sismember(f'{chat.id}:ListRolet:{Dev_Zaid}',user.id):
       return await message.reply_text(f"{k} اسمك موجود بالقائمة")
     else:
       await message.reply_text(f"{k} ضفت اسمك للقائمة")
       r.sadd(f'{chat.id}:ListRolet:{Dev_Zaid}',user.id)
       return True
  
   if text == 'تم' and r.get(f'{chat.id}:ROLETGAME:{Dev_Zaid}') and user.id == int(r.get(f'{chat.id}:ROLETGAME:{Dev_Zaid}')):
     if len(r.smembers(f'{chat.id}:ListRolet:{Dev_Zaid}')) == 1:
       return await message.reply_text(f"{k} مافيه لاعبين")
     else:
       ids = [elem for elem in r.smembers(f'{chat.id}:ListRolet:{Dev_Zaid}')]
       id = random.choice(ids)
       getUser = None
       await message.reply_text(f"{k} مبروك اخترت اللاعب ( [مستخدم] ) واخذ 3 مجوهرات")
       if not r.get(f'{0}:Floos'):
         floos = 0
       else:
         floos = int(r.get(f'{0}:Floos'))
       r.set(f"{0}:Floos",floos+10)
       r.delete(f'{chat.id}:ListRolet:{Dev_Zaid}')
       r.delete(f'{chat.id}:ROLETGAME:{Dev_Zaid}')
       return True
       
  
   if text == 'خواتم':
     name = random.randint(1,6)
     r.set(f'{chat.id}:game5tm:{user.id}{Dev_Zaid}', name ,ex=600)
     r.delete(f'{chat.id}:game:{Dev_Zaid}')
     return await message.reply_text('''
１    ２      ３     ４    ５     ６
  ↓     ↓      ↓     ↓     ↓     ↓
  ✋🏼 ‹› ✋🏼 ‹› ✋🏼 ‹› ✋🏼 ‹› ✋🏼 ‹› ✋🏼
  
  
⚘ اختار اليد اللي تتوقع فيها الخاتم
     ''')
   
   if text == 'اعلام':
     country=random.choice(countries_)
     name = country['name']
     flag=country['flag']
     r.set(f'{chat.id}:game:{Dev_Zaid}', name,ex=600)
     await message.reply_photo(flag, caption='ايش اسم الدولة ؟')
     return True
   
   if text == 'دين':
     dee = random.choice(deen)
     question = dee['question']
     answer = dee['answer']
     r.set(f'{chat.id}:game:{Dev_Zaid}', answer ,ex=600)
     await message.reply_text(question)
     return True
   
   if text == 'سيارات':
     car = random.choice(cars)
     brand = car["brand"]
     r.set(f'{chat.id}:game:{Dev_Zaid}', brand ,ex=600)
     await message.reply_photo(car['photo'], caption='وش اسم السيارة ؟')
     return True
   
   if text == 'ارقام':
     num = ''
     for a in range(random.randint(5,15)):
       num += str(random.randint(1,9))
     r.set(f'{chat.id}:game:{Dev_Zaid}', num ,ex=600)
     await message.reply_text(f'الرقم ↢ ( {num} )', protect_content=True)
     return True
     
   if text == 'انمي':
     anim = random.choice(anime)
     r.set(f'{chat.id}:game:{Dev_Zaid}', anim['anime'] ,ex=600)
     await message.reply_photo(anim['photo'], caption='ايش اسم شخصية الانمي ؟')
     return True
   
   if text == 'صور':
     ph = random.choice(pics)
     r.set(f'{chat.id}:game:{Dev_Zaid}', ph['answer'] ,ex=600)
     if not ph['caption']:
       caption = 'وش الي فالصورة؟'
     else:
       caption = ph['caption']
     await message.reply_photo(ph['photo'], caption=caption)
     return True
   
   if text == 'كرة قدم' or text == 'كره قدم':
     ph = random.choice(football)
     r.set(f'{chat.id}:game:{Dev_Zaid}', ph['answer'] ,ex=600)
     if not ph['caption']:
       caption = 'وش اسم الاعب ؟'
     else:
       caption = ph['caption']
     await message.reply_photo(ph['photo'], caption=caption)
     return True
   
   if text == 'تشفير':
     ph = random.choice(tashfeer)
     r.set(f'{chat.id}:game:{Dev_Zaid}', ph['answer'] ,ex=600)
     if not ph['caption']:
       caption = 'فك التشفير ؟'
     else:
       caption = ph['caption']
     await message.reply_photo(ph['photo'], caption=caption)
     return True
   
   if text == 'تركيب':
     name = random.choice(tarkeeb)
     name1 = name
     name = re.sub("اناث", "ا ن ا ث", name)
     name = re.sub("ثيران", "ث ي ر ا ن", name)
     name = re.sub("دروس", "د ر و س", name)
     name = re.sub("فحص", "ف ح ص", name)
     name = re.sub("رجال", "ر ج ا ل", name)
     name = re.sub("انستا", "ا ن س ت ا", name)
     name = re.sub("ضغوط", "ض غ و ط", name)
     name = re.sub("صف", "ص ف", name)
     name = re.sub("رجب", "ر ج ب", name)
     name = re.sub("اسد", "ا س د", name)
     name = re.sub("وقع", "و ق ع", name)
     name = re.sub("ملك", "م ل ك", name)
     name = re.sub("فصل", "ف ص ل", name)
     name = re.sub("كلاب", "ك ل ا ب", name)
     name = re.sub("صقور", "ص ق و ر", name)
     name = re.sub("عقد", "ع ق د", name)
     name = re.sub("بحور", "ب ح و ر", name)
     name = re.sub("هاتف", "ه ا ت ف", name)
     name = re.sub("حدائق", "ح د ا ئ ق", name)
     name = re.sub("مسرح", "م س ر ح", name)
     name = re.sub("جرائم", "ج ر ا ئ م", name)
     name = re.sub("مدارس", "م د ا ر س", name)
     name = re.sub("منزل", "م ن ز ل", name)
     name = re.sub("كرسي", "ك ر س ي", name)
     name = re.sub("مناطق", "م ن ا ط ق", name)
     name = re.sub("بيوت", "ب ي و ت", name)
     name = re.sub("بنك", "ب ن ك", name)
     name = re.sub("علم", "ع ل م", name)
     name = re.sub("وظائف", "و ظ ا ئ ف", name)
     name = re.sub("طلاب", "ط ل ا ب", name)
     name = re.sub("مراحل", "م ر ا ح ل", name)
     name = re.sub("فنانين", "ف ن ا ن ي ن", name)
     name = re.sub("صواريخ", "ص و ا ر ي خ", name)
     r.set(f'{chat.id}:game:{Dev_Zaid}', name1,ex=600)
     await message.reply_text(f'ركب ↢ ( {name} )')
   
   if text == "سكب ديمون":
    if user.id in users_demon:
        del users_demon[user.id]
        return await message.reply_text("⇜ ابشر الغيت اللعبة")
    else:
        return await message.reply_text("⇜ مافيه لعبة ديمون شغالة")
        
   if text == 'حجره' or text == 'حجرة':
     return await message.reply_text('- اختار حجره / ورقة / مقص',reply_markup=InlineKeyboardMarkup (
     [
     [
       InlineKeyboardButton ('🪨', callback_data=f'RPS:rock++{user.id}'),
       InlineKeyboardButton ('📃', callback_data=f'RPS:paper++{user.id}'),
       InlineKeyboardButton ('✂️', callback_data=f'RPS:scissors++{user.id}'),
     ]
     ]
     ))
   
   if text == 'نرد':
     dice = await context.bot.send_dice(chat.id, emoji="🎲", reply_to_message_id=message.message_id,
     reply_markup=InlineKeyboardMarkup (
       [[
         InlineKeyboardButton ("🧚‍♀️",url=f"t.me/{channel}")
       ]]
     ))
     if dice.dice.value == 6:
        ra = 10
        if r.get(f'{user.id}:Floos'):
           get = int(r.get(f'{user.id}:Floos'))
           r.set(f'{user.id}:Floos',get+ra)
           floos = int(r.get(f'{user.id}:Floos'))
        else:
           floos = ra
           r.set(f'{user.id}:Floos',ra)
        return await message.reply_text(f'''
صح عليك فزت **[بالنرد]({dice.link})** ⁪⁬⁪⁬⁮⁪⁬⁪⁬⁮✔
💸فلوسك: `{floos}` ريال
☆
''', disable_web_page_preview=True)
     else:
        return await message.reply_text(f"{k} للأسف خسرت بالنرد")
       
   
   if text == 'ديمون':
     if user.id in users_demon:
        return await message.reply_text("⇜ في لعبة ديمون شغالة استخدم امر <code>سكب ديمون</code>")
     else:
        return await message.reply_text(f'''بوو 👻
انا ديمون 🧛🏻‍♀️ اقدر اعرف مين الشخصية الي فبالك !

- فكر بشخص واضغط بدء وجاوب على اسئلتي''',
     reply_markup=InlineKeyboardMarkup (
       [
       [
        InlineKeyboardButton ('بدء 🧛🏻‍♀️',callback_data=f'start_aki:{user.id}')
       ]
       ]
     ))

@Client.on_callback_query(filters.Regex('aki'))
async def akinatorHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
   query = update.callback_query
   if not query: return
   message = query
   user = update.effective_user
   if not user: return
   channel = r.get(f'{Dev_Zaid}:BotChannel') if r.get(f'{Dev_Zaid}:BotChannel') else 'scatteredda'
   if message.data == f'start_aki:{user.id}':
    rep = InlineKeyboardMarkup (
         [[InlineKeyboardButton ('🧚‍♀️', url=f't.me/{channel}')]]
       )
    message.edit_message_text("⇜ جاري بدء اللعبة...",reply_markup=rep)
    aki= akinator.Akinator()
    q = aki.start_game(language="ar")
    users_demon.update({user.id:[aki,q]})
    return message.edit_message_text(users_demon[user.id][1],
     reply_markup=InlineKeyboardMarkup (
       [
       [
         InlineKeyboardButton ('لا', callback_data=f'aki_c:n++{user.id}'),
         InlineKeyboardButton ('اي', callback_data=f'aki_c:y++{user.id}'),
       ],
       [
        InlineKeyboardButton ('ممكن',callback_data=f'aki_c:p++{user.id}')
       ]
       ]
     ))
   if message.data == f'aki_c:n++{user.id}':
    users_demon[user.id][1] = users_demon[user.id][0].answer("n")
    if users_demon[user.id][0].progression >= 65:
        users_demon[user.id][0].win()
        str_to_send = users_demon[user.id][0].first_guess
        print(str_to_send)
        message.message.delete()
        rep = InlineKeyboardMarkup (
         [[InlineKeyboardButton ('🧚‍♀️', url=f't.me/{channel}')]]
         )
        try: await context.bot.send_photo(message.message.chat.id, photo=str_to_send['absolute_picture_path'], caption=f"{str_to_send['name']} - {str_to_send['description']}",reply_markup=rep)
        except:         return message.edit_message_text(users_demon[user.id][1],
     reply_markup=InlineKeyboardMarkup (
       [
       [
         InlineKeyboardButton ('لا', callback_data=f'aki_c:n++{user.id}'),
         InlineKeyboardButton ('اي', callback_data=f'aki_c:y++{user.id}'),
       ],
       [
        InlineKeyboardButton ('ممكن',callback_data=f'aki_c:p++{user.id}')
       ]
       ]
     ))
   if message.data == f'aki_c:y++{user.id}':
    users_demon[user.id][1] = users_demon[user.id][0].answer("y")
    if users_demon[user.id][0].progression >= 65:
        users_demon[user.id][0].win()
        str_to_send = users_demon[user.id][0].first_guess
        print(str_to_send)
        message.message.delete()
        rep = InlineKeyboardMarkup (
         [[InlineKeyboardButton ('🧚‍♀️', url=f't.me/{channel}')]]
         )
        try: await context.bot.send_photo(message.message.chat.id, photo=str_to_send['absolute_picture_path'], caption=f"{str_to_send['name']} - {str_to_send['description']}",reply_markup=rep)
        except:         return message.edit_message_text(users_demon[user.id][1],
     reply_markup=InlineKeyboardMarkup (
       [
       [
         InlineKeyboardButton ('لا', callback_data=f'aki_c:n++{user.id}'),
         InlineKeyboardButton ('اي', callback_data=f'aki_c:y++{user.id}'),
       ],
       [
        InlineKeyboardButton ('ممكن',callback_data=f'aki_c:p++{user.id}')
       ]
       ]
     ))
   if message.data == f'aki_c:p++{user.id}':
    users_demon[user.id][1] = users_demon[user.id][0].answer("p")
    if users_demon[user.id][0].progression >= 65:
        users_demon[user.id][0].win()
        str_to_send = users_demon[user.id][0].first_guess
        print(str_to_send)
        message.message.delete()
        rep = InlineKeyboardMarkup (
         [[InlineKeyboardButton ('🧚‍♀️', url=f't.me/{channel}')]]
         )
        try: await context.bot.send_photo(message.message.chat.id, photo=str_to_send['absolute_picture_path'], caption=f"{str_to_send['name']} - {str_to_send['description']}",reply_markup=rep)
        except:         return message.edit_message_text(users_demon[user.id][1],
     reply_markup=InlineKeyboardMarkup (
       [
       [
         InlineKeyboardButton ('لا', callback_data=f'aki_c:n++{user.id}'),
         InlineKeyboardButton ('اي', callback_data=f'aki_c:y++{user.id}'),
       ],
       [
        InlineKeyboardButton ('ممكن',callback_data=f'aki_c:p++{user.id}')
       ]
       ]
     ))


def get_emoji_bank(count):
  if count == 1:
     return '🥇 ) '
  if count == 2:
     return '🥈 ) '
  if count == 3:
     return '🥉 ) '
  else:
     return f' {count}  ) '
     
     

def register(app):
    """Register games handlers."""
    from telegram.ext import MessageHandler, CallbackQueryHandler, filters
    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.GROUPS,
        gamesHandler
    ), group=16)
    app.add_handler(MessageHandler(
        filters.Dice() & filters.ChatType.GROUPS,
        diceFunc
    ), group=36)
    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.GROUPS,
        akinatorHandler
    ), group=37)
    try:
        app.add_handler(CallbackQueryHandler(akinator_callback, pattern=r'^aki'))
    except Exception:
        pass
