from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import pandas as pd
from ...database import get_db
from ...models import GenerateDashboardRequest, AIModelEnum
from ...services.llm_models import ClaudeClient, OpenAIClient 
from ...services.utils import generate_data_description
import logging

logger = logging.getLogger(__name__)

dashboard_router = APIRouter()

@dashboard_router.post("/generate-dashboard", response_model=dict)
def generate_dashboard(request: GenerateDashboardRequest, db: Session = Depends(get_db)):
    try:
        table_data = request.table_data
        model_choice = request.model
        logger.info(f"Received data: columns={len(table_data.columns)}, data_length={len(table_data.data)}, model={model_choice}")
        
        # Validação do número de colunas
        row_lengths = [len(row) for row in table_data.data]
        if len(set(row_lengths)) > 1:
            raise ValueError(f"Inconsistent number of columns in rows. Found lengths: {set(row_lengths)}")
        
        if len(table_data.columns) != row_lengths[0]:
            raise ValueError(f"Mismatch between number of columns ({len(table_data.columns)}) and data ({row_lengths[0]})")
        
        # Conversão para DataFrame
        df = pd.DataFrame(table_data.data, columns=table_data.columns)
        logger.info(f"Created DataFrame with shape: {df.shape}")
        
        # Amostragem se necessário
        if len(df) > 1000:
            sample_size = min(1000, int(len(df) * 0.2))
            df_sample = df.sample(n=sample_size, random_state=42)
            is_sample = True
        else:
            df_sample = df
            is_sample = False
        
        logger.info(f"Using {'sampled' if is_sample else 'full'} data with shape: {df_sample.shape}")
        
        # Geração da descrição dos dados
        data_description = generate_data_description(df)
        logger.info("Generated data description")
        
        # Criação do prompt
        prompt = f"""
        Você é um desenvolvedor Python especialista em visualização de dados e dashboards com Streamlit.
        Com base na seguinte descrição dos dados, gere um código completo e executável para um dashboard em Streamlit:

        {data_description}

        Dados{' (nota: esta é uma amostra do dataset completo)' if is_sample else ''}:
        ```csv
        {df_sample}
        ```

        O código deve:
        1. Importar as bibliotecas necessárias (pandas, streamlit, plotly, etc.)
        2. Carregar os dados (assuma que estão salvos como 'data.csv')
        3. Criar visualizações apropriadas com base nos tipos de dados e possíveis relacionamentos
        4. Organizar as visualizações em um layout claro e amigável no Streamlit
        5. Incluir qualquer processamento ou transformação de dados necessária
        6. Adicionar elementos interativos onde apropriado (por exemplo, dropdowns para selecionar colunas a serem visualizadas)
        7. Garantir que o código esteja completo e possa ser executado diretamente pelo usuário
        8. Se a descrição for baseada em uma amostra, incluir código para lidar com possíveis diferenças no dataset completo

        Forneça apenas o código Python sem explicações adicionais.
        """
        
        logger.info(f"Prompt criado: {prompt}")
        
        # Instanciar o cliente de IA apropriado
        if model_choice == AIModelEnum.CLAUDE:
            client = ClaudeClient()
            logger.info("Usando ClaudeClient para gerar o código do dashboard")
        elif model_choice == AIModelEnum.OPENAI:
            client = OpenAIClient()
            logger.info("Usando OpenAIClient para gerar o código do dashboard")
        else:
            raise ValueError(f"Escolha de modelo não suportada: {model_choice}")
        
        # Chamar o cliente de IA para gerar o código do dashboard
        dashboard_code = client.generate_response(prompt)
        
        logger.info("Dashboard code gerado com sucesso")
        return {"dashboard_code": dashboard_code}
    except Exception as e:
        logger.exception("Erro em generate_dashboard")
        raise HTTPException(status_code=400, detail=str(e))

