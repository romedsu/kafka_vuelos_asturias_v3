import time
import requests
import json
import logging
from kafka import KafkaProducer
import os

BROKER = os.getenv("KAFKA_BROKER", "localhost:9093")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# CONFIGURACION
TOPIC_NAME = 'datos_api_vuelos_asturias'
BOOTSTRAP_SERVERS = ['localhost:9093']
API_URL = "http://opensky-network.org/api/states/all?lamin=43.0&lomin=-7.0&lamax=44.0&lomax=-5.0"

logging.info(" Conectando con Kafka...")

producer = KafkaProducer(
    bootstrap_servers=[BROKER],
    api_version=(2, 5, 0),  # versión kafka-python
    api_version_auto_timeout_ms=10000, # espera
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

logging.info(f" Escuchando la API de Asturias. Enviando datos al tópico '{TOPIC_NAME}' cada 60 segundos...")

while True:
    try:
        # GET a API
        response = requests.get(API_URL, timeout=10)  # 10 segundos de espera máximo
        
        # si respuesta es correcta --> codigo 200
        if response.status_code == 200:
            datos_json = response.json()
            
            # Enviamos el JSON directo a Kafka 
            producer.send(TOPIC_NAME, value=datos_json)

            producer.flush()

            logging.info(f" [{time.strftime('%H:%M:%S')}] CORRECTO. Datos del vuelo inyectados en Kafka.")
        else:
            logging.info(f" Propia API caída o límite excedido. Código HTTP: {response.status_code}")
            
    except Exception as e:
        logging.info(f" Error de conexión: {e}")
        
    # Espera 1 minuto para la siguiente consulta
    time.sleep(60)