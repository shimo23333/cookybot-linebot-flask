import os  # 用於處理系統相關的操作（這裡似乎未使用到）
from datetime import datetime
import random
import string
import requests

# 設定圖片儲存的目錄
UPLOAD_FOLDER = '/tmp/uploads'  # 這個資料夾可以是你的應用所在目錄中的 'uploads'
if not os.path.exists(UPLOAD_FOLDER):  # 如果目錄不存在，則創建它
    os.makedirs(UPLOAD_FOLDER)

# 設定允許上傳的圖片類型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 檢查圖片檔案的副檔名
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# 生成唯一的檔案名稱，包含時間戳和三位隨機碼
def generate_filename(extension):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # 取得當前時間的時間戳
    random_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))  # 生成三位隨機碼
    return f"{timestamp}_{random_code}.{extension}"

def save_upload_image(file):
    # 取得檔案的副檔名
    extension = file.filename.rsplit('.', 1)[1].lower()
    # 生成新的檔案名稱
    filename = generate_filename(extension)
    # 儲存檔案
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return filepath

def save_line_upload_image(message_id, LINE_CHANNEL_TOKEN):
    url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
    headers = {"Authorization": f"Bearer {LINE_CHANNEL_TOKEN}"}
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        filename = f"test.jpeg"
        save_path = os.path.join('uploads', filename)

        # 將圖片內容寫入檔案
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Image saved as {save_path}")
        return save_path
    else:
        print(f"Failed to download image. Status code: {response.status_code}")