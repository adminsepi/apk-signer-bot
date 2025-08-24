import os
import subprocess
import time
import base64
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
COOLDOWN = 30 * 60
user_last_request = {}

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
    if not file.file_name.endswith(".apk"):
        await update.message.reply_text("لطفاً فقط فایل APK ارسال کنید!")
        return

    if file.file_size > 20 * 1024 * 1024:
        await update.message.reply_text("حجم فایل بیش از 20 مگابایت است!")
        return

    await update.message.reply_text(f"فایل APK شما به حجم {file.file_size / 1024 / 1024:.1f} مگابایت دریافت شد\nوضعیت: در حال انجام فرایند...")
    new_file = await file.get_file()
    file_path = os.path.join(UPLOAD_DIR, file.file_name)
    await new_file.download_to_drive(file_path)

    await update.message.reply_text(f"فایل APK شما به حجم {os.path.getsize(file_path) / 1024 / 1024:.1f} مگابایت دریافت شد\nوضعیت: در حال انجام فرایند انکریپت...")
    aligned_path = "aligned.apk"
    try:
        subprocess.run(["zipalign", "-v", "-p", "4", file_path, aligned_path], check=True)
    except subprocess.CalledProcessError:
        await update.message.reply_text("خطا در بهینه‌سازی فایل!")
        os.remove(file_path)
        return

    await update.message.reply_text(f"فایل APK شما به حجم {os.path.getsize(aligned_path) / 1024 / 1024:.1f} مگابایت دریافت شد\nوضعیت: در حال امضای فایل...")
    output_path = os.path.join(OUTPUT_DIR, f"signed_{file.file_name}")
    try:
        with open("keystore.jks", "wb") as f:
            f.write(base64.b64decode(os.getenv("KEYSTORE_BASE64")))
        subprocess.run([
            "apksigner", "sign",
            "--ks", "keystore.jks",
            "--ks-key-alias", os.getenv("KEYSTORE_ALIAS"),
            "--ks-pass", f"pass:{os.getenv('KEYSTORE_PASS')}",
            "--out", output_path,
            aligned_path
        ], check=True)
    except subprocess.CalledProcessError:
        await update.message.reply_text("خطا در امضای فایل!")
        os.remove(file_path)
        os.remove(aligned_path)
        return

    await update.message.reply_text("وضعیت: در حال ارسال ✅")
    with open(output_path, "rb") as signed_file:
        await update.message.reply_document(signed_file, caption="فایل امضا شده با موفقیت!")
    await update.message.reply_text("پایان! می‌توانید 30 دقیقه دیگر فایل جدیدی ارسال کنید.")

    user_last_request[user_id] = current_time
    os.remove(file_path)
    os.remove(aligned_path)
    os.remove(output_path)
    os.remove("keystore.jks")

def main():
    app = Application.builder().token(os.getenv("TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_apk))
    app.run_webhook(
        listen="0.0.0.0",
        port=8443,
        url_path=os.getenv("TOKEN"),
        webhook_url=f"https://your-render-url/{os.getenv('TOKEN')}"
    )

if __name__ == "__main__":
    main()
