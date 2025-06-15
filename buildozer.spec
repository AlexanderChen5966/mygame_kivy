[app]

title = MyZombieApp
package.name = myzombieapp
package.domain = org.example

source.dir = .
source.main = main.py

source.include_exts = py,png,jpg,mp3,wav,ogg,json,ttf,otf
source.include_patterns = assets/*, assets/**/*

version = 1.0

orientation = portrait
fullscreen = 1

android.permissions = INTERNET

android.api = 30
android.minapi = 28
android.ndk = 25b

android.python3 = True
requirements = python3,kivy

p4a.url = https://github.com/kivy/python-for-android.git
p4a.branch = develop

android.accept_sdk_license = True

# 避免把標準庫測試檔打包進去
android.exclude_tests = true
