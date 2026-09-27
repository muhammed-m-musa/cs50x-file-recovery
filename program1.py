import csv
from cs50 import SQL

# 1. الاتصال بقاعدة البيانات الموجودة مسبقاً
db = SQL("sqlite:///files.db")

# 2. فتح وقراءة ملف الـ CSV وإدخال البيانات مباشرة إلى الجدول الجاهز
with open("organizer_report.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        filename = row["Filename"]
        size_bytes = row["Size_Bytes"]

        # إدخال السجلات مباشرة دون الحاجة لإعادة إنشاء الجدول
        db.execute(
            "INSERT INTO recovered_files (filename, size_bytes) VALUES (?, ?);",
            filename,
            size_bytes
        )

print("تمت إضافة جميع الملفات إلى قاعدة البيانات بنجاح!")

# 3. استرجاع البيانات وعرضها للمستخدم لتأكيد النتيجة
files = db.execute("SELECT filename, size_bytes FROM recovered_files;")

print("\nالملفات المسترجعة والمرتبة الموجودة في قاعدة البيانات:")
for f in files:
    print(f"اسم الملف: {f['filename']} | الحجم: {f['size_bytes']} بايت")
