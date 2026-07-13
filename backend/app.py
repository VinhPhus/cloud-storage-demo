import os
import time
from flask import Flask, jsonify
from flask_cors import CORS
import cloudinary
import cloudinary.utils
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

@app.route('/api/v1/cloudinary/signature', methods=['GET'])
def get_signature():
    try:
        timestamp = int(time.time())
        # Thêm thư mục (folder) vào tham số cần ký để quản lý file gọn gàng hơn
        folder_name = "cloud_storage_demo"
        
        params_to_sign = {
            "timestamp": timestamp,
            "folder": folder_name
        }
        
        api_secret = cloudinary.config().api_secret
        signature = cloudinary.utils.api_sign_request(params_to_sign, api_secret)
        
        return jsonify({
            "signature": signature,
            "timestamp": timestamp,
            "api_key": cloudinary.config().api_key,
            "cloud_name": cloudinary.config().cloud_name,
            "folder": folder_name
        }), 200

    except Exception as e:
        print(f"Lỗi tạo chữ ký: {e}")
        return jsonify({"error": "Không thể tạo chữ ký bảo mật"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)