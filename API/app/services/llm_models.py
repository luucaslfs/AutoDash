import anthropic
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