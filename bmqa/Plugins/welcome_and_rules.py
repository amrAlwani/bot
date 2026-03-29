"""
██████╗░██████╗░██████╗░
██╔══██╗╚════██╗██╔══██╗
██████╔╝░█████╔╝██║░░██║
██╔══██╗░╚═══██╗██║░░██║
██║░░██║██████╔╝██████╔╝
╚═╝░░╚═╝╚═════╝░╚═════╝░

[ = This plugin is converted to python-telegram-bot (async) = ]
"""

import logging
import re
import pytz
from datetime import datetime
from telegram import Update, ChatMember
from telegram.ext import Application, ContextTypes, filters, MessageHandler
from telegram.constants import ChatMemberStatus

logger = logging.getLogger(__name__)

default_welcome = """لا تُسِئ اللفظ وإن ضَاق عليك الرَّد

ɴᴀᴍᴇ ⌯ {الاسم}
ᴜѕᴇʀɴᴀᴍᴇ ⌯ {اليوزر}
𝖣𝖺𝗍𝖾 ⌯ {التاريخ}"""


async def welcome_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج الرسائل في المجموعات - للأوامر المتعلقة بالترحيب والقوانين"""
    
    if not update.message or not update.message.text:
        return
    
    try:
        message = update.message
        user = update.effective_user
        chat = update.effective_chat
        
        # استخراج البيانات من context
        from config import Dev_Zaid, r
        
        if not r:
            return
        
        # التحقق من تفعيل البوت في المجموعة
        if not r.get(f"{chat.id}:enable:{Dev_Zaid}"):
            return
        
        # التحقق من كتم صوت
        if r.get(f"{user.id}:mute:{chat.id}{Dev_Zaid}"):
            return
        
        text = message.text
        k = r.get(f"{Dev_Zaid}:botkey") or "⇜"
        
        # معالجة أمر إلغاء وضع الترحيب
        if text.strip() == "الغاء" and r.get(f"{chat.id}:setWelcome:{user.id}{Dev_Zaid}"):
            r.delete(f"{chat.id}:setWelcome:{user.id}{Dev_Zaid}")
            await message.reply_text(f"{k} ابشر لغيت وضع الترحيب")
            return
        
        # معالجة أمر إلغاء وضع القوانين
        if text.strip() == "الغاء" and r.get(f"{chat.id}:setRules:{user.id}{Dev_Zaid}"):
            r.delete(f"{chat.id}:setRules:{user.id}{Dev_Zaid}")
            await message.reply_text(f"{k} ابشر لغيت وضع القوانين")
            return
        
        # معالجة إدخال القوانين
        if r.get(f"{chat.id}:setRules:{user.id}{Dev_Zaid}"):
            # التحقق من الادمن/مدير
            try:
                member = await context.bot.get_chat_member(chat.id, user.id)
                if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                    r.set(f"{chat.id}:CustomRules:{Dev_Zaid}", text)
                    r.delete(f"{chat.id}:setRules:{user.id}{Dev_Zaid}")
                    await message.reply_text(f"{k} تم حطيتها")
                    return
            except Exception as e:
                logger.error(f"خطأ في التحقق من صلاحيات الادمن: {e}")
                return
        
        # معالجة إدخال الترحيب
        if r.get(f"{chat.id}:setWelcome:{user.id}{Dev_Zaid}"):
            # التحقق من الادمن/مدير
            try:
                member = await context.bot.get_chat_member(chat.id, user.id)
                if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                    r.set(f"{chat.id}:CustomWelcome:{Dev_Zaid}", text)
                    r.delete(f"{chat.id}:setWelcome:{user.id}{Dev_Zaid}")
                    await message.reply_text(f"{k} تم وسوينا الترحيب ياعيني")
                    return
            except Exception as e:
                logger.error(f"خطأ في التحقق من صلاحيات الادمن: {e}")
                return
        
        # أوامر إدارة الترحيب والقوانين
        if text.strip() == "مسح القوانين":
            try:
                member = await context.bot.get_chat_member(chat.id, user.id)
                if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                    r.delete(f"{chat.id}:CustomRules:{Dev_Zaid}")
                    await message.reply_text(f"{k} من عيوني مسحت القوانين")
                else:
                    await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
            except Exception as e:
                logger.error(f"خطأ في التحقق من صلاحيات الادمن: {e}")
                await message.reply_text(f"{k} خطأ في التحقق من الصلاحيات")
            return
        
        if text.strip() == "وضع قوانين":
            try:
                member = await context.bot.get_chat_member(chat.id, user.id)
                if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                    r.set(f"{chat.id}:setRules:{user.id}{Dev_Zaid}", 1)
                    await message.reply_text(f"{k} ارسل القوانين الحين")
                else:
                    await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
            except Exception as e:
                logger.error(f"خطأ في التحقق من صلاحيات الادمن: {e}")
                await message.reply_text(f"{k} خطأ في التحقق من الصلاحيات")
            return
        
        if text.strip() == "الترحيب":
            try:
                member = await context.bot.get_chat_member(chat.id, user.id)
                if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                    if not r.get(f"{chat.id}:CustomWelcome:{Dev_Zaid}"):
                        await message.reply_text(f"`{default_welcome}`", parse_mode="Markdown")
                    else:
                        welcome = r.get(f"{chat.id}:CustomWelcome:{Dev_Zaid}")
                        await message.reply_text(f"`{welcome}`", parse_mode="Markdown")
                else:
                    await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
            except Exception as e:
                logger.error(f"خطأ: {e}")
            return
        
        if text.strip() == "مسح الترحيب":
            try:
                member = await context.bot.get_chat_member(chat.id, user.id)
                if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                    r.delete(f"{chat.id}:CustomWelcome:{Dev_Zaid}")
                    await message.reply_text(f"{k} مسحت الترحيب")
                else:
                    await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
            except Exception as e:
                logger.error(f"خطأ: {e}")
            return
        
        if text.strip() in ["وضع الترحيب", "ضع الترحيب"]:
            try:
                member = await context.bot.get_chat_member(chat.id, user.id)
                if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                    r.set(f"{chat.id}:setWelcome:{user.id}{Dev_Zaid}", 1)
                    help_text = """⇜ تمام عيني  
⇜ ارسل رسالة الترحيب الحين

⇜ ملاحظة تقدر تضيف دوال للترحيب مثلا :
⇜ اظهار قوانين المجموعه  ⇠ {القوانين}  
⇜ اظهار اسم العضو ⇠ {الاسم}
⇜ اظهار اليوزر العضو ⇠ {اليوزر}
⇜ اظهار اسم المجموعه ⇠ {المجموعه} 
⇜ اظهار تاريخ دخول العضو ⇠ {التاريخ} 
⇜ اظهار وقت دخول العضو ⇠ {الوقت} 
☆"""
                    await message.reply_text(help_text)
                else:
                    await message.reply_text(f"{k} هذا الامر يخص ( المدير وفوق ) بس")
            except Exception as e:
                logger.error(f"خطأ: {e}")
            return
        
    except Exception as e:
        logger.error(f"خطأ في welcome_message_handler: {e}", exc_info=True)


async def welcome_new_members_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أحداث الأعضاء الجدد - ترحيب الأعضاء الجدد"""
    
    try:
        if not update.message:
            return
        
        message = update.message
        chat = update.effective_chat
        
        # استخراج البيانات من context
        from config import Dev_Zaid, r
        
        if not r:
            return
        
        # التحقق من تفعيل البوت في المجموعة
        if not r.get(f"{chat.id}:enable:{Dev_Zaid}"):
            return
        
        if not message.new_chat_members:
            return
        
        k = r.get(f"{Dev_Zaid}:botkey") or "⇜"
        channel = r.get(f"{Dev_Zaid}:BotChannel") or "scatteredda"
        
        if not r.get(f"{chat.id}:disableWelcome:{Dev_Zaid}"):
            if not r.get(f"{chat.id}:CustomWelcome:{Dev_Zaid}"):
                welcome_text = default_welcome
            else:
                welcome_text = r.get(f"{chat.id}:CustomWelcome:{Dev_Zaid}")
            
            for member in message.new_chat_members:
                if member.id != int(Dev_Zaid):  # لا نرحب بالبوت نفسه
                    # التحقق من التحقق المطلوب
                    if r.get(f"{chat.id}:enableVerify:{Dev_Zaid}"):
                        try:
                            member_obj = await context.bot.get_chat_member(chat.id, member.id)
                            if member_obj.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
                                continue  # تخطي الأعضاء الذين لم يتم التحقق منهم
                        except Exception as e:
                            logger.error(f"خطأ في التحقق من العضو: {e}")
                            continue
                    
                    # جمع بيانات الترحيب
                    title = chat.title or "المجموعة"
                    name = member.first_name or "الصديق"
                    username = f"@{member.username}" if member.username else f"@{channel}"
                    
                    # الحصول على الوقت والتاريخ
                    TIME_ZONE = "Asia/Riyadh"
                    ZONE = pytz.timezone(TIME_ZONE)
                    TIME = datetime.now(ZONE)
                    clock = TIME.strftime("%I:%M %p")
                    date_str = TIME.strftime("%d/%m/%Y")
                    
                    # الحصول على القوانين
                    if r.get(f"{chat.id}:CustomRules:{Dev_Zaid}"):
                        rules = r.get(f"{chat.id}:CustomRules:{Dev_Zaid}")
                    else:
                        rules = f"""{k} ممنوع نشر الروابط 
{k} ممنوع التكلم او نشر صور اباحيه 
{k} ممنوع اعاده توجيه 
{k} ممنوع العنصرية بكل انواعها 
{k} الرجاء احترام المدراء والادمنيه"""
                    
                    # استبدال الدوال
                    welcome_msg = (
                        welcome_text
                        .replace("{القوانين}", rules)
                        .replace("{الاسم}", name)
                        .replace("{المجموعه}", title)
                        .replace("{الوقت}", clock)
                        .replace("{التاريخ}", date_str)
                        .replace("{اليوزر}", username)
                    )
                    
                    # محاولة إرسال الصورة إن وجدت
                    try:
                        if not r.get(f"{chat.id}:disableWelcomep:{Dev_Zaid}") and member.photo:
                            profile_photo = await context.bot.get_user_profile_photos(member.id, limit=1)
                            if profile_photo.photos:
                                photo_file_id = profile_photo.photos[0][-1].file_id
                                await context.bot.send_photo(
                                    chat_id=chat.id,
                                    photo=photo_file_id,
                                    caption=welcome_msg
                                )
                                continue
                    except Exception as e:
                        logger.debug(f"لا يمكن إرسال الصورة: {e}")
                    
                    # إرسال الرسالة النصية
                    try:
                        await context.bot.send_message(
                            chat_id=chat.id,
                            text=welcome_msg,
                            disable_web_page_preview=True
                        )
                    except Exception as e:
                        logger.error(f"خطأ في إرسال رسالة الترحيب: {e}")
    
    except Exception as e:
        logger.error(f"خطأ في welcome_new_members_handler: {e}", exc_info=True)


# ==================== دالة تسجيل المعالجات ====================

def register_welcome_handlers(app: Application):
    """تسجيل معالجات الترحيب في التطبيق"""
    
    # معالج رسائل الترحيب والقوانين
    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.GROUPS,
        welcome_message_handler
    ))
    
    # معالج أحداث الأعضاء الجدد
    app.add_handler(MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        welcome_new_members_handler
    ))
    
    logger.info("✅ تم تسجيل معالجات الترحيب")
