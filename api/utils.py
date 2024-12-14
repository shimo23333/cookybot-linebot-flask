import requests
import base64


# 設定允許上傳的圖片類型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 檢查圖片檔案的副檔名
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_line_upload_image(message_id, LINE_CHANNEL_TOKEN):
    url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
    headers = {"Authorization": f"Bearer {LINE_CHANNEL_TOKEN}"}
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        img_base64 = base64.b64encode(response.content).decode('utf-8')
        return img_base64

    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        