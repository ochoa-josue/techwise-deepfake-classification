FROM python:3.11.5-slim

RUN apt-get update \
    && apt-get install -y gcc \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . ./

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
