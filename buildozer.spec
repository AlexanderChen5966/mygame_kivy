
[app]

title = MyZombieApp
package.name = myzombieapp
package.domain = org.example

source.dir = .
source.main = main.py

source.include_exts = py,png,jpg,mp3,wav,ogg,json,ttf,otf
source.include_patterns = assets/*, assets/**/*

version = 1.0

android.api = 30
android.minapi = 28
android.sdk = 30

orientation = portrait
fullscreen = 1

android.permissions = INTERNET

android.python3 = True
requirements = python3,kivy

android.copy_libs = 1
android.accept_sdk_license = True
