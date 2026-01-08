[app]
title = FlappyBird
package.name = flappybird
package.domain = org.shivu
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 1

[buildozer]
log_level = 2

[android]
android.api = 31
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a,armeabi-v7a
