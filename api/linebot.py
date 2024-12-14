import os

from api import magic
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
from utils import allowed_file, save_upload_image

class LineBot:
    def __init__(self, LINE_CHANNEL_TOKEN,LINE_CHANNEL_SECRET,magic):
        self.configuration = Configuration(access_token=LINE_CHANNEL_TOKEN)
        self.line_handler = WebhookHandler(LINE_CHANNEL_SECRET)
        self.api_clien=ApiClient(self.configuration)
        self.magic=magic

    def getHandler(self): 
        return self.line_handler
        
    #接收到使用者輸入的文字
    def handler_message(self, event):
        with ApiClient(self.configuration) as api_client:

            # 餵給openAI
            openAiResponse =  self.magic.generate_recipe(event.message.text)
            
            # 傳送文字回應
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=openAiResponse)] 
                )
            )
            

             
    # 接收到使用者輸入的圖片
    def handler_image(self, event):
        with ApiClient(self.configuration) as api_client:
            
            #line_bot_blob_api = MessagingApiBlob(api_client)
            #message_content = line_bot_blob_api.get_message_content(message_id=event.message.id)
            
            # 檢查檔案名是否有效
            if file.filename == '':
                return jsonify({"error": "No selected file"}), 400
            
            # 如果檔案有效並且是允許的格式，則儲存檔案
            if file and allowed_file(file.filename):
                filepath=save_upload_image(file)
                # 主要程式區
                labels =  self.magic.identify_ingredients(filepath)
                recipe= self.magic.generate_recipe(labels)
                image= self.magic.generate_dinner_image(recipe)
            
            
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info( #回傳訊息的功能
                ReplyMessageRequest( #建立一個回傳訊息物件
                    reply_token=event.reply_token, #這次溝通的密碼
                    messages=[ #訊息的內容(多個)
                        TextMessage(text=labels),
                        TextMessage(text=recipe),
                        StickerMessage(package_id='1', sticker_id='2'),
                        # ImageSendMessage(
                        #     original_content_url = ngrok_url + "/static/" + event.message.id + ".png",
                        #     preview_image_url = ngrok_url + "/static/" + event.message.id + ".png"
                        # )
                    ] 
                )
            )

