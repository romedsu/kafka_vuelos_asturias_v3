import time
import requests
import logging
# import json
# import os
# from kafka import KafkaProducer
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

# BROKER_URL = os.getenv("KAFKA_BROKER", "localhost:9093")
# SCHEMA_REGISTRY_URL = os.getenv("SCHEMA_REGISTRY_URL", "http://localhost:8081")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# CONFIGURACION
TOPIC_NAME = 'datos_api_vuelos_asturias'
BOOTSTRAP_SERVERS = 'kafka:9092'
SCHEMA_REGISTRY_URL = 'http://schema-registry:8081'
API_URL = "http://opensky-network.org/api/states/all?lamin=43.0&lomin=-7.0&lamax=44.0&lomax=-5.0"

# area londres-> pruebas asegurar aviones
# API_URL = "https://opensky-network.org/api/states/all?lamin=50.0&lomin=-2.0&lamax=52.0&lomax=1.0"

logging.info(" Conectando con Kafka...")

# producer = KafkaProducer(
#     bootstrap_servers=[BROKER],
#     api_version=(2, 5, 0),  # versión kafka-python
#     api_version_auto_timeout_ms=10000, # espera
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# cargar schema .avsc
try:
    value_schema = avro.load('./schemas/vuelos_schema.avsc')
except Exception as e:
    logging.error(f"No se pudo cargar el archivo de esquema: {e}")
    exit(1)

producer_conf = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'schema.registry.url': SCHEMA_REGISTRY_URL,
    'compression.type': 'snappy' 
}
try:
    producer = AvroProducer(producer_conf, default_value_schema=value_schema)

    logging.info(f"Conectado con éxito a Kafka ({BOOTSTRAP_SERVERS}) y Schema Registry ({SCHEMA_REGISTRY_URL})")    

except Exception as e:
    logging.error(f"Error al conectar los servicios de mensajería: {e}")
    exit(1)

logging.info(f"Escuchando API de OpenSky (Asturias). Enviando eventos cada 60 segundos...")

while True:
    try:
        # GET a API
        response = requests.get(API_URL, timeout=15)  # 15 segundos de espera máximo
        
        # si respuesta es correcta --> codigo 200
        if response.status_code == 200:
            datos_json = response.json()
            states = datos_json.get("states", [])
            
            if states is None:
                logging.info("Radar activo, pero 0 aviones detectados en el espacio aéreo de Asturias.")
                time.sleep(60)
                continue
                
            logging.info(f"Procesando snapshot. Aviones detectados: {len(states)}")
            
            # Recorremos cada avión para enviarlo de forma individual siguiendo tu esquema
            for avion in states:
                # MAPEO 
                # Extraemos las posiciones exactas de la lista de openSky según tabla
                # Mapeo  basado en el esquema .avsc
                vuelo_mapeado = {
                    "icao24": str(avion[0]),
                    "callsign": str(avion[1]).strip() if avion[1] else None,
                    "latitud": float(avion[6]) if avion[6] else None,
                    "longitud": float(avion[5]) if avion[5] else None,
                    "altitud": float(avion[7]) if avion[7] else None,
                    "velocidad": float(avion[9]) if avion[9] else None,
                    "vertical_rate": float(avion[11]) if avion[11] else None,
                    "en_tierra": bool(avion[8])
                }
                
                # Enviamos el registro validado. El AvroProducer lo convierte a binario antes de enviarlo.
                producer.produce(topic=TOPIC_NAME, value=vuelo_mapeado)
            
            # Forzamos el envío de todo el lote de aviones acumulados
            producer.flush()

            logging.info("¡Éxito! Lote de vuelos validado por Schema Registry e inyectado en Kafka.")
            
        else:
            logging.warning(f"API OpenSky no disponible o límite de peticiones superado. Código HTTP: {response.status_code}")
            
    except Exception as e:
        logging.error(f"Error inesperado en el bucle de datos: {e}")

         
        
    # Espera 1 minuto para la siguiente consulta
    time.sleep(60)
    