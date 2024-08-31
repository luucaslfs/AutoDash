import pandas as pd
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

class ClaudeClient:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def generate_response(self, prompt):
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=8000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return ''.join(block.text for block in response.content)

def generate_dashboard_code(data):
    """Generate dashboard code using Claude AI"""
    model = ClaudeClient()
    
    prompt = f"""
    Create Python code for a Streamlit dashboard based on this dataset (first 10 rows shown below):

    {data.head(10).to_string()}

    The code should include:
    1. Data preprocessing (if needed)
    2. At least two visualizations using Plotly or Altair
    3. Some basic statistics or insights about the data
    4. Interactive elements (e.g., filters, selectors)

    The code should be complete and ready to run within a Streamlit app.
    Do not include any placeholder comments or TODO items.
    Include all necessary imports at the beginning of the code.
    """

    dashboard_code = model.generate_response(prompt)
    return dashboard_code