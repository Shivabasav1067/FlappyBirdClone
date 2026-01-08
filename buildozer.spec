[app]
title = Flappy Bird Clone
package.name = flappybird
package.domain = org.shivu

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

version = 0.1

requirements = python3,kivy

orientation = portrait

fullscreen = 1


[buildozer]
log_level = 2

[app.android]
bootstrap = sdl2
android.api = 31
android.minapi = 21

android.archs = arm64-v8a,armeabi-v7a

android.permissions = INTERNET

android.allow_backup = True
