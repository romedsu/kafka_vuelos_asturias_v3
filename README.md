# Sistema de Ingesta de Datos en Tiempo Real (kafka_connects + Kafka + Postgres) --> V3

## Sistema de ingesta de datos a través de un pipeline de procesamiento de datos en streaming en tiempo real, desplegado sobre Docker a través de Apache Kafka y PostgreSQL.

## A través de kafka connect se realiza ingesrta de datos , captar el evento y registrarlo en la BBDD de Postgre.



## VER LISTA TOPICS creados
```docker exec kafka kafka-topics --list --bootstrap-server localhost:9092```

## LOGS (servicio)
```docker logs -f [servicio] ```

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

## CONECTOR confluent HTTP JSON
```
$json = @{
    name = "asturias-flights-source"
    config = @{
        "connector.class" = "io.confluent.connect.http.HttpSourceConnector"
        "tasks.max" = "1"
        "url" = "https://opensky-network.org/api/states/all?lamin=43.0&lomin=-7.0&lamax=44.0&lomax=-5.0"
        "topic.name.pattern" = "vuelos-asturias-raw"
        "http.timer.interval" = "60000"
        "confluent.topic.bootstrap.servers" = "kafka:9092"
        "confluent.topic.replication.factor" = "1"
        "value.converter" = "org.apache.kafka.connect.json.JsonConverter"
        "value.converter.schemas.enable" = "false"
        "http.offset.mode" = "SIMPLE_INCREMENTING"
        "http.initial.offset" = "0"
        "http.increment.column" = "timestamp"
        "confluent.license" = ""
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "http://localhost:8083/connectors-plugins" -Method Post -Body $json -ContentType "application/json"

 ```
 ## LISTAS CONECTORES
 Invoke-RestMethod -Uri "http://localhost:8083/connectors-plugins" -Method Get


## BORRAR CONECTOR
Invoke-RestMethod -Uri "http://localhost:8083/connectors-plugins/asturias-flights-source" -Method Delete


 # ESTADO CONECTOR
 Invoke-RestMethod -Uri "http://localhost:8083/connectors-plugins/asturias-flights-source/status" -Method Get | ConvertTo-Json


 <!-- CONECTOR VUELOS ATURIAS -->
