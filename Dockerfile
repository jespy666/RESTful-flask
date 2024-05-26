FROM python:3.11

EXPOSE 5000

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
