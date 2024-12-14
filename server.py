from api.linebot import LineBot
from api.magic import RecipeGenerator
from api.normal import NormalRequest
from flask import Flask, request, abort, jsonify  # 匯入 Flask 框架，request 用於處理請求，abort 用於中止請求，jsonify 用於回應 JSON 格式資料
import os  # 用於處理系統相關的操作（這裡似乎未使用到）

from dotenv import load_dotenv
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
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
@line_handler.add(MessageEvent, message=TextMessageContent)
def line_receive_message(event):
    line.line_handler_message(event)

@line_handler.add(MessageEvent, message=ImageMessageContent)
def line_upload_image(event):
    line.line_handler_image(event)


# 如果此檔案是主程式運行，啟動 Flask 應用
if __name__ == '__main__':
    app.run(debug=True)  # 開啟 Flask 開發模式(debug=True)，可以即時看到錯誤並重啟應用