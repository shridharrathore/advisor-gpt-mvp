from openai import OpenAI
import logging
import json
from backend.config import Settings

class openaiservice:
    def __init__(self, settings: Settings):
        self.client = OpenAI(api_key = settings.openai_api_key)
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        
    def generate_response(self, user_prompt: str, system_prompt: str):
        messages = [
           {"role": "system","content": system_prompt},
           {"role": "user","content": user_prompt}
           ]
           
        try:
            response = self.client.chat.completions.create(
                model=self.settings.openai_model,
                messages=messages,
                )
            content = response.choices[0].message.content
            
            # Try to parse as JSON first
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # If not JSON, return as string
                return content
                
        except Exception as e:
            self.logger.error(f"Failed to generate response: {str(e)}")
            return "Error generating response"
