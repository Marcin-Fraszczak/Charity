FROM python:3.11.2-alpine

WORKDIR /app
COPY . /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt && \
    python manage.py migrate && \
#    pytest > log.txt && \
    python scripts.py > log.txt && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8000

ENTRYPOINT cat log.txt && python manage.py runserver 0.0.0.0:8000
