import pandas as pd
import anthropic
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod
import streamlit as st

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
    """

    dashboard_code = model.generate_response(prompt)
    return dashboard_code

def save_dashboard_code(code, output_file="output/streamlit_dashboard.py"):
    """Save the generated dashboard code to a file"""
    template = """
import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("Data/Marketing+Data/marketing_data.csv")

data = load_data()

# Set page title
st.set_page_config(page_title="Marketing Data Dashboard", layout="wide")

# Main title
st.title("Marketing Data Dashboard")

# Generated dashboard code will be inserted here
{generated_code}

if __name__ == "__main__":
    st.sidebar.info("This dashboard is generated using AI.")
    """
    
    full_code = template.format(generated_code=code)
    
    with open(output_file, "w") as f:
        f.write(full_code)
    print(f"Dashboard code saved to {output_file}")

def main():
    # Choose the AI model client (Claude in this case)
    model = ClaudeClient()

    # Read the data
    data = read_data("Data/Marketing+Data/marketing_data.csv")
    
    # Generate dashboard code
    dashboard_code = generate_dashboard_code(data, model)
    
    # Save the generated code
    save_dashboard_code(dashboard_code)

if __name__ == "__main__":
    main()