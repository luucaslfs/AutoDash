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
            max_tokens=200000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content

class OpenAIClient(AIModel):
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

    def generate_response(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o",
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
    """Generate dashboard code using the specified AI model"""
    data_summary = data.describe().to_string()
    prompt = f"""You are an expert in data analysis and visualization. Your task is to analyze the following dataset summary and generate Python code for an interactive dashboard using Dash and Plotly.

Dataset summary:
{data_summary}

Instructions:
1. Data Import and Preparation: Include code to load and clean the data.
2. Exploratory Data Analysis (EDA): Calculate descriptive statistics and identify patterns.
3. Visualizations and Insights: Create visualizations that best represent the key insights.
4. Interactive Dashboard: Develop an interactive dashboard with filters or controls.

Provide only the Python code required to create the dashboard. The code should be complete and runnable, including all necessary imports and the app.run_server() call.

Objective: Create a dashboard that presents the data in a visually appealing manner and provides valuable insights easily understandable by someone with no prior experience in data analysis or business intelligence.
Output: The output will be saved in a runnable .py file so make sure you just output the runnable python code with nothing else.
"""

    return model.generate_response(prompt)

def save_dashboard_code(code, output_file="output/dashboard.py"):
    """Save the generated dashboard code to a file"""
    with open(output_file, "w") as f:
        f.write(code)
    print(f"Dashboard code saved to {output_file}")

def main():
    # Choose the AI model client (Claude or OpenAI)
    model = OpenAIClient()

    data = read_data("data/Rotten Tomatoes Movies.csv")
    dashboard_code = generate_dashboard_code(data, model)
    save_dashboard_code(dashboard_code)

if __name__ == "__main__":
    main()