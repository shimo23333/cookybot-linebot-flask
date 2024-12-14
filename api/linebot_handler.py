
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage,
    ImageMessage
)
from api.utils import  save_line_upload_image

class LineBot:
    def __init__(self, LINE_CHANNEL_TOKEN,LINE_CHANNEL_SECRET,magic):
        self.token=LINE_CHANNEL_TOKEN
        self.configuration = Configuration(access_token=LINE_CHANNEL_TOKEN)
        self.line_handler = WebhookHandler(LINE_CHANNEL_SECRET)
        self.api_clien=ApiClient(self.configuration)
        self.magic=magic

    def getHandler(self): 
        return self.line_handler
        
    def getConfig(self):
        return self.configuration
    #接收到使用者輸入的文字
    def handler_message(self, event):
        with ApiClient(self.configuration) as api_client:

            # 餵給openAI
            recipe =  self.magic.generate_recipe(event.message.text)
            image=self.magic.generate_dinner_image(recipe)
            
            messages=[
                TextMessage(text=recipe),
                ImageMessage(
                    original_content_url = image,
                    preview_image_url = image
                )  
            ]
            
            # # 傳送文字回應
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=messages
                )
            )
        
             
    # 接收到使用者輸入的圖片
    def handler_image(self,event):
        with ApiClient(self.configuration) as api_client:
            message_id = event.message.id
            save_path=save_line_upload_image(message_id, self.token)

            
            labels = self.magic.identify_ingredients(save_path)
            recipe=self.magic.generate_recipe(labels)
            image=self.magic.generate_dinner_image(recipe)
            
            messages=[
                TextMessage(text=labels),
                TextMessage(text=recipe),
                ImageMessage(
                    original_content_url = image,
                    preview_image_url = image
                )  
            ]

            # 回傳圖片給使用者
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=messages
                )
            )

                
                
                
