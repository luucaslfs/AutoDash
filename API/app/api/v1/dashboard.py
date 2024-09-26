from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import pandas as pd
from ...database import get_db
from ...models import GenerateDashboardRequest, AIModelEnum, DownloadDashboardRequest, TableData
from ...services.llm_models import ClaudeClient, OpenAIClient 
from ...services.utils import generate_data_description, fake_code
from ...services.project_setup import organize_project, cleanup_project
from ...services.state_manager import get_dashboard_code, store_dashboard_code, get_table_data
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
        {df_sample.to_csv(index=False)}
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
        
        logger.info("Prompt criado para geração do dashboard")
        logger.debug(f"Prompt: {prompt}")
        
        # Instanciar o cliente de IA apropriado
        if model_choice == AIModelEnum.CLAUDE:
            client = ClaudeClient()
            logger.info("Usando ClaudeClient para gerar o código do dashboard")
        elif model_choice == AIModelEnum.OPENAI:
            client = OpenAIClient()
            logger.info("Usando OpenAIClient para gerar o código do dashboard, Prompt: {prompt}")
        else:
            raise ValueError(f"Escolha de modelo não suportada: {model_choice}")
        
        # Chamar o cliente de IA para gerar o código do dashboard
        dashboard_code = fake_code()
        #dashboard_code = client.generate_response(prompt)
        logger.info("Dashboard code gerado com sucesso")
         
        # Armazenar o código gerado e obter um UUID
        unique_id = store_dashboard_code(dashboard_code, preview_data=table_data)
        logger.info(f"Dashboard code armazenado com UUID: {unique_id}")
        
        # Retornar o código e o UUID para o frontend
        return {
            "unique_id": unique_id,
            "dashboard_code": dashboard_code
        }
    except Exception as e:
        logger.exception("Erro em generate_dashboard")
        raise HTTPException(status_code=400, detail=str(e))

@dashboard_router.post("/download-dashboard")
def download_dashboard(
    request: DownloadDashboardRequest, 
    background_tasks: BackgroundTasks
):
    try:
        unique_id = request.unique_id

        logger.info(f"Request to download dashboard with unique_id: {unique_id}")
        
        # Recuperar o código do dashboard associado ao unique_id
        dashboard_code = get_dashboard_code(unique_id)
        if not dashboard_code:
            raise HTTPException(status_code=404, detail="Dashboard not found or has expired.")
        
        # Recuperar os dados associados ao unique_id
        table_data = get_table_data(unique_id)
        if not table_data:
            raise HTTPException(status_code=404, detail="Table data not found for the provided unique_id.")
        
         # Garantir que table_data é um objeto TableData
        if not isinstance(table_data, TableData):
            table_data = TableData(columns=table_data['columns'], data=table_data['data'])
        
        # Definir arquivos adicionais
        additional_files = {
            "assets/style.css": """
            body {
                font-family: Arial, sans-serif;
            }
            """,
            "assets/data_description.txt": "Descrição dos dados..."
        }
        
        # Organizar o projeto e criar ZIP
        project_dir = f"generated_dashboard_{unique_id}"
        zip_path = organize_project(
            table_data=table_data,
            dashboard_code=dashboard_code,
            additional_files=additional_files,
            project_dir=project_dir
        )
        
        logger.info(f"Projeto organizado em {zip_path}")
        
        # Adicionar tarefa de limpeza ao background
        background_tasks.add_task(cleanup_project, project_dir, zip_path)
        
        # Retornar o arquivo ZIP como resposta
        return FileResponse(path=zip_path, filename="dashboard_project.zip", media_type='application/zip')
        
    except HTTPException as he:
        logger.exception("Erro em download_dashboard")
        raise he
    except Exception as e:
        logger.exception("Erro em download_dashboard")
        raise HTTPException(status_code=400, detail=str(e))
