FROM python:3

RUN apt-get update && apt-get -y install netcat && apt-get clean

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY config.yaml ./
COPY run.sh ./

COPY access/service.py ./
COPY access/secret.py ./
COPY access/authorization.py ./

RUN chmod +x ./run.sh

CMD ["./run.sh"]