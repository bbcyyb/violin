from python:3.7.9

MAINTAINER bbcyyb <bbcyyb@gmail.com>

WORKDIR /app

COPY docker/violin/requirements.txt .
COPY docker/violin/entrypoint.sh .
COPY crawler/ crawler/

RUN pip install -r requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"]
