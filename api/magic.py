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
            style="A professional food photography scene capturing a warm and authentic meal setup. The composition highlights vibrant colors and textures, showcasing dishes with glossy sauces, fluffy grains, and freshly baked bread. The lighting is soft and diffused, with natural side lighting streaming in to create realistic shadows and a warm, inviting glow. A subtle backlight adds depth, emphasizing the fine details like steam rising from the dishes and subtle reflections on the tableware.The setting features rustic, natural elements, such as slightly worn wooden boards, hand-thrown ceramic plates, and utensils with a matte finish, giving an authentic, lived-in feel. The dishes are slightly imperfect, with small drips of sauce and scattered crumbs, adding a touch of realism. The background is dark and softly blurred, featuring props like loosely folded napkins, a lit candle, and sprigs of fresh herbs, creating a cozy, intimate dining atmosphere. The garnishes, such as fresh herbs and vibrant spices, are casually arranged to evoke a sense of spontaneity and natural beauty. The overall scene feels genuine, as though captured moments before a meal is enjoyed."
            # style="Capture a realistic and inviting flat-lay shot of a variety of colorful dishes served in mismatched round bowls and plates, as if freshly prepared for a shared meal. Arrange the items in an organic, slightly imperfect composition to create a natural, casual vibe. Incorporate warm tones like orange, yellow, and red with cool-toned accents such as dark tablecloths, green garnishes, and scattered spices or herbs for added authenticity. Use soft, diffused natural light or simulated natural light from the top-left corner to highlight the textures of the food, avoiding harsh shadows while maintaining gentle gradients for depth. Enhance realism with small, natural details like crumbs, spills, or utensils slightly out of place. Add textured fabric napkins, rustic serving boards, or subtle imperfections in the table surface for a cozy, lived-in atmosphere."
            # style="Create a hyper-realistic, detailed illustration with soft lighting and natural color tones. The artwork should emphasize vibrant colors, clear textures, and fine details, showcasing a clean and fresh aesthetic. The style is modern yet artistic, resembling high-quality still-life photography, with a minimalistic and elegant composition."
            image_prompt = f"{style}, 根據這份食譜，畫出一道美味的晚餐。食譜內容：{recipe_text}"

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
