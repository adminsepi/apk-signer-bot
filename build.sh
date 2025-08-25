#!/bin/bash
echo "Installing Android SDK tools..."

# ایجاد دایرکتوری‌های لازم
mkdir -p /opt/android-sdk/cmdline-tools

# دانلود و نصب Android SDK
wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O tools.zip
unzip -q tools.zip -d /opt/android-sdk/cmdline-tools
mv /opt/android-sdk/cmdline-tools/cmdline-tools /opt/android-sdk/cmdline-tools/latest
rm tools.zip

# اضافه کردن به PATH
export PATH=$PATH:/opt/android-sdk/cmdline-tools/latest/bin

# نصب build-tools
echo "y" | /opt/android-sdk/cmdline-tools/latest/bin/sdkmanager --sdk_root=/opt/android-sdk "build-tools;33.0.0"

echo "Android SDK tools installed successfully!"
