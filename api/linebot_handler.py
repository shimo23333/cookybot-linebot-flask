
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,PushMessageRequest,
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
        # self.api_clien=
        self.magic=magic
        self.line_bot_api = MessagingApi(ApiClient(self.configuration))

    def getHandler(self): 
        return self.line_handler
    
    #接收到使用者輸入的文字
    def handler_message(self, event):
        user_id = event.source.user_id
        token=event.reply_token

        # 餵給openAI
        # 傳送文字回應
        recipe =  self.magic.generate_recipe(event.message.text)
        messages=[
            TextMessage(text=recipe),
            TextMessage(text="模擬圖生成中, 請稍後..."),
        ]
    
        self.replay(token,messages)
        
        # 回傳圖片給使用者
        image=self.magic.generate_dinner_image(recipe)
        messages=[
            ImageMessage(original_content_url = image,preview_image_url = image)  
        ]
        self.push(user_id,messages)
    
             
    # 接收到使用者輸入的圖片
    def handler_image(self,event):
        message_id = event.message.id
        user_id = event.source.user_id
        token=event.reply_token
        
        base64_image=save_line_upload_image(message_id, self.token)
        labels = self.magic.identify_ingredients(base64_image)
        recipe = self.magic.generate_recipe(labels)
        messages=[
            TextMessage(text=labels),
            TextMessage(text=recipe),
            TextMessage(text="模擬圖生成中, 請稍後..."),
        ]
        self.replay(token,messages)
        
        # 回傳圖片給使用者
        image=self.magic.generate_dinner_image(recipe)
        messages=[
            ImageMessage(original_content_url = image,preview_image_url = image)  
        ]
        self.push(user_id,messages)

    def replay(self,token,messages): 
        try:
            self.line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=token,
                    messages=messages
                )
            )
        except Exception as e:
            print(f"Failed to send push message: {e}")
        
    def push(self,user_id,messages):  
        try:
            self.line_bot_api.push_message(
                PushMessageRequest(
                    to=user_id,  # 推送的目標用戶
                    messages=messages
                )
            )
            print("Push message sent successfully!")
        except Exception as e:
            print(f"Failed to send push message: {e}")
                
                
