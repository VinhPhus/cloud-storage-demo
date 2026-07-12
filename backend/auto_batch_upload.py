import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Tải cấu hình từ file .env hiện có
load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# Đường dẫn đến thư mục chứa ảnh thô
FOLDER_PATH = "./local_images"

def batch_upload():
    print(f"🔄 Bắt đầu quét thư mục: {FOLDER_PATH}")
    
    # Kiểm tra xem thư mục có tồn tại không
    if not os.path.exists(FOLDER_PATH):
        print("❌ Lỗi: Không tìm thấy thư mục local_images. Hãy tạo và thêm ảnh vào nhé!")
        return

    # Lặp qua tất cả các file trong thư mục
    for filename in os.listdir(FOLDER_PATH):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            file_path = os.path.join(FOLDER_PATH, filename)
            print(f"\n🚀 Đang xử lý và tải lên: {filename}...")
            
            try:
                # Gọi API Cloudinary để upload, nén và tự động gán tag
                response = cloudinary.uploader.upload(
                    file_path,
                    folder="auto_batch_demo",       # Tự động tạo thư mục trên Cloud
                    tags=["demo_script", "cloud_storage"], # Gán thẻ để dễ tìm kiếm
                    transformation=[
                        {"width": 800, "height": 800, "crop": "fill"}, # Cắt vuông 800x800
                        {"quality": "auto", "fetch_format": "auto"}    # Tự động nén và chọn định dạng tối ưu (WebP/AVIF)
                    ]
                )
                
                print(f"✅ Thành công! Kích thước mới: {response.get('bytes')} bytes")
                print(f"🔗 URL: {response.get('secure_url')}")
                
            except Exception as e:
                print(f"❌ Lỗi khi tải file {filename}: {e}")

if __name__ == "__main__":
    batch_upload()
    print("\n🎉 Hoàn tất quá trình tải lên tự động!")