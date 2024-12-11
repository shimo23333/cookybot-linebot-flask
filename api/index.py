from flask import Flask, request, abort
import os


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
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
    
)

#改成新的了~~~(.evn)
#需要有 官方帳號的 TOKEN 和 SECRET

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/")
def home():
    return "Hello world"


#LINE 官方帳號的 webhook 網址輸入後，的驗證回傳函示。略過
@app.route("/callback", methods=['POST'])
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

#run 自動回應使用者輸入的文字
@line_handler.add(MessageEvent, message=TextMessageContent)
def line_handler_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        if event.message.text == "先度瑞拉":
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="再度你媽")]
                )
            )
        else:
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=event.message.text)] 
                )
            )
             
#run 自動回應使用者傳送的圖片
@line_handler.add(MessageEvent, message=ImageMessageContent)
def line_handler_message(event):
    with ApiClient(configuration) as api_client:
        
        #line_bot_blob_api = MessagingApiBlob(api_client)
        #message_content = line_bot_blob_api.get_message_content(message_id=event.message.id)
        
        # line_bot_api = MessagingApi(api_client)
        # line_bot_api.reply_message_with_http_info(
        #     ReplyMessageRequest(
        #         reply_token=event.reply_token,
        #         messages=[TextMessage(text="收到圖片了")] 
        #     )
        # )
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[StickerMessage(
                    package_id='1',
                    sticker_id='1')
                ]
            )
        )

            

if __name__ == "__main__":
    app.run()