import time
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

icao24
callsign
pais_origen


# Inicialización del diccionario fuera del bucle
dic_rutas_asturias = {}

# Dentro de tu bucle de consumo de Kafka:
def procesar_vuelo(msg):
    datos = msg.value() # Tu objeto de vuelo
    icao24 = datos.get("icao24")
    callsign = datos.get("callsign")

    # 1. Verificar si ya tenemos el dato en nuestra "Caché"
    if icao24 not in dic_rutas_asturias:
        logging.info(f"Nuevo avión detectado {icao24}. Consultando API...")
        
        # 2. Aquí iría tu función que llama a la API de OpenSky
        info_vuelo = consultar_api_opensky(icao24) 
        
        # 3. Guardar en el diccionario usando callsign como clave única
        dic_rutas_asturias[icao24] = {
            "origen": info_vuelo['origen'],
            "destino": info_vuelo['destino'],
            "timestamp": time.time()
        }
    
    # 4. Enriquecer el mensaje con los datos del diccionario
    datos["origen"] = dic_rutas_asturias[icao24]["origen"]
    datos["destino"] = dic_rutas_asturias[icao24]["destino"]
    
    return datos