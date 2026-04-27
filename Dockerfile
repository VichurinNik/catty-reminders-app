FROM python:3.14-slim

ARG DEPLOY_REF=unknown
ENV DEPLOY_REF=${DEPLOY_REF}

WORKDIR /app

# Копируем всё
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем uvicorn если его нет в requirements
RUN pip install --no-cache-dir uvicorn

EXPOSE 8181

# Команда для поиска и запуска приложения
CMD ["sh", "-c", "python -c \"import app.main; import uvicorn; uvicorn.run(app.main.app, host='0.0.0.0', port=8181)\" || python -m uvicorn app.main:app --host 0.0.0.0 --port 8181"]
