import os
import csv
import shutil
import uuid
from flask import Flask, render_template, request, redirect, send_file, flash, after_this_request, session, abort
from cs50 import SQL
import subprocess

app = Flask(__name__)
app.secret_key = "cs50x_super_session_key"

JOBS_FOLDER = 'jobs'
app.config['JOBS_FOLDER'] = JOBS_FOLDER

db = SQL("sqlite:///files.db")

# القائمة البيضاء لأنواع المجلدات المسموح بتحميلها لمنع الثغرات الأمنية
ALLOWED_TYPES = {"jpg", "png", "gif", "zip", "no_ext"}

def format_size(size_in_bytes):
    if size_in_bytes is None:
        return "0 بايت"
    if size_in_bytes >= 1024 * 1024 * 1024:
        return f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"  #EXAMPLE: Bilion: 1.5 / 1.0 = 1.5 GB    --1.072.000.000 = GB
    elif size_in_bytes >= 1024 * 1024:
        return f"{size_in_bytes / (1024 * 1024):.2f} MB"    # 1.048.000 = MB
    elif size_in_bytes >= 1024:
        return f"{size_in_bytes / 1024:.2f} KB" # 1024 = 1 KB
    else:
        return f"{size_in_bytes} byte"

@app.route("/")
def index():
    if 'user_session' not in session:
        session['user_session'] = str(uuid.uuid4())

    current_session = session['user_session']

    folders_summary = db.execute("""
        SELECT
            SUBSTR(filename, INSTR(filename, '.') + 1) as folder_type,
            COUNT(*) as file_count,
            SUM(size_bytes) as total_size
        FROM recovered_files
        WHERE session_id = ?
        GROUP BY folder_type;
    """, current_session)

    for folder in folders_summary:
        folder["formatted_size"] = format_size(folder["total_size"])

    return render_template("index.html", folders=folders_summary)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "raw_file" not in request.files:
        flash("لم يتم العثور على ملف الـ RAW المرفوع.", "danger")
        return redirect("/")

    file = request.files["raw_file"]
    if file.filename == "":
        flash("الرجاء اختيار ملف صالح قبل المتابعة.", "danger")
        return redirect("/")

    if 'user_session' not in session:
        session['user_session'] = str(uuid.uuid4())
    current_session = session['user_session']

    # مسار مجلد هذه الجلسة الخاصة بالمستخدم الحالي فقط
    session_dir = os.path.join(JOBS_FOLDER, current_session)

    # تنظيف مجلد الجلسة بالكامل لضمان عدم تراكم الملفات القديمة
    if os.path.exists(session_dir):
        shutil.rmtree(session_dir)

        # تفريغ بيانات الجلسة القديمة لنفس المستخدم من قاعدة البيانات مسبقاً
    db.execute("DELETE FROM recovered_files WHERE session_id = ?;", current_session)


    os.makedirs(session_dir, exist_ok=True)

    # حفظ ملف الـ RAW المرفوع حديثاً
    file_path = os.path.join(session_dir, "input.raw")
    file.save(file_path)

    # تجهيز المسارات المعزولة تماماً لتمريرها لبرنامج C
    recovered_dir = os.path.join(session_dir, "recovered")
    sorted_dir = os.path.join(session_dir, "sorted_files")
    os.makedirs(recovered_dir, exist_ok=True)
    os.makedirs(sorted_dir, exist_ok=True)


    # استدعاء برنامج C المعزول بالمعاملات الـ 4 تماماً
    result = subprocess.run([
        "./project",
        file_path,
        recovered_dir,
        session_dir,
        current_session
    ], capture_output=True, text=True)

    if result.returncode != 0:
        flash("حدث خطأ أثناء معالجة الملف بواسطة برنامج الاسترجاع (C).", "danger")
        return redirect("/")

    # المسار الصارم والدقيق لملف الـ CSV الخاص بهذه الجلسة حصرياً
    csv_file_path = os.path.join(session_dir, f"user_{current_session}_report.csv")

    file_count_inserted = 0
    if not os.path.exists(csv_file_path):
        flash("عذراً، لم يتم العثور على أي ملفات مدعومة للاسترجاع في هذا الملف. تأكد من رفع ملف RAW صالح.", "danger")
        return redirect("/")


    with open(csv_file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # التحقق من أن القيم موجودة وليست فارغة لمنع الأخطاء
            if row.get("Filename") and row.get("Size_Bytes"):
                db.execute(
                    "INSERT INTO recovered_files (session_id, filename, size_bytes) VALUES (?, ?, ?);",
                    current_session,
                    row["Filename"],
                    row["Size_Bytes"]
                )
                file_count_inserted += 1

    # التحقق الذكي: هل تم استرجاع ملفات حقاً أم أن الملف كان فارغاً (مثل الـ PDF)؟
    if file_count_inserted == 0:

        # حذف مجلد الجلسة بالكامل من القرص الصلب فوراً لمنع تراكم الملفات
        if os.path.exists(session_dir):
            shutil.rmtree(session_dir)

        # حذف السجلات المرتبطة بهذه الجلسة من قاعدة البيانات
        db.execute("DELETE FROM recovered_files WHERE session_id = ?;", current_session)
        flash("عذراً، لم يتم العثور على أي ملفات مدعومة للاسترجاع في هذا الملف. تأكد من رفع ملف RAW صالح.", "danger")
        return redirect("/")

    flash("تم استرجاع وتنظيم الملفات بنجاح تام!", "success")
    return redirect("/")

@app.route("/reset", methods=["POST"])
def reset_view():
    if 'user_session' in session:
        current_session = session['user_session']
        db.execute("DELETE FROM recovered_files WHERE session_id = ?;", current_session)

        session_dir = os.path.join(JOBS_FOLDER, current_session)
        if os.path.exists(session_dir):
            shutil.rmtree(session_dir)

    flash("تمت إعادة ضبط النظام ومسح مخلفات جلستك بنجاح.", "info")
    return redirect("/")

@app.route("/download/<folder_type>")
def download_folder(folder_type):
    if 'user_session' not in session:
        return redirect("/")

    if folder_type not in ALLOWED_TYPES:
        abort(404)

    current_session = session['user_session']
    folder_path = os.path.join(JOBS_FOLDER, current_session, "sorted_files", folder_type)

    if not os.path.exists(folder_path):
        flash("المجلد غير موجود على النظام.", "danger")
        return redirect("/")

    session_dir = os.path.join(JOBS_FOLDER, current_session)
    zip_filename_base = os.path.join(session_dir, f"{folder_type}_files")
    zip_filepath = shutil.make_archive(zip_filename_base, 'zip', folder_path)

    @after_this_request
    def remove_zip(response):
        try:
            if os.path.exists(zip_filepath):
                os.remove(zip_filepath)
        except Exception as e:
            print(f"Error deleting zip file: {e}")
        return response #HOSE have the first pointer of deleted file

    return send_file(zip_filepath, as_attachment=True) # here since this send_file func be defualt he will have the hose

if __name__ == "__main__":
    app.run(debug=False)
