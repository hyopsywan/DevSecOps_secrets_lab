FROM python:3.11-slim

WORKDIR /app

# Copia apenas o código da aplicação
COPY app/ /app/

CMD ["python", "main.py"]