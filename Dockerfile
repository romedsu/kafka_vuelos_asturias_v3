# imagen oficial de Kafka Connect (basada en Debian)
FROM confluentinc/cp-kafka-connect:7.5.0

USER root
RUN yum install -y gcc python3-devel

RUN confluent-hub install --no-prompt confluentinc/kafka-connect-http:latest

RUN pip3 install --upgrade pip

# librerías de Python desde tu requirements.txt
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# entorno de aplicación
WORKDIR /app
COPY ./src /app
COPY ./schemas /app/schemas