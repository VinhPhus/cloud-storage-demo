import os
import time
from flask import Flask, jsonify
from flask_cors import CORS
import cloudinary
import cloudinary.utils
from dotenv import load_dotenv

# Tải các biến từ file .env
load_dotenv()

app = Flask(__name__)
# Bật CORS để cho phép Frontend React gọi API
CORS(app)

# Cấu hình Cloudinary SDK
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

@app.route('/api/v1/cloudinary/signature', methods=['GET'])
def get_signature():
    try:
        # 1. Lấy timestamp hiện tại (tính bằng giây)
        timestamp = int(time.time())
        
        # 2. Tham số cần ký (bắt buộc phải có timestamp)
        params_to_sign = {
            "timestamp": timestamp
        }
        
        # 3. Tạo chữ ký bảo mật bằng API Secret (tự động lấy từ config)
        api_secret = cloudinary.config().api_secret
        signature = cloudinary.utils.api_sign_request(params_to_sign, api_secret)
        
        # 4. Trả về JSON cho Frontend
        return jsonify({
            "signature": signature,
            "timestamp": timestamp,
            "api_key": cloudinary.config().api_key,
            "cloud_name": cloudinary.config().cloud_name
        }), 200

    except Exception as e:
        print(f"Lỗi tạo chữ ký: {e}")
        return jsonify({"error": "Không thể tạo chữ ký bảo mật"}), 500

if __name__ == '__main__':
    # Chạy server ở cổng 5000
    app.run(port=5000, debug=True)