FROM python:3.12-slim


ARG DEPLOY_REF=unknown


ENV DEPLOY_REF=${DEPLOY_REF}

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


RUN mkdir -p /app/logs


EXPOSE 8181


CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8181"]

