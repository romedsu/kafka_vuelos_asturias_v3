# kafka_vuelos_asturias_v3

## Sistema de Ingesta de Datos en Tiempo Real (API opensky + python producer + Kafka + ksqlDB + Postgres) --> V3

### Sistema de ingesta de datos a través de un pipeline de procesamiento de datos en streaming en tiempo real, desplegado sobre Docker a través de Apache Kafka y PostgreSQL.

## A partir de la API Opensky, se realiza ingesta de datos a traves de producer (python) , capta el evento y envío al broker de kafka para registrarlo en la BBDD de Postgre.

[OpenSky](https://openskynetwork.github.io/opensky-api/rest.html)




## VER LISTA TOPICS creados
` docker exec kafka kafka-topics --list --bootstrap-server localhost:9092 `

## LOGS (servicio)
` docker logs -f [servicio] `

## CONSULTA BBDD
```docker exec -it postgres psql -U admin -d transacciones_db -c "SELECT * FROM transacciones;"```

---
## ORDEN SECUENCIA ARRANQUE
healthcheck --> comprobar que cada servicio ha arrancado correctamente y devuelve respuesta

1. ZooKeeper: Es el primero. Sin él, Kafka no arranca.

2. Kafka: Espera a zookeeper.

3. Schema Registry: Espera a kafka (usando healthcheck).

4. Base de Datos (Postgres): Puede arrancar en paralelo a Kafka.



## SQL --> init-scripts--> scripts .sql de creación tablas de bbdd


## SCHEMA REGISTRY --> Data Governance --> Garantizar formato correcto de los datos --> AVRO .avsc


## KAFKA CONNECT --> comprobar
``` Invoke-RestMethod -Uri "http://localhost:8083/connector-plugins" -Method Get ```

``` Invoke-RestMethod -Uri "http://localhost:8083/connector-plugins" -Method Get | ConvertTo-Json ```

```curl.exe http://localhost:8083/connector-plugins   ```

## comprobar plugin http
``` docker exec -it kafka-connect bash ```
``` ls /usr/share/confluent-hub-components ```

--

# crear requiremnets.txt
pip freeze > requirements.txt

# instalar requirements
pip install -r requirements.txt

 python -m venv venvPython
 .\venvPython\Scripts\activate


## CONECTORES HTTP
 ## LISTAS CONECTORES
Invoke-RestMethod -Uri "http://localhost:8083/connector-plugins" -Method Get


## BORRAR CONECTOR
Invoke-RestMethod -Uri "http://localhost:8083/connector-plugins/asturias-flights-source" -Method Delete


 # ESTADO CONECTOR
 Invoke-RestMethod -Uri "http://localhost:8083/connectors-plugins/asturias-flights-source/status" -Method Get | ConvertTo-Json



 ## CONSUMER
  docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic datos_api_vuelos_asturias --from-beginning



## ksqlDB CLI (consola)
docker exec -it ksqldb-cli ksql http://ksqldb-server:8088

## registrar topic
CREATE STREAM VUELOS_STREAM WITH (
  KAFKA_TOPIC='datos_api_vuelos_asturias', 
  VALUE_FORMAT='AVRO'
);


## verificar conexion
SHOW STREAMS;

## consulta basica
### EMIT CHANGES --> queda escuchando para ir actualizando cada evz que se modifique el evento
SELECT icao24, latitud, longitud, velocidad 
FROM VUELOS_STREAM 
WHERE velocidad > 300 
EMIT CHANGES;

SELECT *
FROM VUELOS_STREAM
EMIT CHANGES;

## contador
SELECT icao24, COUNT(*) AS mensajes_recibidos
FROM VUELOS_STREAM
GROUP BY icao24
EMIT CHANGES;

## PANDAS --> rutas ASTURIAS (OVD) --> /_data/pandas
#### Filtrado y limpieda de dataset de rutas para obtener solo las de Asturias (rutas desactualizadas)


