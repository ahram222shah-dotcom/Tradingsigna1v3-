# Trading Signal V3

موبائل Trading Signal V3 project.

## شامل چیزیں
- `index.html` — موبائل HTML interface
- `main.py` — Android/Kivy app
- `buildozer.spec` — APK configuration
- `.github/workflows/build-apk.yml` — GitHub Actions سے APK build

## APK
GitHub میں تمام files upload کرنے کے بعد:
1. **Actions** کھولیں
2. **Build Android APK** workflow منتخب کریں
3. **Run workflow** دبائیں
4. Build مکمل ہونے پر **Artifacts** میں APK ملے گا

نوٹ: موجودہ signal engine demo prices استعمال کرتا ہے۔ حقیقی market data کے لیے authorized market-data API شامل کرنا ضروری ہے۔
یہ financial advice نہیں ہے اور کسی trade کی کامیابی کی ضمانت نہیں دیتا۔- name: Setup Android SDK
  uses: android-actions/setup-android@v3

- name: Install Android SDK components
  run: |
    yes | sdkmanager --licenses || true
    sdkmanager "platform-tools" "build-tools;35.0.0" "platforms;android-35"
    sdkmanager "cmdline-tools;latest"
