FROM python:3.8-slim

WORKDIR /app

# اول apt-get update را جداگانه اجرا کنید
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jdk-headless \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# تنظیم Android SDK
ENV ANDROID_HOME /opt/android-sdk
RUN mkdir -p $ANDROID_HOME/cmdline-tools && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O tools.zip && \
    unzip tools.zip -d $ANDROID_HOME/cmdline-tools && \
    mv $ANDROID_HOME/cmdline-tools/cmdline-tools $ANDROID_HOME/cmdline-tools/latest && \
    rm tools.zip

ENV PATH $PATH:$ANDROID_HOME/cmdline-tools/latest/bin

# قبول licenses و نصب build-tools
RUN mkdir -p /root/.android && touch /root/.android/repositories.cfg
RUN yes | sdkmanager --licenses && sdkmanager "build-tools;33.0.0"

# نصب Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن فایل‌های برنامه
COPY . .

CMD ["python", "main.py"]
