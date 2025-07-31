[buildozer]
warn_on_root = 1
log_level = 2
log_file = buildozer.log

[app]
title = LoginApp
package.name = ghaith
package.domain = org.kivy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,requests
orientation = portrait
fullscreen = 1
icon.filename = assets/icon.png
entrypoint = main.py
presplash.filename = assets/splash.png

[android]
android.api = 30
android.minapi = 21
android.sdk = 30
android.build_tools_version = 30.0.3
android.ndk = 25b
android.sdk_tools = 6858069
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.release = True
android.debug = False
android.arch = armeabi-v7a,arm64-v8a
