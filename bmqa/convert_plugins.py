#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكريبت تحويل Plugins من Pyrogram إلى python-telegram-bot
"""

import os
import re

def convert_plugin(file_path):
    """تحويل ملف plugin واحد"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    print(f"🔄 جاري تحويل {os.path.basename(file_path)}...")
    
    # 1. تحويل الـ Imports
    content = re.sub(
        r'from pyrogram import \*\nfrom pyrogram\.enums import \*\nfrom pyrogram\.types import \*',
        'from telegram import Update\nfrom telegram.ext import ContextTypes, MessageHandler, filters',
        content
    )
    
    # الاستيراد الفردي
    content = re.sub(
        r'from pyrogram import .*?\n',
        '',
        content
    )
    content = re.sub(
        r'from pyrogram\.enums import .*?\n',
        '',
        content
    )
    content = re.sub(
        r'from pyrogram\.types import .*?\n',
        '',
        content
    )
    
    # 2. إزالة Threads
    content = re.sub(
        r'from threading import Thread\n',
        '',
        content
    )
    
    # 3. تحويل المعالجات - استخراج الدوال القديمة
    # النمط: @Client.on_message(...) def handler(c,m):
    # التحويل: async def handler_async(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # البحث عن جميع decorators ويحويلها
    content = re.sub(
        r'@Client\.on_message\((.*?)\)\ndef\s+(\w+)\s*\(\s*c\s*,\s*m\s*\):',
        r'async def \2_async(update: Update, context: ContextTypes.DEFAULT_TYPE):',
        content,
        flags=re.DOTALL
    )
    
    # 4. تحويل الرد على الرسائل
    # m.reply(...) → await message.reply_text(...)
    content = re.sub(
        r'm\.reply\s*\(',
        'await message.reply_text(',
        content
    )
    
    # m.reply_photo(...) → await message.reply_photo(...)
    content = re.sub(
        r'm\.reply_photo\s*\(',
        'await message.reply_photo(',
        content
    )
    
    # m.reply_video(...) → await message.reply_video(...)
    content = re.sub(
        r'm\.reply_video\s*\(',
        'await message.reply_video(',
        content
    )
    
    # m.reply_document(...) → await message.reply_document(...)
    content = re.sub(
        r'm\.reply_document\s*\(',
        'await message.reply_document(',
        content
    )
    
    # 5. تحويل المتغيرات
    # m.from_user.id → user.id (بعد استخراج user من update)
    # m.chat.id → chat.id (بعد استخراج chat من update)
    # m.text → message.text
    # m.from_user → user
    # m.chat → chat
    
    content = re.sub(
        r'm\.from_user\.id',
        'user.id',
        content
    )
    
    content = re.sub(
        r'm\.from_user\.mention',
        'user.mention_html()',
        content
    )
    
    content = re.sub(
        r'm\.chat\.id',
        'chat.id',
        content
    )
    
    content = re.sub(
        r'm\.from_user',
        'user',
        content
    )
    
    content = re.sub(
        r'm\.chat',
        'chat',
        content
    )
    
    content = re.sub(
        r'm\.text',
        'message.text',
        content
    )
    
    # m. → message. (للمتغيرات الأخرى)
    content = re.sub(
        r'\bm\.(\w+)',
        r'message.\1',
        content
    )
    
    # 6. استخراج update و context في بداية الدوال
    # البحث عن def handler_async وإضافة الأسطر
    content = re.sub(
        r'(async def \w+_async\(update: Update, context: ContextTypes\.DEFAULT_TYPE\):)\n',
        r'\1\n    if not update.message:\n        return\n    message = update.message\n    user = update.effective_user\n    chat = update.effective_chat\n',
        content
    )
    
    # 7. تحويل Threads → async مباشر
    # Thread(target=func, args=(c,m,k,channel)).start() → await func(c, m, k, channel)
    content = re.sub(
        r'Thread\s*\(\s*target\s*=\s*(\w+)\s*,\s*args\s*=\s*\((.*?)\)\s*\)\.start\(\)',
        r'await \1(\2)',
        content,
        flags=re.DOTALL
    )
    
    # 8. تحويل time.sleep إلى asyncio.sleep
    content = re.sub(
        r'time\.sleep\s*\(',
        'await asyncio.sleep(',
        content
    )
    
    # 9. إضافة import asyncio إن لم يكن موجودًا
    if 'await asyncio.sleep' in content and 'import asyncio' not in content:
        # أضف بعد الـ imports الأخرى
        import_section = content.split('\nfrom config import')[0]
        content = import_section + '\nimport asyncio\nfrom config import' + content.split('\nfrom config import')[1]
    
    # 10. إضافة دالة register في النهاية
    if 'def register(app:' not in content:
        file_name = os.path.basename(file_path).replace('.py', '')
        register_func = f"""

# ==================== تسجيل المعالجات ====================

def register(app):
    \"\"\"تسجيل معالجات {file_name} في التطبيق\"\"\"
    
    app.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.GROUPS,
        {[name for name in re.findall(r'async def (\w+)_async', content)][0]}_async if [name for name in re.findall(r'async def (\w+)_async', content)] else None
    ))
    
    import logging
    logging.getLogger(__name__).info(f"✅ تم تحميل {file_name} plugin")
"""
        content += register_func
    
    # تحقق من التغييرات
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ تم تحويل {os.path.basename(file_path)}")
        return True
    else:
        print(f"⚠️ لم تحدث تغييرات في {os.path.basename(file_path)}")
        return False

def main():
    """تحويل جميع الـ Plugins"""
    
    plugins_dir = os.path.dirname(os.path.abspath(__file__)) + '/Plugins'
    
    if not os.path.exists(plugins_dir):
        print(f"❌ المجلد {plugins_dir} غير موجود")
        return
    
    py_files = [f for f in os.listdir(plugins_dir) if f.endswith('.py') and not f.startswith('__')]
    
    print(f"\n{'='*70}")
    print(f"🔄 جاري تحويل {len(py_files)} ملف...")
    print(f"{'='*70}\n")
    
    converted = 0
    for py_file in py_files:
        file_path = os.path.join(plugins_dir, py_file)
        try:
            if convert_plugin(file_path):
                converted += 1
        except Exception as e:
            print(f"❌ خطأ في تحويل {py_file}: {e}")
    
    print(f"\n{'='*70}")
    print(f"✅ تم تحويل {converted}/{len(py_files)} ملف بنجاح")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
