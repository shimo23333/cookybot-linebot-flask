from api.linebot import LineBot
from api.magic import RecipeGenerator
from api.normal import NormalRequest
from flask import Flask, request, abort, jsonify  # 匯入 Flask 框架，request 用於處理請求，abort 用於中止請求，jsonify 用於回應 JSON 格式資料
import os  # 用於處理系統相關的操作（這裡似乎未使用到）
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage,
    StickerMessage,
    # ImageSendMessage
)
from linebot.models import ImageSendMessage
from dotenv import load_dotenv
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)

load_dotenv()
app = Flask(__name__)  # 創建一個 Flask 應用實例
magic = RecipeGenerator(os.getenv("OPENAI_API_KEY"))
line=LineBot(os.getenv("LINE_CHANNEL_TOKEN"),os.getenv("LINE_CHANNEL_SECRET"),magic)
normal=NormalRequest(magic)
line_handler=line.getHandler()

# 根路由，當用戶訪問 '/' 時返回 "Hello world"
@app.route("/")
def home():
    return "Hello 你好world"

# 設定一個處理 POST 請求的路由，路徑為 '/message'
@app.route('/message', methods=['POST']) 
def api_receive_message():
    return normal.handler_message(request)

@app.route('/upload', methods=['POST'])
def api_upload_image():
    return normal.handler_image(request)

# Line 串接區
#LINE 官方帳號的 webhook 網址輸入後，的驗證回傳函示。略過

@app.route("/line", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@line_handler.add(MessageEvent, message=TextMessageContent)
def line_receive_message(event):
    # line.handler_message(event)
    configuration=line.getConfig()
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        image_url= preview_url = 'https://cdn.pixabay.com/photo/2015/10/01/17/17/car-967387_1280.png'  # 設定你要回應的圖片 URL
        messages = [
                TextMessage(text='hhhh'),  # 這是你要回應的文字訊息
                StickerMessage(package_id='1', sticker_id='2'),
                # ImageSendMessage(original_content_url=image_url, preview_image_url=preview_url)  # 圖片回應
        ]
        
        line_bot_api.reply_message_with_http_info( #回傳訊息的功能
            ReplyMessageRequest( #建立一個回傳訊息物件
                reply_token=event.reply_token, #這次溝通的密碼
                messages=messages
            )
        )

@line_handler.add(MessageEvent, message=ImageMessageContent)
def line_upload_image(event):
    line.handler_image(event)


# 如果此檔案是主程式運行，啟動 Flask 應用
if __name__ == '__main__':
    app.run(debug=True)  # 開啟 Flask 開發模式(debug=True)，可以即時看到錯誤並重啟應用
