from api.utils import allowed_file
from flask import jsonify
import base64

class NormalRequest:
    def __init__(self, magic):
        self.magic=magic

    def handler_message(self, request):
         # 取得請求中的 JSON 資料
        data = request.get_json()
        openAiResponse =  self.magic.generate_recipe(data)
        # 檢查請求資料中是否有 'message' 欄位
        if 'message' in data:
            # 如果有，回傳收到的訊息
            return jsonify({"data": openAiResponse}), 200
        else:
            # 如果沒有 'message' 欄位，回傳錯誤訊息
            return jsonify({"error": "No message found in the request"}), 400

    def handler_image(self, request):
        # 檢查請求中是否包含檔案
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        
        # 檢查檔案名是否有效
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        # 如果檔案有效並且是允許的格式，則儲存檔案
        if file and allowed_file(file.filename):
            base64_image = base64.b64encode(file.read()).decode('utf-8')
            # 主要程式區
            labels = self.magic.identify_ingredients(base64_image)
            recipe=self.magic.generate_recipe(labels)
            image=self.magic.generate_dinner_image(recipe)
            # 回傳結果
            return jsonify({
                "labels": labels,
                "recipe":recipe,
                "image":image
            }), 200
        else:
            return jsonify({"error": "File type not allowed"}), 400
        