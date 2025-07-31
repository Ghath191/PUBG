[app]

# (اسم التطبيق)
title = MyApp

# (اسم البايثون الرئيسي، مثلا main.py)
source.dir = .

# (اسم الملف الرئيسي لتشغيل التطبيق)
source.main = main.py

# (النسخة)
version = 1.0

# (اسم الحزمة)
package.name = myapp

# (معرف الحزمة، غيرّه حسبك)
package.domain = org.example

# (الإصدار)
android.api = 33

# (الإصدار الأدنى من SDK)
android.minapi = 21

# (الإصدار الأدنى من NDK)
android.ndk = 25b

# (موجه NDK)
android.ndk_api = 21

# (تصريح لتشغيل الإنترنت)
android.permissions = INTERNET

# (المكتبات الإضافية التي يحتاجها مشروعك، مثلاً kivy)
requirements = python3,kivy

# (خاصية تشغيل الكود على وضع التطوير)
android.debug = 1

# (تصاريح إضافية لو تحتاج، أضف هنا)
# android.permissions = INTERNET,ACCESS_FINE_LOCATION

[buildozer]

# (مكان حفظ ملفات البناء)
build_dir = ./build

# (تفعيل أو تعطيل بناء التطبيق)
# build = True
