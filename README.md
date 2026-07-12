# ☁️ Cloud Storage Demo: React + Python + Cloudinary

Dự án này là một bản demo kỹ thuật minh họa cho kiến trúc phân tách giữa tài nguyên tính toán (Compute) và lưu trữ (Storage).
Hệ thống sử dụng **React (Vite)** cho giao diện người dùng, **Python (Flask)** làm máy chủ cấp phát chữ ký bảo mật, và **Cloudinary** làm nền tảng Object Storage để lưu trữ tài sản tĩnh (ảnh).

## 📂 Cấu trúc dự án

Dự án được chia làm 2 phần hoạt động hoàn toàn độc lập:

- `backend/`: Máy chủ API viết bằng Python (Flask). Chịu trách nhiệm bảo mật API Secret và cấp phát chữ ký (Signature) cho Frontend.
- `frontend/`: Ứng dụng Web tĩnh viết bằng ReactJS (Vite). Đảm nhận việc cung cấp giao diện tải ảnh, gọi API lấy chữ ký từ Backend và đẩy file thẳng lên Cloudinary (Serverless Upload).

---

## ⚙️ Hướng dẫn cài đặt và chạy dự án

### Yêu cầu hệ thống:

- Đã cài đặt [Node.js](https://nodejs.org/) (phiên bản 16 trở lên).
- Đã cài đặt [Python](https://www.python.org/) (phiên bản 3.8 trở lên).

### 1. Thiết lập Backend (Python)

Mở terminal, di chuyển vào thư mục gốc của dự án và thực hiện các lệnh sau:

```bash
# 1. Di chuyển vào thư mục backend
cd backend

# 2. Khởi tạo môi trường ảo (Virtual Environment)
python -m venv venv

# 3. Kích hoạt môi trường ảo
# - Trên Windows:
venv\Scripts\activate
# - Trên Mac/Linux:
# source venv/bin/activate

# 4. Cài đặt các thư viện cần thiết
pip install flask flask-cors cloudinary python-dotenv

# 5. Lệnh chạy backend
python app.py

### 2. Thiết lập Frontend (React)

# 1. Di chuyển vào thư mục frontend
cd frontend

# 2. Cài đặt các gói thư viện Node.js
npm install

# 3. Cài đặt thêm axios (để gọi API)
npm install axios

# 4. Khởi động giao diện web
npm run dev
```
