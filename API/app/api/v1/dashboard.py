from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import pandas as pd
from ...database import get_db
from ...models import TableData
from ...services.llm_models import ClaudeClient
from ...services.utils import generate_data_description
import logging

logger = logging.getLogger(__name__)

dashboard_router = APIRouter()

@dashboard_router.post("/generate-dashboard", response_model=dict)
def generate_dashboard(table_data: TableData, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received data: columns={len(table_data.columns)}, data_length={len(table_data.data)}")
        
        # Validate that all rows have the same number of columns
        row_lengths = [len(row) for row in table_data.data]
        if len(set(row_lengths)) > 1:
            raise ValueError(f"Inconsistent number of columns in rows. Found lengths: {set(row_lengths)}")
        
        if len(table_data.columns) != row_lengths[0]:
            raise ValueError(f"Mismatch between number of columns ({len(table_data.columns)}) and data ({row_lengths[0]})")
        
        # Convert the received data to a pandas DataFrame
        df = pd.DataFrame(table_data.data, columns=table_data.columns)
        logger.info(f"Created DataFrame with shape: {df.shape}")
        
        # Sample the data if it's large
        if len(df) > 1000:
            sample_size = min(1000, int(len(df) * 0.1))
            df_sample = df.sample(n=sample_size, random_state=42)
            is_sample = True
        else:
            df_sample = df
            is_sample = False
        
        logger.info(f"Using {'sampled' if is_sample else 'full'} data with shape: {df_sample.shape}")
        
        # Generate a data description
        data_description = generate_data_description(df_sample)
        logger.info("Generated data description")
        
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

        logger.info("Calling Claude API to generate dashboard code")
        # Call Claude API to generate the dashboard code
        claude_client = ClaudeClient()
        dashboard_code = claude_client.generate_response(prompt)
        
        logger.info("Successfully generated dashboard code")
        return {"dashboard_code": dashboard_code}
    except Exception as e:
        logger.exception("Error in generate_dashboard")
        raise HTTPException(status_code=400, detail=str(e))