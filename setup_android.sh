#!/usr/bin/env bash
set -euo pipefail

echo "=== Setup Android build tools (real) ==="

ROOT_DIR="$(pwd)"
SDK_DIR="$ROOT_DIR/android-sdk"
JDK_DIR="$ROOT_DIR/jdk"
TOOLS_ZIP_URL="https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip"
BUILD_TOOLS_VERSION="${BUILD_TOOLS_VERSION:-34.0.0}"

mkdir -p "$SDK_DIR" "$JDK_DIR"

# --- نصب JDK 17 (Temurin) ---
if [ ! -d "$JDK_DIR/jdk-17" ]; then
  echo "→ Download JDK 17"
  curl -L -o "$JDK_DIR/jdk.tar.gz" \
    "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.11+9/OpenJDK17U-jdk_x64_linux_hotspot_17.0.11_9.tar.gz"
  tar -xzf "$JDK_DIR/jdk.tar.gz" -C "$JDK_DIR"
  rm -f "$JDK_DIR/jdk.tar.gz"
  mv "$JDK_DIR"/jdk-17.* "$JDK_DIR/jdk-17"
fi

export JAVA_HOME="$JDK_DIR/jdk-17"
export PATH="$JAVA_HOME/bin:$PATH"

# --- نصب cmdline-tools ---
if [ ! -d "$SDK_DIR/cmdline-tools/latest" ]; then
  echo "→ Download cmdline-tools"
  mkdir -p "$SDK_DIR/cmdline-tools"
  curl -L -o "$SDK_DIR/tools.zip" "$TOOLS_ZIP_URL"
  unzip -q "$SDK_DIR/tools.zip" -d "$SDK_DIR/cmdline-tools"
  rm -f "$SDK_DIR/tools.zip"
  mv "$SDK_DIR/cmdline-tools/cmdline-tools" "$SDK_DIR/cmdline-tools/latest" || true
fi

export ANDROID_HOME="$SDK_DIR"
export ANDROID_SDK_ROOT="$SDK_DIR"
export PATH="$SDK_DIR/cmdline-tools/latest/bin:$PATH"

# --- نصب build-tools رسمی (zipalign/apksigner) ---
echo "→ Accept licenses & install build-tools;$BUILD_TOOLS_VERSION"
yes | sdkmanager --sdk_root="$SDK_DIR" "build-tools;${BUILD_TOOLS_VERSION}" >/dev/null

export PATH="$SDK_DIR/build-tools/${BUILD_TOOLS_VERSION}:$PATH"

# --- بررسی ---
echo "→ Check tools"
command -v zipalign >/dev/null || { echo "zipalign not found"; exit 1; }
command -v apksigner >/dev/null || { echo "apksigner not found"; exit 1; }

zipalign -h >/dev/null || true
apksigner >/dev/null || true

echo "✅ Android build-tools ${BUILD_TOOLS_VERSION} ready."
