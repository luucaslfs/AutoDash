#!/bin/bash

echo "Executando migrações do Alembic (Inicializando Base de Dados)..."
alembic upgrade head

echo "Iniciando a aplicação..."
uvicorn app.main:app --host 0.0.0.0 --port 8080