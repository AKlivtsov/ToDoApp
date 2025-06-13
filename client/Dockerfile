FROM python:3.12

ENV REDIS_URL=redis://redis
ENV PYTHONUNBUFFERED=1
ENV TODOAPP_SERVER_HOST=aklivtsovcloud.ru
ENV TODOAPP_SERVER_PORT=9777

WORKDIR /client
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["reflex", "run", "--env", "prod", "--loglevel", "debug" ]
