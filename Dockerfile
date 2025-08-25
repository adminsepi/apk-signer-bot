FROM python:3.9.7-slim-buster

WORKDIR /app

# نصب وابستگی‌های سیستم
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jre-headless \
    wget \
    unzip \
    zip \
    && rm -rf /var/lib/apt/lists/*

# دانلود و نصب Android SDK
ENV ANDROID_HOME /opt/android-sdk
RUN mkdir -p $ANDROID_HOME/cmdline-tools && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O tools.zip && \
    unzip -q tools.zip -d $ANDROID_HOME/cmdline-tools && \
    mv $ANDROID_HOME/cmdline-tools/cmdline-tools $ANDROID_HOME/cmdline-tools/latest && \
    rm tools.zip

# اضافه کردن Android SDK به PATH
ENV PATH $PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/build-tools/33.0.0

# نصب build-tools و پلتفرم‌ها
RUN yes | sdkmanager --sdk_root=$ANDROID_HOME "build-tools;33.0.0" "platforms;android-33"

# کپی فایل‌های مورد نیاز
COPY requirements.txt .

# نصب وابستگی‌های پایتون
RUN pip install --no-cache-dir -r requirements.txt

# کپی سورس کد
COPY . .

# ایجاد دایرکتوری‌های لازم
RUN mkdir -p uploads outputs

CMD ["python", "main.py"]
