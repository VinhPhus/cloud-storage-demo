import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# THAY BẰNG PUBLIC ID BẠN VỪA COPY TỪ GIAO DIỆN WEB
TARGET_PUBLIC_ID = "cloud_storage_demo/zyyasvax7uwe9ymok6qb" 
MALWARE_IMAGE = "hacked.jpg"

print(f"😈 [Ransomware] Đang xâm nhập và mã hóa mục tiêu: {TARGET_PUBLIC_ID}...")

try:
    # Lệnh upload này sẽ cố tình ghi đè vào đúng ID của bức ảnh cũ
    # invalidate=True để xóa bộ nhớ đệm (cache), ép ảnh mới hiển thị ngay lập tức
    response = cloudinary.uploader.upload(
        MALWARE_IMAGE,
        public_id=TARGET_PUBLIC_ID,
        invalidate=True
    )
    print("💥 Tấn công thành công! Dữ liệu gốc đã bị ghi đè.")
    print(f"🔗 Kiểm tra ngay: {response.get('secure_url')}")
except Exception as e:
    print(f"❌ Lỗi: {e}")   