FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["sh", "-c", "while ! nc -z db 5432; do sleep 2; done && python money_manage_Django/manage.py migrate && python money_manage_Django/manage.py runserver 0.0.0.0:8000"]