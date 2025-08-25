#!/bin/bash
echo "=== نصب ابزارهای لازم برای ربات امضا APK ==="

# ایجاد دایرکتوری‌های لازم
echo "📁 ایجاد دایرکتوری‌های لازم..."
mkdir -p /opt/android-sdk
cd /opt/android-sdk

# دانلود Command Line Tools از گوگل
echo "⬇️ دانلود Command Line Tools..."
wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O tools.zip
unzip -q tools.zip
rm tools.zip
mv cmdline-tools latest

# نصب build-tools و zipalign
echo "⬇️ نصب build-tools و zipalign..."
yes | ./latest/bin/sdkmanager --sdk_root=/opt/android-sdk "build-tools;33.0.0"

# دانلود apksigner (از Android SDK)
echo "📦 تنظیم apksigner..."
# apksigner معمولاً توی build-tools هست، پس مسیر رو چک می‌کنیم
if [ -f "/opt/android-sdk/build-tools/33.0.0/apksigner" ]; then
    chmod +x /opt/android-sdk/build-tools/33.0.0/apksigner
    echo "🎉 apksigner با موفقیت پیدا شد!"
else
    echo "❌ apksigner پیدا نشد، تلاش برای دانلود دستی..."
    wget -q https://raw.githubusercontent.com/aosp-mirror/platform_build/master/tools/apksigner -O /opt/android-sdk/build-tools/33.0.0/apksigner
    chmod +x /opt/android-sdk/build-tools/33.0.0/apksigner
    echo "🎉 apksigner با موفقیت دانلود شد!"
fi

# تنظیم متغیرهای محیطی
echo "🌐 تنظیم متغیرهای محیطی..."
export ANDROID_HOME=/opt/android-sdk
export PATH=$PATH:$ANDROID_HOME/latest/bin:$ANDROID_HOME/build-tools/33.0.0

# بررسی نصب موفقیت‌آمیز
echo "✅ بررسی نصب ابزارها..."
if [ -f "$ANDROID_HOME/build-tools/33.0.0/zipalign" ]; then
    echo "🎉 zipalign با موفقیت نصب شد!"
    if [ -x "$ANDROID_HOME/build-tools/33.0.0/zipalign" ]; then
        echo "✅ zipalign قابل اجرا است"
    else
        chmod +x "$ANDROID_HOME/build-tools/33.0.0/zipalign"
        echo "🔧 مجوزهای اجرا به zipalign داده شد"
    fi
else
    echo "❌ خطا در نصب zipalign!"
    exit 1
fi

if [ -f "$ANDROID_HOME/build-tools/33.0.0/apksigner" ]; then
    echo "🎉 apksigner با موفقیت نصب شد!"
    if [ -x "$ANDROID_HOME/build-tools/33.0.0/apksigner" ]; then
        echo "✅ apksigner قابل اجرا است"
    else
        chmod +x "$ANDROID_HOME/build-tools/33.0.0/apksigner"
        echo "🔧 مجوزهای اجرا به apksigner داده شد"
    fi
else
    echo "❌ خطا در نصب apksigner!"
    exit 1
fi

echo "🎊 تمام ابزارها با موفقیت نصب شدند!"
echo "📁 مسیر نصب: $ANDROID_HOME"
