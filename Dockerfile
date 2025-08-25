FROM ubuntu:22.04

WORKDIR /app

# نصب وابستگی‌های سیستم
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    unzip \
    openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

# دانلود و نصب Android SDK
ENV ANDROID_HOME /opt/android-sdk
RUN mkdir -p $ANDROID_HOME && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O /tmp/tools.zip && \
    unzip -q /tmp/tools.zip -d $ANDROID_HOME && \
    mv $ANDROID_HOME/cmdline-tools $ANDROID_HOME/latest && \
    rm /tmp/tools.zip

# اضافه کردن به PATH
ENV PATH $PATH:$ANDROID_HOME/latest/bin

# قبول لیسانس‌ها و نصب build-tools
RUN yes | $ANDROID_HOME/latest/bin/sdkmanager --licenses && \
    $ANDROID_HOME/latest/bin/sdkmanager "build-tools;33.0.0"

# اضافه کردن build-tools به PATH
ENV PATH $PATH:$ANDROID_HOME/build-tools/33.0.0

# کپی فایل‌های پروژه
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ایجاد دایرکتوری‌های لازم
RUN mkdir -p uploads outputs

CMD ["python", "main.py"]
