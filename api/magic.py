import os
import base64
from openai import OpenAI
from groq import Groq

class RecipeGenerator:
    def __init__(self, OPENAI_API_KEY,GROQ_API_KEY):
        self.image_llm_client = OpenAI(api_key=OPENAI_API_KEY)
        self.llm_client= Groq(api_key=GROQ_API_KEY)
        # self.llm_model="gpt-4o-mini"
        self.llm_model="llama-3.2-90b-vision-preview"
    def groq_identify_ingredients(self, base64_image): 
        """使用llm vision辨識圖片中的食材"""
        try:
            print("食材辨識中...")
            text= {
                "type": "text",
                "text": "請辨識出圖片中所有食物",
            }
            image={
                "type": "image_url",
                "image_url": {"url":  f"data:image/jpeg;base64,{base64_image}"}
            }
            completion = self.groq_client.chat.completions.create(
                # model="gpt-4o-mini",
                model=self.llm_model,
                messages=[{
                        "role": "user",
                        "content": [text,image],
                }],
            )
            result = completion.choices[0].message.content
            return result
        except Exception as e:
            print(f"Error identifying ingredients: {e}")
            return ""
    def identify_ingredients(self, base64_image):
        """使用gpt-4o-mini 辨識圖片中的食材"""
        try:
            print("食材辨識中...")
            text= {
                "type": "text",
                "text": "請辨識出圖片中所有食物",
            }
            image={
                "type": "image_url",
                "image_url": {"url":  f"data:image/jpeg;base64,{base64_image}"}
            }
            completion = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[{
                        "role": "user",
                        "content": [text,image],
                }],
            )
            result = completion.choices[0].message.content
            return result
        except Exception as e:
            print(f"Error identifying ingredients: {e}")
            return ""

    def generate_recipe(self, ingredients):
        """使用 OpenAI API 生成食譜"""
        try:
            print("生成食譜中...")
            recipe_prompt = f"請根據這些食材：{ingredients}，生成一份晚餐食譜，200字以內簡短介紹。"

            response_recipe = self.llm_client.chat.completions.create(
                model= self.llm_model,
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
            print("生成食物圖片中...")
            image_prompt = f"根據這份食譜，畫出一道美味的晚餐。食譜內容：{recipe_text}"

            response_image = self.image_llm_client.images.generate(
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
