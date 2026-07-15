import requests
import socket
from urllib.parse import urlparse
import re
import time

def analyze_cloudinary_url(url):
    print(f"\n🔍 [OSINT TOOL] ĐANG PHÂN TÍCH PUBLIC URL...")
    time.sleep(1)
    
    # 1. Phân tích cú pháp URL
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path_parts = parsed_url.path.split('/')
    
    print("\n--- 📂 1. THÔNG TIN HỆ THỐNG (INFORMATION LEAKAGE) ---")
    try:
        # Lấy Cloud Name (Thường nằm ở vị trí thứ 1 trong path của Cloudinary)
        cloud_name = path_parts[1]
        print(f"[+] Cloud Name (Tài khoản đích): {cloud_name}")
        
        # Tìm thư mục nội bộ và Tên file
        file_name = path_parts[-1]
        folder_structure = "/".join(path_parts[5:-1]) if len(path_parts) > 5 else "Thư mục gốc"
        print(f"[+] Tên file: {file_name}")
        print(f"[+] Cấu trúc thư mục nội bộ: {folder_structure}")
        
        # Tìm mã Version (v...)
        version_match = re.search(r'v\d+', url)
        if version_match:
            print(f"[+] Mã phiên bản (Version): {version_match.group(0)}")
    except Exception as e:
        print("[-] Không thể bóc tách cấu trúc Cloudinary chuẩn.")

    print("\n--- 🌐 2. TRINH SÁT HẠ TẦNG MẠNG (NETWORK RECONNAISSANCE) ---")
    time.sleep(1)
    try:
        # Phân giải IP của CDN Server
        cdn_ip = socket.gethostbyname(domain)
        print(f"[+] Tên miền phân phối: {domain}")
        print(f"[+] Địa chỉ IP máy chủ CDN (Edge Node): {cdn_ip}")
    except socket.gaierror:
        print("[-] Không thể phân giải IP.")

    print("\n--- 🕵️ 3. DẤU VẾT HTTP HEADERS (CDN CACHE & SERVER INFO) ---")
    time.sleep(1)
    try:
        # Gửi request để đọc Headers mà không tải toàn bộ ảnh (tối ưu băng thông)
        response = requests.head(url)
        headers = response.headers
        
        print(f"[+] Kích thước file: {headers.get('Content-Length', 'N/A')} bytes")
        print(f"[+] Loại dữ liệu (MIME Type): {headers.get('Content-Type', 'N/A')}")
        print(f"[+] Máy chủ phản hồi (Server): {headers.get('Server', 'N/A')}")
        print(f"[+] Trạng thái Bộ nhớ đệm (X-Cache): {headers.get('X-Cache', 'Không xác định')}")
        print(f"[+] Ngày giờ máy chủ (Date): {headers.get('Date', 'N/A')}")
    except Exception as e:
        print(f"[-] Lỗi khi quét Headers: {e}")

# Chạy thử nghiệm với một link URL bất kỳ của bạn
if __name__ == "__main__":
    test_url = input("Nhập URL Public cần phân tích: ")
    analyze_cloudinary_url(test_url)