import pandas as pd
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

class OpenAIClient(AIModel):
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

    def generate_response(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

def read_data(file_path):
    """Read data from Excel or CSV file"""
    if file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file format. Please use .xlsx or .csv")

def generate_dashboard_code(data, model):
    """Generate a complete, runnable dashboard code using the specified AI model"""

    prompt = f"""
    Create a complete, runnable Python script that generates an interactive dashboard using Dash and Plotly based on this dataset. (Head 10 rows of the dataset shown below):

    {data.head(10).to_string()}

    The script should include the following components:
    1. Data import and cleaning
    2. Exploratory Data Analysis (EDA)
    3. Dashboard layout and structure
    4. Interactive visualizations
    5. User controls (e.g., filters, dropdowns)
    6. Main function to run the dashboard

    The final script should be a single, self-contained file that can be run to launch the interactive dashboard. 
    Ensure the code is well-organized, documented, and follows best practices for Streamlit Dashboards.
    Do not include any placeholder comments or TODO items. The script should be complete and ready to run.

    Important: The script must use Streamlit and Plotly for the dashboard. Do not use any other visualization libraries.
    """

    dashboard_code = model.generate_response(prompt)
    return dashboard_code

def save_dashboard_code(code, output_file="output/dashboard_claude.py"):
    """Save the generated dashboard code to a file"""
    with open(output_file, "w") as f:
        f.write(code)
    print(f"Dashboard code saved to {output_file}")

def main():
    # Choose the AI model client (Claude or OpenAI)
    model = ClaudeClient()

    data = read_data("Data/Marketing+Data/marketing_data.csv")
    dashboard_code = generate_dashboard_code(data, model)
    save_dashboard_code(dashboard_code)

if __name__ == "__main__":
    main()