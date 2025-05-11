from flask import Flask, request, jsonify
from deepface import DeepFace
import cv2
import numpy as np
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

app = Flask(__name__)

# === 讀取 Railway 上的金鑰變數 ===
service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
creds = service_account.Credentials.from_service_account_info(service_account_info)

# === Google Drive API 客戶端 ===
drive_service = build("drive", "v3", credentials=creds)

# === 測試用首頁 ===
@app.route("/")
def home():
    return "🚁 Drone Face Recognition API Ready!"

# === 臉部比對 API ===
@app.route("/verify", methods=["POST"])
def verify():
    if 'img1' not in request.files or 'img2' not in request.files:
        return jsonify({'error': 'Two images required (img1 and img2)'}), 400

    # 將兩張圖片轉成 numpy 格式
    img1 = np.frombuffer(request.files['img1'].read(), np.uint8)
    img2 = np.frombuffer(request.files['img2'].read(), np.uint8)
    img1 = cv2.imdecode(img1, cv2.IMREAD_COLOR)
    img2 = cv2.imdecode(img2, cv2.IMREAD_COLOR)

    try:
        result = DeepFace.verify(img1, img2, enforce_detection=False)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === 主程式入口 ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
