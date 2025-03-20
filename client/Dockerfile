FROM python:3.12.3

ENV REDIS_URL=redis://redis PYTHONUNBUFFERED=1

WORKDIR /client
COPY . .

RUN pip install -r requirements.txt
