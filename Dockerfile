FROM python:3.14-slim

# Аргумент для передачи из GitHub Actions
ARG DEPLOY_REF=unknown

WORKDIR /catty-reminders-app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY static/ ./static/
COPY templates/ ./templates/
COPY config.json .

# Создаём скрипт, который заменяет {{ deploy_ref }} на реальный DEPLOY_REF
RUN echo '#!/bin/bash\n\
if [ "$DEPLOY_REF" != "unknown" ] && [ "$DEPLOY_REF" != "" ]; then\n\
    echo "Replacing {{ deploy_ref }} with $DEPLOY_REF in HTML files"\n\
    find /catty-reminders-app/templates -name "*.html" -exec sed -i "s/{{ deploy_ref }}/$DEPLOY_REF/g" {} \;\n\
fi\n\
exec uvicorn app.main:app --host 0.0.0.0 --port 8181' > /start.sh && chmod +x /start.sh

EXPOSE 8181

CMD ["/start.sh"]
