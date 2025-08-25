FROM python:3.8-slim

WORKDIR /app

# ابتدا requirements را کپی و نصب کن
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# سپس بقیه موارد را نصب کن
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

ENV ANDROID_HOME /opt/android-sdk
RUN mkdir -p $ANDROID_HOME/cmdline-tools && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O tools.zip && \
    unzip -q tools.zip -d $ANDROID_HOME/cmdline-tools && \
    mv $ANDROID_HOME/cmdline-tools/cmdline-tools $ANDROID_HOME/cmdline-tools/latest && \
    rm tools.zip

ENV PATH $PATH:$ANDROID_HOME/cmdline-tools/latest/bin

RUN mkdir -p /root/.android && touch /root/.android/repositories.cfg
RUN yes | sdkmanager --licenses --sdk_root=$ANDROID_HOME && \
    sdkmanager "build-tools;33.0.0" --sdk_root=$ANDROID_HOME

COPY . .

CMD ["python", "main.py"]
