import os
import shutil
import zipfile
import logging
import pandas as pd
import io

from fastapi import HTTPException
from fastapi.responses import FileResponse

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_project_structure(project_dir="generated_dashboard"):
    """
    Cria a estrutura de diretórios do projeto.
    """
    try:
        directories = [
            project_dir,
            os.path.join(project_dir, "assets"),
            # Adicione mais diretórios conforme necessário
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Criado diretório: {directory}")
        
        return project_dir
    except Exception as e:
        logger.exception("Erro ao criar a estrutura do projeto")
        raise

def write_file(content, path):
    """
    Escreve o conteúdo em um arquivo específico.
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Arquivo criado: {path}")
    except Exception as e:
        logger.exception(f"Erro ao escrever no arquivo {path}")
        raise

def generate_requirements():
    """
    Gera o conteúdo do requirements.txt.
    """
    dependencies = [
        "pandas",
        "streamlit",
        "plotly",
        "numpy",
        "wordcloud"
        # Adicione outras dependências conforme necessário
    ]
    
    # Adicionar dependências específicas geradas pelo modelo AI
    # Por exemplo, se o código do dashboard usa outras bibliotecas:
    # dependencies.append("biblioteca_especifica")
    
    requirements_content = "\n".join(dependencies)
    return requirements_content

def save_data_csv(table_data, output_path):
    """
    Salva os dados do usuário em um arquivo CSV.
    """
    try:
        df = pd.DataFrame(table_data['data'], columns=table_data['columns'])
        df.to_csv(output_path, index=False)
        logger.info(f"Dados salvos em {output_path}")
    except Exception as e:
        logger.exception(f"Erro ao salvar dados em {output_path}")
        raise

def save_readme(project_dir):
    """
    Cria um arquivo README.md com instruções básicas.
    """
    readme_content ="""
    # AutoDash Generated Dashboard

    Este projeto foi gerado automaticamente pelo [**AutoDash**](https://github.com/luucaslfs/AutoDash/).

    ## Como Instalar

    1. **Clone o repositório** (caso esteja hospedado em um repositório Git):

        ```bash
        git clone https://github.com/seu-usuario/seu-repositorio.git
        cd seu-repositorio
        ```

    2. **Instale as dependências**:

        ```bash
        pip install -r requirements.txt
        ```

    ## Como Rodar

    Execute o dashboard Streamlit com o seguinte comando:

    ```bash
    streamlit run app.py
    ```

    O dashboard estará disponível para acessar no seu navegador (veja o link no console).
    """

    readme_path = os.path.join(project_dir, "README.md") 
    write_file(readme_content, readme_path)

def add_additional_files(project_dir, additional_files):
    """
    Adiciona arquivos adicionais na estrutura do projeto.

    :param project_dir: Diretório principal do projeto.
    :param additional_files: Dicionário com caminho relativo e conteúdo dos arquivos.
    """
    try:
        for relative_path, content in additional_files.items():
            full_path = os.path.join(project_dir, relative_path)
            # Certifique-se de que o diretório existe
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            write_file(content, full_path)
            logger.info(f"Arquivo adicional criado: {full_path}")
    except Exception as e:
        logger.exception("Erro ao adicionar arquivos adicionais")
        raise


def create_project_zip(project_dir, zip_name="dashboard_project.zip"):
    """
    Compacta a pasta do projeto em um arquivo ZIP.

    :param project_dir: Diretório principal do projeto.
    :param zip_name: Nome do arquivo ZIP a ser criado.
    :return: Caminho para o arquivo ZIP criado.
    """
    try:
        zip_path = os.path.join(project_dir, zip_name)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(project_dir):
                for file in files:
                    if file == zip_name:
                        continue  # Evita adicionar o ZIP dentro dele mesmo
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, project_dir))
        logger.info(f"Arquivo ZIP criado: {zip_path}")
        return zip_path
    except Exception as e:
        logger.exception("Erro ao criar o arquivo ZIP")
        raise

def cleanup_project(project_dir, zip_path):
    """
    Remove a pasta do projeto e o arquivo ZIP após o download.

    :param project_dir: Diretório principal do projeto.
    :param zip_path: Caminho para o arquivo ZIP.
    """
    try:
        shutil.rmtree(project_dir)
        logger.info(f"Diretório {project_dir} removido após criação do ZIP")
        os.remove(zip_path)
        logger.info(f"Arquivo ZIP {zip_path} removido após download")
    except Exception as e:
        logger.warning(f"Erro ao limpar arquivos temporários: {e}")


def save_data_csv_string(table_data):
    """
    Salva os dados do usuário em um objeto StringIO (em memória).

    :param table_data: Dicionário contendo 'columns' e 'data'.
    :return: String contendo os dados em formato CSV.
    """
    try:
        df = pd.DataFrame(table_data['data'], columns=table_data['columns'])
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        logger.info("Dados CSV salvos em memória")
        return csv_buffer.getvalue()
    except Exception as e:
        logger.exception("Erro ao salvar dados em memória")
        raise


def organize_project(table_data, dashboard_code, additional_files=None, project_dir="generated_dashboard"):
    """
    Organiza os arquivos do projeto criando a estrutura de diretórios e adicionando os arquivos.

    :param table_data: Dicionário contendo 'columns' e 'data' para o CSV.
    :param dashboard_code: Código do dashboard gerado pelo AI.
    :param additional_files: Dicionário opcional com caminhos e conteúdos de arquivos adicionais.
    :param project_dir: Nome do diretório do projeto.
    :return: Caminho para o arquivo ZIP criado.
    """
    try:
        # 1. Criar a estrutura de diretórios
        create_project_structure(project_dir)

        # 2. Escrever o código do dashboard
        app_py_path = os.path.join(project_dir, "app.py")
        write_file(dashboard_code, app_py_path)

        # 3. Gerar e escrever requirements.txt
        requirements = generate_requirements()
        requirements_path = os.path.join(project_dir, "requirements.txt")
        write_file(requirements, requirements_path)

        # 4. Salvar dados como data.csv
        data_csv_path = os.path.join(project_dir, "data.csv")
        save_data_csv(table_data, data_csv_path)

        # 5. Criar README.md
        save_readme(project_dir)

        # 6. Adicionar arquivos adicionais se houver
        if additional_files:
            add_additional_files(project_dir, additional_files)

        # 7. Criar arquivo ZIP
        zip_path = create_project_zip(project_dir)

        return zip_path
    except Exception as e:
        logger.exception("Erro ao organizar o projeto")
        raise