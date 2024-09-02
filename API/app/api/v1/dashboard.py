from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
from ...database import get_db
from ...models import TableData
from ...services.llm_models import ClaudeClient
from ...services.utils import generate_data_description

dashboard_router = APIRouter()

@dashboard_router.post("/generate-dashboard", response_model=dict)
async def generate_dashboard(table_data: TableData, db: AsyncSession = Depends(get_db)):
    try:
        # Convert the received data to a pandas DataFrame
        df = pd.DataFrame(table_data.data, columns=table_data.columns)
        
        # Sample the data if it's large
        if len(df) > 1000:
            sample_size = min(1000, int(len(df) * 0.1))
            df_sample = df.sample(n=sample_size, random_state=42)
            is_sample = True
        else:
            df_sample = df
            is_sample = False
        
        # Generate a data description
        data_description = generate_data_description(df_sample)
        
        # Create the prompt for Claude
        prompt = f"""
        You are an expert Python developer specializing in data visualization and Streamlit dashboards.
        Based on the following data description{' (note: this is based on a sample of the full dataset)' if is_sample else ''}, generate a complete, runnable Streamlit dashboard code:

        {data_description}

        The code should:
        1. Import necessary libraries (pandas, streamlit, plotly, etc.)
        2. Load the data (assume it's saved as 'data.csv')
        3. Create appropriate visualizations based on the data types and potential relationships
        4. Organize the visualizations in a clear, user-friendly Streamlit layout
        5. Include any necessary data processing or transformations
        6. Add interactive elements where appropriate (e.g., dropdowns for selecting columns to visualize)
        7. Ensure the code is complete and can be run as-is by the user
        8. If the description is based on a sample, include code to handle potential differences in the full dataset

        Provide only the Python code without any additional explanations.
        """

        # Call Claude API to generate the dashboard code
        claude_client = ClaudeClient()
        dashboard_code = claude_client.generate_response(prompt)
        
        return {"dashboard_code": dashboard_code}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))