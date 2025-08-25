import os
import subprocess
import time
import base64
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes
from telegram.ext.filters import Document

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("فایل APK خود را (حداکثر 20 مگابایت) ارسال کنید.")

async def handle_apk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    current_time = time.time()

    if user_id in user_last_request and (current_time - user_last_request[user_id]) < COOLDOWN:
        remaining = int(COOLDOWN - (current_time - user_last_request[user_id]))
        await update.message.reply_text(f"لطفاً {remaining // 60} دقیقه و {remaining % 60} ثانیه صبر کنید.")
        return

    file = update.message.document
    if not file or not file.file_name.endswith(".apk"):
        await update.message.reply_text("لطفاً فقط فایل APK ارسال کنید!")
        return

    if file.file_size > 20 * 1024 * 1024:
        await update.message.reply_text("حجم فایل بیش از 20 مگابایت است!")
        return

    file_size_mb = file.file_size / 1024 / 1024
    await update.message.reply_text(f"فایل APK شما به حجم [{file_size_mb:.1f} مگابایت] دریافت شد\nوضعیت: در حال دریافت...")
    file_path = os.path.join(UPLOAD_DIR, file.file_name)
    await file.get_file().download_to_drive(file_path)

    await update.message.reply_text(f"فایل APK شما به حجم [{file_size_mb:.1f} مگابایت] دریافت شد\nوضعیت: در حال پردازش APK...")
    aligned_path = "aligned.apk"
    try:
        subprocess.run(["zipalign", "-v", "-p", "4", file_path, aligned_path], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        await update.message.reply_text("خطا: ابزار zipalign پیدا نشد یا خطایی رخ داد!")
        os.remove(file_path)
        return

    await update.message.reply_text(f"فایل APK شما به حجم [{file_size_mb:.1f} مگابایت] دریافت شد\nوضعیت: در حال انجام فرایند انکریپت...")
    output_path = os.path.join(OUTPUT_DIR, f"signed_{file.file_name}")
    try:
        with open("keystore.jks", "wb") as f:
            f.write(base64.b64decode(KEYSTORE_BASE64))
        subprocess.run([
            "apksigner", "sign",
            "--ks", "keystore.jks",
            "--ks-key-alias", KEYSTORE_ALIAS,
            "--ks-pass", f"pass:{KEYSTORE_PASS}",
            "--out", output_path,
            aligned_path
        ], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        await update.message.reply_text("خطا: ابزار apksigner پیدا نشد یا خطایی رخ داد!")
        os.remove(file_path)
        os.remove(aligned_path)
        return

    await update.message.reply_text(f"فایل APK شما به حجم [{file_size_mb:.1f} مگابایت] دریافت شد\nوضعیت: در حال امضای فایل...")
    await update.message.reply_text(f"فایل APK شما به حجم [{file_size_mb:.1f} مگابایت] دریافت شد\nوضعیت: در حال ارسال فایل...")
    await update.message.reply_document(open(output_path, "rb"), caption="فایل امضا شده با موفقیت!")
    await update.message.reply_text("پایان! 30 دقیقه دیگه می‌تونی فایل جدید بفرستی.")

    user_last_request[user_id] = current_time
    for file_to_remove in [file_path, aligned_path, output_path, "keystore.jks"]:
        if os.path.exists(file_to_remove):
            os.remove(file_to_remove)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(Document(), handle_apk))
    app.run_polling()  # برای تست محلی، بعد از دیپلوی به webhook برمی‌گردیم

if __name__ == "__main__":
    main()
