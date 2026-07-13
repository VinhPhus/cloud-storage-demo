import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadedUrl, setUploadedUrl] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setUploadedUrl(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);

    try {
      const sigResponse = await axios.get("/api/v1/cloudinary/signature");
      const { signature, timestamp, api_key, cloud_name } = sigResponse.data;

      const formData = new FormData();
      formData.append("file", file);
      formData.append("api_key", api_key);
      formData.append("timestamp", timestamp);
      formData.append("signature", signature);

      const cloudinaryUrl = `https://api.cloudinary.com/v1_1/${cloud_name}/image/upload`;
      const uploadResponse = await axios.post(cloudinaryUrl, formData);

      setUploadedUrl(uploadResponse.data.secure_url);
    } catch (error) {
      console.error("Lỗi khi upload:", error);
      alert("Đã xảy ra lỗi trong quá trình tải ảnh lên.");
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

        {/* Khung kéo thả / chọn file */}
        <div className="dropzone-container">
          <input
            type="file"
            className="file-input"
            accept="image/*"
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
              <p>Nhấn vào đây hoặc kéo thả ảnh</p>
              <span className="file-hint">Hỗ trợ JPG, PNG, WEBP</span>
            </div>
          ) : (
            <div className="preview-content">
              <img src={preview} alt="Preview" className="image-preview" />
              <div className="change-file-overlay">
                <span>Nhấn để đổi ảnh khác</span>
              </div>
            </div>
          )}
        </div>

        {/* Nút Tải lên */}
        <button
          className={`btn-upload ${uploading ? "loading" : ""} ${!file ? "disabled" : ""}`}
          onClick={handleUpload}
          disabled={!file || uploading}
        >
          {uploading ? (
            <>
              <span className="spinner"></span>
              Đang xử lý...
            </>
          ) : (
            "🚀 Tải ảnh lên Đám mây"
          )}
        </button>

        {/* Kết quả trả về */}
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
            <div className="link-box">
              <input type="text" readOnly value={uploadedUrl} />
              <button
                onClick={() => navigator.clipboard.writeText(uploadedUrl)}
              >
                Copy
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
