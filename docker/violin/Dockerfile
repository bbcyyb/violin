from python:3.7.9-alpine3.12

MAINTAINER bbcyyb <bbcyyb@gmail.com>

WORKDIR /app

COPY requirements.txt .
COPY entrypoint.sh .
COPY ../../crawler .

RUN pip install -r requirements.txt