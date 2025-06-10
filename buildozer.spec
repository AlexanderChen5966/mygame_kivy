[app]
# 應用程式名稱
title = MyKivyGame

# 套件名稱與網域
package.name = mykivygame
package.domain = org.example

# 程式原始碼目錄
source.dir = .

# Python 套件需求
requirements = python3,kivy

# 版號，一定要設定
version = 0.1.0

# 方向與全螢幕設定
orientation = portrait
fullscreen = 0

# (以下是既有的 buildozer 參數，請保持)
[buildozer]
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.private_storage = True
