# -*- coding: utf-8 -*-
# app.py - Telegram APK signer bot (Python 3.9.7 compatible)

import os
import time
import base64
import logging
import tempfile
import shutil
import subprocess
from typing import Optional

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

# =========[ تنظیمات ثابت – طبق خواسته شما داخل سورس ]=========
BOT_TOKEN = "7569529571:AAFxyFyv-vcosc-VpdkwUqA-pR-uiNHHZkE"
KEYSTORE_BASE64 = """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"""
KEYSTORE_PASS = "android123"
KEYSTORE_ALIAS = "alias_name"

# =========[ تنظیمات دیگر ]=========
MAX_FILE_MB = 20
COOLDOWN_SEC = 30 * 60  # 30 دقیقه

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("apk-signer-bot")

user_last_request = {}

# ---------------- UI ----------------
def main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📂 ارسال فایل APK", callback_data="upload_apk")],
        [InlineKeyboardButton("ℹ️ راهنما", callback_data="help")],
        [InlineKeyboardButton("🧪 تست ابزارها", callback_data="check_tools")],
        [InlineKeyboardButton("❌ خروج", callback_data="exit")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"سلام {user.first_name} 👋\nبه ربات امضاکننده APK خوش اومدی.\nاز منو یکی رو انتخاب کن:",
        reply_markup=main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "upload_apk":
        await query.edit_message_text(f"📂 لطفاً فایل APK خود را ارسال کنید (≤ {MAX_FILE_MB}MB).")
    elif query.data == "help":
        await query.edit_message_text(
            "راهنما:\n"
            f"• فایل APK (≤ {MAX_FILE_MB}MB) بفرست.\n"
            "• ربات zipalign و با keystore شما امضا می‌کند.\n"
            f"• محدودیت ارسال: هر {COOLDOWN_SEC//60} دقیقه یک‌بار.\n",
            reply_markup=main_menu()
        )
    elif query.data == "check_tools":
        ok, msg = await check_tools_message()
        await query.edit_message_text(msg, reply_markup=main_menu())
    elif query.data == "exit":
        await query.edit_message_text("❌ منو بسته شد.")

# --------------- ابزارها ---------------
def which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)

def ensure_android_tools_available() -> None:
    if not which("zipalign"):
        raise FileNotFoundError("zipalign در PATH یافت نشد.")
    if not which("apksigner"):
        raise FileNotFoundError("apksigner در PATH یافت نشد.")

async def check_tools_message():
    try:
        ensure_android_tools_available()
        # sanity run
        subprocess.run(["zipalign", "-h"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        subprocess.run(["apksigner"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        # keystore decode test
        tmp = tempfile.mkdtemp(prefix="ks_")
        try:
            write_keystore_from_base64(os.path.join(tmp, "keystore.jks"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        return True, "✅ ابزارها و keystore آماده‌اند (zipalign/apksigner/keystore OK)."
    except Exception as e:
        return False, f"❌ مشکل در آماده‌سازی: {e}"

def write_keystore_from_base64(dest_path: str) -> None:
    try:
        raw = base64.b64decode(KEYSTORE_BASE64)
        with open(dest_path, "wb") as f:
            f.write(raw)
    except Exception as e:
        raise RuntimeError(f"خطا در ساخت keystore از base64: {e}")

def run_cmd(args, cwd=None) -> None:
    p = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if p.returncode != 0:
        out = p.stdout or ""
        raise RuntimeError(f"خطا در اجرای {' '.join(args)}:\n{out[:4000]}")

# --------------- هندل APK ---------------
async def handle_apk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # محدودیت زمانی هر کاربر
    user_id = update.effective_user.id
    now = time.time()
    last = user_last_request.get(user_id)
    if last and now - last < COOLDOWN_SEC:
        remain = int(COOLDOWN_SEC - (now - last))
        await update.message.reply_text(f"⏳ لطفاً {remain//60} دقیقه و {remain%60} ثانیه دیگر تلاش کنید.")
        return

    doc = update.message.document
    if not doc or not doc.file_name.lower().endswith(".apk"):
        await update.message.reply_text("⚠️ لطفاً فقط فایل‌های APK ارسال کنید.")
        return

    if doc.file_size and doc.file_size > MAX_FILE_MB * 1024 * 1024:
        await update.message.reply_text(f"⚠️ حجم فایل بیش از {MAX_FILE_MB}MB است.")
        return

    size_mb = (doc.file_size or 0) / (1024 * 1024)
    status = await update.message.reply_text(
        f"فایل دریافت شد: [{size_mb:.1f} MB]\n"
        "وضعیت: در حال دریافت فایل..."
    )

    tmpdir = tempfile.mkdtemp(prefix="apk_")
    keystore_path = os.path.join(tmpdir, "keystore.jks")
    input_apk = os.path.join(tmpdir, doc.file_name)
    aligned_apk = os.path.join(tmpdir, "aligned.apk")
    signed_apk = os.path.join(tmpdir, f"signed_{doc.file_name}")

    try:
        ensure_android_tools_available()

        tg_file = await doc.get_file()
        await tg_file.download_to_drive(input_apk)

        await status.edit_text(f"فایل دریافت شد: [{size_mb:.1f} MB]\nوضعیت: ساخت keystore...")
        write_keystore_from_base64(keystore_path)

        await status.edit_text(f"فایل دریافت شد: [{size_mb:.1f} MB]\nوضعیت: zipalign...")
        run_cmd(["zipalign", "-v", "-p", "4", input_apk, aligned_apk])

        await status.edit_text(f"فایل دریافت شد: [{size_mb:.1f} MB]\nوضعیت: امضا با apksigner...")
        run_cmd([
            "apksigner", "sign",
            "--ks", keystore_path,
            "--ks-key-alias", KEYSTORE_ALIAS,
            "--ks-pass", f"pass:{KEYSTORE_PASS}",
            "--out", signed_apk,
            aligned_apk
        ])

        # (اختیاری) تأیید امضا
        verify = subprocess.run(
            ["apksigner", "verify", "--verbose", "--print-certs", signed_apk],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        logger.info("apksigner verify output:\n%s", verify.stdout)

        await status.edit_text("وضعیت: ارسال فایل امضا شده...")
        with open(signed_apk, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=f"signed_{doc.file_name}",
                caption="✅ فایل با موفقیت zipalign و امضا شد."
            )

        user_last_request[user_id] = now
        await status.edit_text(f"✅ انجام شد! می‌تونی بعد از {COOLDOWN_SEC//60} دقیقه دوباره فایل بفرستی.")

    except Exception as e:
        logger.exception("Signing error")
        try:
            await status.edit_text(f"❌ خطا: {e}")
        except Exception:
            await update.message.reply_text(f"❌ خطا: {e}")
    finally:
        try:
            shutil.rmtree(tmpdir, ignore_errors=True)
        except Exception:
            pass

# --------------- main ---------------
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", cmd_start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.Document.FileExtension("apk"), handle_apk))
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger.info("🚀 Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
