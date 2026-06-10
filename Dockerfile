FROM python:3.11-slim

WORKDIR /app

# CORRIGIDO: Removida a cópia do arquivo .env estático
COPY app/ /app/

CMD ["python", "main.py"]