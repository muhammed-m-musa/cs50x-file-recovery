# import io
# import zipfile
# from PIL import Image, ImageDraw

# block_size = 512
# output_filename = "flash1.raw"

# def get_in_memory_jpeg(index):
#     img = Image.new('RGB', (100, 100), color=(index * 5 % 255, 120, 200))
#     d = ImageDraw.Draw(img)
#     d.text((10, 40), f"JPG {index}", fill=(255, 255, 255))
#     output = io.BytesIO()
#     img.save(output, format="JPEG")
#     return output.getvalue()

# def get_in_memory_png(index):
#     img = Image.new('RGB', (100, 100), color=(50, index * 5 % 255, 150))
#     d = ImageDraw.Draw(img)
#     d.text((10, 40), f"PNG {index}", fill=(255, 255, 255))
#     output = io.BytesIO()
#     img.save(output, format="PNG")
#     return output.getvalue()

# def get_in_memory_gif(index):
#     img = Image.new('RGB', (100, 100), color=(100, 150, index * 5 % 255))
#     d = ImageDraw.Draw(img)
#     d.text((10, 40), f"GIF {index}", fill=(255, 255, 255))
#     output = io.BytesIO()
#     img.save(output, format="GIF")
#     return output.getvalue()

# def get_in_memory_zip(index):
#     output = io.BytesIO()
#     with zipfile.ZipFile(output, 'w', zipfile.ZIP_STORED) as zf:
#         zf.writestr(f"sample_{index}.txt", f"This is real data for zip file number {index}")
#     return output.getvalue()

# all_blocks = []
# count_per_type = 50

# # قطاع بداية فارغ (MBR / Unallocated space) لكي لا ينخدع ويندوز ويميز الملف كصورة
# all_blocks.append(b'\x00' * block_size)

# print("جاري إنشاء الملفات في الذاكرة وكتابتها مباشرة إلى الملف الخام...")

# for i in range(count_per_type):
#     # جلب بايتات الملفات مباشرة من الذاكرة
#     file_contents = [
#         get_in_memory_jpeg(i),
#         get_in_memory_png(i),
#         get_in_memory_gif(i),
#         get_in_memory_zip(i)
#     ]

#     for content in file_contents:
#         # تقسيم محتوى الملف إلى كتل بحجم 512 بايت
#         for j in range(0, len(content), block_size):
#             chunk = content[j:j + block_size]
#             if len(chunk) < block_size:
#                 chunk += b'\x00' * (block_size - len(chunk))
#             all_blocks.append(chunk)

#         # إضافة فراغ صغير بين الملفات لمحاكاة قطاعات القرص
#         all_blocks.append(b'\x00' * block_size)

# # كتابة القرص الخام النهائي مباشرة
# with open(output_filename, "wb") as f:
#     for block in all_blocks:
#         f.write(block)

# print(f"تم بنجاح إنشاء '{output_filename}' كملف خام حقيقي وصافي 100% بدون أي مجلدات أو ملفات مؤقتة!")


import io
import zipfile
from PIL import Image, ImageDraw

block_size = 512
output_filename = "flash2.raw"

def get_in_memory_jpeg(index):
    img = Image.new('RGB', (100, 100), color=(index * 5 % 255, 120, 200))
    d = ImageDraw.Draw(img)
    d.text((10, 40), f"JPG {index}", fill=(255, 255, 255))
    output = io.BytesIO()
    img.save(output, format="JPEG")
    return output.getvalue()

def get_in_memory_png(index):
    img = Image.new('RGB', (100, 100), color=(50, index * 5 % 255, 150))
    d = ImageDraw.Draw(img)
    d.text((10, 40), f"PNG {index}", fill=(255, 255, 255))
    output = io.BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()

def get_in_memory_gif(index):
    img = Image.new('RGB', (100, 100), color=(100, 150, index * 5 % 255))
    d = ImageDraw.Draw(img)
    d.text((10, 40), f"GIF {index}", fill=(255, 255, 255))
    output = io.BytesIO()
    img.save(output, format="GIF")
    return output.getvalue()

def get_in_memory_zip(index):
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_STORED) as zf:
        zf.writestr(f"sample_{index}.txt", f"This is real data for zip file number {index}")
    return output.getvalue()

all_blocks = []
count_per_type = 10   # <-- التعديل الوحيد: كان 50 وصار 10

all_blocks.append(b'\x00' * block_size)

print("جاري إنشاء الملفات في الذاكرة وكتابتها مباشرة إلى الملف الخام...")

for i in range(count_per_type):
    file_contents = [
        get_in_memory_jpeg(i),
        get_in_memory_png(i),
        get_in_memory_gif(i),
        get_in_memory_zip(i)
    ]

    for content in file_contents:
        for j in range(0, len(content), block_size):
            chunk = content[j:j + block_size]
            if len(chunk) < block_size:
                chunk += b'\x00' * (block_size - len(chunk))
            all_blocks.append(chunk)

        all_blocks.append(b'\x00' * block_size)

with open(output_filename, "wb") as f:
    for block in all_blocks:
        f.write(block)

print(f"تم بنجاح إنشاء '{output_filename}' كملف خام حقيقي وصافي 100% بدون أي مجلدات أو ملفات مؤقتة!")
