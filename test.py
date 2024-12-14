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
    ReplyMessageRequest,
    TextMessage,
)
from linebot.models import ImageSendMessage
from dotenv import load_dotenv
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)

load_dotenv()
app = Flask(__name__)  # 創建一個 Flask 應用實例

# LINE 密鑰
configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# Line 串接區
#LINE 官方帳號的 webhook 網址輸入後，的驗證回傳函示。略過

@app.route("/line", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)
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
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        image_url= 'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png'  # 設定你要回應的圖片 URL
        img_message=ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)  # 圖片回應
        text=TextMessage(text='hhhh2')
        messages = [
                # img_message, # 問題在這裡, 一直無法運行
                text
        ]
        # print(image)
        try:
            line_bot_api.reply_message_with_http_info( #回傳訊息的功能
                ReplyMessageRequest( #建立一個回傳訊息物件
                    reply_token=event.reply_token, #這次溝通的密碼
                    messages=messages
                )
            )
        except Exception  as e:
            app.logger.error(f"Error sending message: {e}")
            return jsonify({"error": "Failed to send message"}), 500



# 如果此檔案是主程式運行，啟動 Flask 應用
if __name__ == '__main__':
    app.run(debug=True)  # 開啟 Flask 開發模式(debug=True)，可以即時看到錯誤並重啟應用
