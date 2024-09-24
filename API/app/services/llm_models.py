import anthropic
from openai import OpenAI
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod

load_dotenv()

class AIModel(ABC):
    @abstractmethod
    def generate_response(self, prompt):
        pass

class ClaudeClient(AIModel):
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

    def generate_response(self, prompt):
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=8000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return ''.join(block.text for block in response.content)

class OpenAIClient(AIModel):
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

    def generate_response(self, prompt):
        response = self.client.chat.completions.create(
            model="o1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content