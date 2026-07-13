import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [fileType, setFileType] = useState(null); // 'image' hoặc 'video'
  const [preview, setPreview] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadedUrl, setUploadedUrl] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setUploadedUrl(null);

      // Nhận diện xem người dùng đang chọn ảnh hay video
      if (selectedFile.type.startsWith("video/")) {
        setFileType("video");
      } else {
        setFileType("image");
      }
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);

    try {
      // 1. Lấy chữ ký từ Python (Đã cập nhật dùng đường dẫn tương đối)
      const sigResponse = await axios.get("/api/v1/cloudinary/signature");
      const { signature, timestamp, api_key, cloud_name, folder } =
        sigResponse.data;

      // 2. Đóng gói dữ liệu
      const formData = new FormData();
      formData.append("file", file);
      formData.append("api_key", api_key);
      formData.append("timestamp", timestamp);
      formData.append("signature", signature);
      formData.append("folder", folder);

      // 3. Dùng /auto/upload để Cloudinary tự phân loại Ảnh hoặc Video
      const cloudinaryUrl = `https://api.cloudinary.com/v1_1/${cloud_name}/auto/upload`;
      const uploadResponse = await axios.post(cloudinaryUrl, formData);

      setUploadedUrl(uploadResponse.data.secure_url);
    } catch (error) {
      console.error("Lỗi khi upload:", error);
      alert(
        "Đã xảy ra lỗi trong quá trình tải lên đám mây. Hãy kiểm tra lại kết nối hoặc console log.",
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="app-wrapper">
      <div className="upload-card">
        <div className="card-header">
          <h2>Cloud Storage</h2>
          <p className="subtitle">Hệ thống lưu trữ tài sản tĩnh tối ưu</p>
        </div>

        <div className="dropzone-container">
          <input
            type="file"
            className="file-input"
            accept="image/*,video/*"
            onChange={handleFileChange}
          />

          {!preview ? (
            <div className="dropzone-content">
              <svg
                className="upload-icon"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                />
              </svg>
              <p>Nhấn vào đây hoặc kéo thả file</p>
              <span className="file-hint">
                Hỗ trợ JPG, PNG, WEBP, MP4, MOV...
              </span>
            </div>
          ) : (
            <div className="preview-content">
              {fileType === "video" ? (
                <video src={preview} controls className="image-preview" />
              ) : (
                <img src={preview} alt="Preview" className="image-preview" />
              )}

              <div className="change-file-overlay">
                <span>Nhấn để đổi file khác</span>
              </div>
            </div>
          )}
        </div>

        <button
          className={`btn-upload ${uploading ? "loading" : ""} ${!file ? "disabled" : ""}`}
          onClick={handleUpload}
          disabled={!file || uploading}
        >
          {uploading ? (
            <>
              <span className="spinner"></span>
              Đang đẩy lên mây...
            </>
          ) : (
            "🚀 Tải file lên Đám mây"
          )}
        </button>

        {uploadedUrl && (
          <div className="success-box">
            <div className="success-header">
              <svg
                className="check-icon"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
              <span>Tải lên thành công!</span>
            </div>
            <div className="link-box" style={{ marginBottom: "16px" }}>
              <input type="text" readOnly value={uploadedUrl} />
              <button
                onClick={() => navigator.clipboard.writeText(uploadedUrl)}
              >
                Copy
              </button>
            </div>

            <div
              style={{
                borderRadius: "12px",
                overflow: "hidden",
                border: "1px solid #d1d5db",
              }}
            >
              {fileType === "video" ? (
                <video
                  src={uploadedUrl}
                  controls
                  style={{ width: "100%", display: "block" }}
                />
              ) : (
                <img
                  src={uploadedUrl}
                  alt="Cloud Asset"
                  style={{ width: "100%", display: "block" }}
                />
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
