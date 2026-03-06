import google.generativeai as genai
from app.core.config import settings

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def generate_content(self, prompt: str) -> str:
        """
        Generates content based on a prompt using Gemini 1.5 Flash.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            # In a real app, use a proper logger
            print(f"Error calling Gemini: {e}")
            return f"Error: Could not generate content. {str(e)}"

gemini_service = GeminiService()
