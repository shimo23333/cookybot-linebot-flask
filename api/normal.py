from api import magic
from flask import Flask, request, abort, jsonify
from utils import allowed_file, save_upload_image  # 匯入 Flask 框架，request 用於處理請求，abort 用於中止請求，jsonify 用於回應 JSON 格式資料

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
            filepath=save_upload_image(file)
            # 主要程式區
            labels = self.magic.identify_ingredients(filepath)
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
        