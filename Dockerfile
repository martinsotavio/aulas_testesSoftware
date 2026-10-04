FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/projeto

WORKDIR /projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
