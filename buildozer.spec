[app]

title = AI Dungeon RPG
package.name = aidungeon
package.domain = org.tyler

source.dir = .
source.include_exts = py

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 1

android.permissions = INTERNET

# Android versions
android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 28c

[buildozer]

log_level = 2
warn_on_root = 1