FROM python:3.11-slim

WORKDIR /app

# ERRO CRÍTICO: Copiando segredos locais para dentro da imagem final
COPY .env /app/.env
COPY app/ /app/

CMD ["python", "main.py"]