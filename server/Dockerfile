FROM python:3.12.3-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

ENV SERVER_ADDRESS="0.0.0.0:8080"
ENV DATABASE_URL="postgresql://aklivtsov:122365@aklivtsovcloud.ru:5432/main"
ENV REDIS_HOST="aklivtsovcloud.ru"
ENV REDIS_PORT="6379"

CMD [ "python", "main.py"]
