from http.client import HTTPException
import os

def generate_data_description(df):
    description = []
    description.append(f"O dataset contém {df.shape[0]} linhas e {df.shape[1]} colunas.")
    description.append("\nColunas e seus tipos de dados:")
    for col in df.columns:
        description.append(f"- {col}: {df[col].dtype}")
    
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns
    
    if len(numeric_columns) > 0:
        description.append("\nColunas Numéricas:")
        for col in numeric_columns:
            description.append(
                f"- {col}: min={df[col].min()}, max={df[col].max()}, média={df[col].mean():.2f}, "
                f"mediana={df[col].median()}, desvio padrão={df[col].std():.2f}, "
                f"valores ausentes={df[col].isnull().sum()}"
            )
    
    if len(categorical_columns) > 0:
        description.append("\nColunas Categóricas:")
        for col in categorical_columns:
            description.append(
                f"- {col}: {df[col].nunique()} valores únicos, "
                f"valores ausentes={df[col].isnull().sum()}"
            )
    
    # Adicionando correlação para colunas numéricas
    if len(numeric_columns) > 1:
        corr_matrix = df[numeric_columns].corr().to_dict()
        description.append("\nCorrelação entre colunas numéricas:")
        for col1 in numeric_columns:
            for col2 in numeric_columns:
                if col1 != col2 and col2 not in description[-1]:
                    corr_value = corr_matrix[col1][col2]
                    description.append(f"- Correlação entre {col1} e {col2}: {corr_value:.2f}")
                    break  # Para evitar repetições
    
    # Informações adicionais
    description.append("\nResumo geral:")
    description.append(f"- Total de valores ausentes no dataset: {df.isnull().sum().sum()}")
    
    return "\n".join(description)