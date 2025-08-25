FROM python:3.8-slim

# ابتدا sources.list را به روز کنید
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i '/stretch-updates/d' /etc/apt/sources.list

WORKDIR /app

# ابتدا فقط apt-get update را جداگانه اجرا کنید
RUN apt-get update || apt-get update --allow-unauthenticated

# حالا بسته‌ها را نصب کنید
RUN apt-get install -y --no-install-recommends \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Java را از طریق alternatives نصب کنید
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-11-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# تنظیم Android SDK
ENV ANDROID_HOME /opt/android-sdk
RUN mkdir -p $ANDROID_HOME/cmdline-tools && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O tools.zip && \
    unzip -q tools.zip -d $ANDROID_HOME/cmdline-tools && \
    mv $ANDROID_HOME/cmdline-tools/cmdline-tools $ANDROID_HOME/cmdline-tools/latest && \
    rm tools.zip

ENV PATH $PATH:$ANDROID_HOME/cmdline-tools/latest/bin

# ایجاد فایل config برای جلوگیری از warning
RUN mkdir -p /root/.android && touch /root/.android/repositories.cfg

# نصب build-tools با timeout و retry
RUN yes | sdkmanager --licenses --sdk_root=$ANDROID_HOME && \
    sdkmanager "build-tools;33.0.0" --sdk_root=$ANDROID_HOME

# نصب Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن فایل‌های برنامه
COPY . .

CMD ["python", "main.py"]
