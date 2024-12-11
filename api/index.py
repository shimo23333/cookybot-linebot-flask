from flask import Flask, request, abort
import os
from openai import OpenAI
from PIL import Image


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

# LINE 密鑰
configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 輸入你的 OpenAI API 密鑰
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



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


# 根據食材生成晚餐食譜
def generate_recipe(ingredients):
    food_description = ", ".join(ingredients)
    recipe_prompt = f"請根據這些食材：{food_description}，生成一份晚餐食譜，150字以內簡短介紹。"

    response_recipe = client.chat.completions.create(
        model="gpt-4-turbo", 
        messages=[
            {"role": "system", "content": "你是一位大廚，根據食材創建美味的晚餐食譜。"},
            {"role": "user", "content": recipe_prompt}
        ]
    )
    recipe_text = response_recipe.choices[0].message.content
    return recipe_text


#run 自動回應使用者輸入的文字
@line_handler.add(MessageEvent, message=TextMessageContent)
def line_handler_message(event):
    with ApiClient(configuration) as api_client:
        
        # 用逗號分割成一個陣列
        textParts = event.message.text.split(",")
        
        # 把陣列喂給openAI
        openAiResponse = generate_recipe(textParts)
        
        # 傳送文字回應
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=openAiResponse)] 
            )
        )
            

             
#run 自動回應使用者傳送的圖片
@line_handler.add(MessageEvent, message=ImageMessageContent)
def line_handler_message(event):
    with ApiClient(configuration) as api_client:
        
        #line_bot_blob_api = MessagingApiBlob(api_client)
        #message_content = line_bot_blob_api.get_message_content(message_id=event.message.id)
        
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info( #回傳訊息的功能
            ReplyMessageRequest( #建立一個回傳訊息物件
                reply_token=event.reply_token, #這次溝通的密碼
                messages=[ #訊息的內容(多個)
                    TextMessage(text="收到圖片了1"),
                    TextMessage(text="收到圖片了2"),
                    StickerMessage(package_id='1', sticker_id='2'),
                ] 
            )
        )
    
        

if __name__ == "__main__":
    app.run()