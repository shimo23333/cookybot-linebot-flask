import os
import base64
from openai import OpenAI

class RecipeGenerator:
    def __init__(self, OPENAI_API_KEY):
        self.openai_client = OpenAI(api_key=OPENAI_API_KEY)

    def encode_image(self, image_path):
        """圖片編碼為 Base64"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"Error: File {image_path} not found. Please check the file path.")
            return None

    def identify_ingredients(self, image_path):
        """使用gpt-4o-mini 辨識圖片中的食材"""
        try:
            base64_image=self.encode_image(image_path)
            text= {
                "type": "text",
                "text": "請辨識出圖片中所有食物",
            }
            image={
                "type": "image_url",
                "image_url": {"url":  f"data:image/jpeg;base64,{base64_image}"}
            }
            completion = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                        "role": "user",
                        "content": [text,image],
                }],
            )
            result = completion.choices[0].message.content
            return result
        except Exception as e:
            print(f"Error identifying ingredients: {e}")
            return []

    def generate_recipe(self, ingredients):
        """使用 OpenAI API 生成食譜"""
        try:
            recipe_prompt = f"請根據這些食材：{ingredients}，生成一份晚餐食譜，200字以內簡短介紹。"

            response_recipe = self.openai_client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "你是一位大廚，根據食材創建美味的晚餐食譜。"},
                    {"role": "user", "content": recipe_prompt}
                ]
            )

            return response_recipe.choices[0].message.content
        except Exception as e:
            print(f"Error generating recipe: {e}")
            return ""

    def generate_dinner_image(self, recipe_text):
        """使用 OpenAI API 生成食物圖片"""
        try:
            image_prompt = f"根據這份食譜，畫出一道美味的晚餐。食譜內容：{recipe_text}"

            response_image = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )

            return response_image.data[0].url
        except Exception as e:
            print(f"Error generating dinner image: {e}")
            return ""
