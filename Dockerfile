#Dockerfile
FROM python:3.11-slim-bullseye

COPY server server

COPY server/requirements.txt . 

RUN pip install -r requirements.txt

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8008"]