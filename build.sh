#!/bin/bash
echo "=== نصب ابزارهای لازم برای ربات امضا APK ==="

# آپدیت سیستم و نصب وابستگی‌های پایه
echo "📦 در حال آپدیت سیستم و نصب وابستگی‌ها..."
apt-get update
apt-get install -y wget unzip openjdk-11-jdk

# ایجاد دایرکتوری Android SDK
echo "📁 ایجاد دایرکتوری Android SDK..."
mkdir -p /opt/android-sdk
cd /opt/android-sdk

# دانلود Android Command Line Tools
echo "⬇️ دانلود Android Command Line Tools..."
wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O tools.zip

# اکسترکت کردن فایل‌ها
echo "📦 اکسترکت کردن فایل‌ها..."
unzip -q tools.zip
rm tools.zip

# جابجایی فایل‌ها به مسیر صحیح
echo "🔧 تنظیم مسیرها..."
mv cmdline-tools latest
mkdir -p cmdline-tools
mv latest cmdline-tools/

# تنظیم متغیرهای محیطی
echo "🌐 تنظیم متغیرهای محیطی..."
export ANDROID_HOME=/opt/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin

# قبول لیسانس‌ها
echo "📝 قبول لیسانس‌های Android..."
yes | sdkmanager --licenses

# نصب Build Tools
echo "🛠️ نصب Build Tools 33.0.0..."
sdkmanager "build-tools;33.0.0"

# اضافه کردن به PATH
echo "🔧 اضافه کردن Build Tools به PATH..."
export PATH=$PATH:$ANDROID_HOME/build-tools/33.0.0

# بررسی نصب موفقیت‌آمیز
echo "✅ بررسی نصب ابزارها..."
if [ -f "$ANDROID_HOME/build-tools/33.0.0/zipalign" ]; then
    echo "🎉 zipalign با موفقیت نصب شد!"
else
    echo "❌ خطا در نصب zipalign!"
    exit 1
fi

if [ -f "$ANDROID_HOME/build-tools/33.0.0/apksigner" ]; then
    echo "🎉 apksigner با موفقیت نصب شد!"
else
    echo "❌ خطا در نصب apksigner!"
    exit 1
fi

echo "🎊 تمام ابزارها با موفقیت نصب شدند!"
