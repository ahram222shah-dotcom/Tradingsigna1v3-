[app]
title = Trading Signal V3
package.name = tradingsignalv3
package.domain = org.tradingsignal
source.dir = .
source.include_exts = py,kv,html,png,jpg,wav,mp3
version = 3.0
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 35
android.build_tools_version = 35.0.0
android.minapi = 23
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.permissions = INTERNET
