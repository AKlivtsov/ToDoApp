FROM python:3.12

ENV REDIS_URL=redis://redis PYTHONUNBUFFERED=1

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
EXPOSE 3000
EXPOSE 8000
