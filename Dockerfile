FROM python:3.10-slim

COPY requirements.txt ./requirements.txt
RUN pip3 install -r ./requirements.txt --no-cache-dir

COPY . /app

WORKDIR /app/src

ENTRYPOINT ["/app/entrypoint.sh"]
