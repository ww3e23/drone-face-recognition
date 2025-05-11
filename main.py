import random
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# === 必填參數 ===
SERVICE_ACCOUNT_FILE = "service_account.json"
FOLDER_NAME = "people"
TARGET_PERSON = "王小明"  # 改成你要測試的人名資料夾
API_URL = "https://你的部署網址/verify"  # ← 改成你 Railway 上的網址

# === 初始化 Google Drive API ===
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

# === 找特定資料夾 ID ===
def get_folder_id(name, parent_id=None):
    q = f"name='{name}' and mimeType='application/vnd.google-apps.folder'"
    if parent_id:
        q += f" and '{parent_id}' in parents"
    results = drive_service.files().list(q=q, fields="files(id, name)").execute()
    files = results.get("files", [])
    return files[0]["id"] if files else None

# === 下載圖片為 BytesIO ===
def download_file(file_id):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    fh.seek(0)
    return fh

# === 主流程 ===
people_id = get_folder_id(FOLDER_NAME)
if not people_id:
    print("找不到 people 資料夾")
    exit()

person_id = get_folder_id(TARGET_PERSON, parent_id=people_id)
if not person_id:
    print(f"找不到人物資料夾：{TARGET_PERSON}")
    exit()

files = drive_service.files().list(
    q=f"'{person_id}' in parents and mimeType contains 'image/'",
    fields="files(id, name)").execute()["files"]

if len(files) < 2:
    print("照片數量不足")
    exit()

selected = random.sample(files, 2)
img1 = download_file(selected[0]["id"])
img2 = download_file(selected[1]["id"])

# === 發送 POST 請求給 API ===
response = requests.post(API_URL, files={
    "img1": ("img1.jpg", img1, "image/jpeg"),
    "img2": ("img2.jpg", img2, "image/jpeg")
})

print("✅ 驗證結果：", response.json())
