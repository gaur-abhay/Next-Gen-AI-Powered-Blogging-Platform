import json
import re
import os

import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_KEY"))


class Gemini:

    def __init__(self):
        self.model = genai.GenerativeModel(model_name="gemini-1.0-pro")

    async def send_request(self, prompt: str):
        response = await self.model.generate_content_async(prompt)

        return Gemini.parse_model_response(response.text)

    @staticmethod
    def parse_model_response(response):
        attempt = 0
        try:
            # Use regex to remove \n before and after keys
            parsed_data = response.replace("\n", "\\n")
            parsed_data = re.sub(r'\\n\s*"\s*', '"', parsed_data)
            # Removing \n at the end
            parsed_data = re.sub(r'\\n}$', '}', parsed_data)
            parsed_data = re.sub(r'\\n\s*"', '"', parsed_data)
            parsed_data = re.sub(r'"\s*\\n\s*', '"', parsed_data)
            parsed_data = json.loads(parsed_data)
            if len(parsed_data["body"]) != 2:
                raise
        except Exception as e:
            if attempt == 2:
                return None
            attempt += 1
            return Gemini.parse_model_response(response)

        return parsed_data


class GeminiUtils:

    def __init__(self):
        self.gemini_utils = Gemini()

    async def generate_blog_post(self, title: str, topic: str, tone: str) -> dict:
        prompt = f"""As an AI writer your task is to draft a blog post with title as '{title}' on topic '{topic}'. Use a '{tone}' tone and style.
- Well structured and attractive.
- Use interactive Emojis.
- Response must be short.

Expected Format:
{{"title": str, "body": str}}
"""

        return await self.gemini_utils.send_request(prompt)

    async def suggest_blog_post(self, name: str, job_title: str, skill: str, interest: str) -> dict:
        prompt = f"""As an AI writer your task is to draft two blog post for '{name}' a '{job_title}' who has expertise in '{skill}' and interest as '{interest}'.
- Use a tone and style that best suit user.
- Well structured and attractive.  
- Use interactive Emojis.
- Response must be short.
- Strictly follow expected format.

Expected Format:  
{{"title":  ["title1", "title2"], "body": ["body1", "body2"]}}
"""

        return await self.gemini_utils.send_request(prompt)
