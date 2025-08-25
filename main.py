import os
import subprocess
import time
import base64
import logging
import shutil
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# پیکربندی
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
COOLDOWN = 30 * 60
user_last_request = {}
TOKEN = "7569529571:AAFxyFyv-vcosc-VpdkwUqA-pR-uiNHHZkE"
KEYSTORE_PASS = "mysecretpassword"
KEYSTORE_ALIAS = "alias_name"
KEYSTORE_BASE64 = "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"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# مسیر ابزارها
ZIPALIGN_PATH = "./android-sdk/build-tools/33.0.0/zipalign"
APKSIGNER_PATH = "./android-sdk/build-tools/33.0.0/apksigner"

def check_tools():
    """بررسی وجود ابزارهای لازم"""
    if not os.path.exists(ZIPALIGN_PATH):
        logger.error(f"ابزار zipalign یافت نشد: {ZIPALIGN_PATH}")
        return False
    
    if not os.path.exists(APKSIGNER_PATH):
        logger.error(f"ابزار apksigner یافت نشد: {APKSIGNER_PATH}")
        return False
    
    # دادن مجوز اجرا
    os.chmod(ZIPALIGN_PATH, 0o755)
    os.chmod(APKSIGNER_PATH, 0o755)
    
    logger.info("همه ابزارها با موفقیت یافت شدند")
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 ربات امضا و انکریپت APK\n\nفایل APK خود را (حداکثر 20 مگابایت) ارسال کنید.")

async def handle_apk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    current_time = time.time()

    if user_id in user_last_request and (current_time - user_last_request[user_id]) < COOLDOWN:
        remaining = int(COOLDOWN - (current_time - user_last_request[user_id]))
        minutes = remaining // 60
        seconds = remaining % 60
        await update.message.reply_text(f"⏳ لطفاً {minutes} دقیقه و {seconds} ثانیه صبر کنید.")
        return

    file = update.message.document
    if not file or not file.file_name.lower().endswith(".apk"):
        await update.message.reply_text("❌ لطفاً فقط فایل APK ارسال کنید!")
        return

    if file.file_size > 20 * 1024 * 1024:
        await update.message.reply_text("❌ حجم فایل بیش از 20 مگابایت است!")
        return

    file_size_mb = file.file_size / 1024 / 1024
    status_message = await update.message.reply_text(f"📥 فایل APK شما به حجم [{file_size_mb:.1f} مگابایت] دریافت شد\n🔄 وضعیت: در حال دریافت...")

    file_path = None
    aligned_path = None
    output_path = None

    try:
        # بررسی ابزارها
        if not check_tools():
            await status_message.edit_text("❌ ابزارهای لازم یافت نشد. لطفاً بعداً تلاش کنید.")
            return

        # دانلود فایل
        file_path = os.path.join(UPLOAD_DIR, file.file_name)
        file_obj = await file.get_file()
        await file_obj.download_to_drive(file_path)

        await status_message.edit_text(f"📥 فایل APK شما به حجم [{file_size_mb:.1f} مگابایت] دریافت شد\n🔄 وضعیت: در حال پردازش APK...")

        # پردازش APK
        aligned_path = os.path.join(UPLOAD_DIR, "aligned.apk")
        
        # اجرای zipalign
        try:
            subprocess.run([ZIPALIGN_PATH, "-v", "-p", "4", file_path, aligned_path], check=True, timeout=300)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            await status_message.edit_text("❌ خطا در پردازش فایل!")
            logger.error(f"Zipalign error: {e}")
            return

        await status_message.edit_text(f"📥 فایل APK شما به حجم [{file_size_mb:.1f} مگابایت] دریافت شد\n🔒 وضعیت: در حال انجام فرایند انکریپت...")

        # ایجاد keystore
        with open("keystore.jks", "wb") as f:
            f.write(base64.b64decode(KEYSTORE_BASE64))

        # امضای فایل
        output_filename = f"signed_{file.file_name}"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        try:
            subprocess.run([
                APKSIGNER_PATH, "sign",
                "--ks", "keystore.jks",
                "--ks-key-alias", KEYSTORE_ALIAS,
                "--ks-pass", f"pass:{KEYSTORE_PASS}",
                "--out", output_path,
                aligned_path
            ], check=True, timeout=300)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            await status_message.edit_text("❌ خطا در امضای فایل!")
            logger.error(f"Apksigner error: {e}")
            return

        await status_message.edit_text(f"📥 فایل APK شما به حجم [{file_size_mb:.1f} مگابایت] دریافت شد\n✅ وضعیت: در حال ارسال فایل...")

        # ارسال فایل امضا شده
        output_size_mb = os.path.getsize(output_path) / 1024 / 1024
        await update.message.reply_document(
            document=open(output_path, "rb"),
            caption=f"✅ فایل امضا شده با موفقیت!\n📦 حجم فایل خروجی: {output_size_mb:.1f} مگابایت"
        )
        
        await status_message.edit_text(f"📥 فایل APK شما به حجم [{file_size_mb:.1f} مگابایت] دریافت شد\n✅ وضعیت: پایان!\n\n🎉 شما می‌توانید 30 دقیقه دیگر فایل جدیدی ارسال کنید.")

        user_last_request[user_id] = current_time

    except Exception as e:
        logger.error(f"Error processing APK: {e}")
        await status_message.edit_text("❌ خطایی در پردازش فایل رخ داد!")
        
    finally:
        # پاکسازی فایل‌های موقت
        for file_to_remove in [file_path, aligned_path, output_path, "keystore.jks"]:
            if file_to_remove and os.path.exists(file_to_remove):
                try:
                    os.remove(file_to_remove)
                except:
                    pass

def main():
    # بررسی نهایی ابزارها
    if check_tools():
        logger.info("همه ابزارها آماده هستند!")
    else:
        logger.warning("برخی ابزارها یافت نشدند!")
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.FileExtension("apk"), handle_apk))
    
    logger.info("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
