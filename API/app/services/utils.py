from http.client import HTTPException
import anthropic
import httpx
import os

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = os.getenv("CLAUDE_API_URL")

def generate_data_description(df):
    description = []
    description.append(f"The dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")
    description.append("\nColumns and their data types:")
    for col in df.columns:
        description.append(f"- {col}: {df[col].dtype}")
    
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_columns = df.select_dtypes(include=['object']).columns
    
    if len(numeric_columns) > 0:
        description.append("\nNumeric columns:")
        for col in numeric_columns:
            description.append(f"- {col}: min={df[col].min()}, max={df[col].max()}, mean={df[col].mean():.2f}")
    
    if len(categorical_columns) > 0:
        description.append("\nCategorical columns:")
        for col in categorical_columns:
            description.append(f"- {col}: {df[col].nunique()} unique values")
    
    return "\n".join(description)

