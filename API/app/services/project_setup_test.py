# Append this code to the "project_setup.py" file and run it


# Exemplo de uso (para testes locais)
if __name__ == "__main__":
    # Dados de exemplo
    table_data_example = {
        "columns": ["Coluna1", "Coluna2", "Coluna3"],
        "data": [
            ["A1", "B1", "C1"],
            ["A2", "B2", "C2"],
            ["A3", "B3", "C3"],
        ]
    }
    
    dashboard_code_example = """
import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados
df = pd.read_csv('data.csv')

st.title('Dashboard Gerado pelo AutoDash')

# Exibir dados
st.write(df)

# Gráfico de exemplo
fig = px.bar(df, x='Coluna1', y='Coluna2')
st.plotly_chart(fig)
"""
    
    # Arquivos adicionais (opcional)
    additional_files_example = {
        "assets/style.css": """
body {
    font-family: Arial, sans-serif;
}
""",
        "assets/data_description.txt": "Descrição dos dados..."
    }
    
    # Organizar o projeto
    zip_path = organize_project(
        table_data=table_data_example,
        dashboard_code=dashboard_code_example,
        additional_files=additional_files_example
    )
    
    logger.info(f"Projeto organizado e compactado em {zip_path}")
    
    # Opcional: Limpar arquivos temporários após a criação do ZIP
    # cleanup_project("generated_dashboard", zip_path)

