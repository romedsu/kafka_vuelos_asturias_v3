# Sistema de Ingesta de Datos en Tiempo Real (kafka_connects + Kafka + Postgres) --> V3

## Sistema de ingesta de datos a través de un pipeline de procesamiento de datos en streaming en tiempo real, desplegado sobre Docker a través de Apache Kafka y PostgreSQL.

## A través de kafka connect se realiza ingesrta de datos , captar el evento y registrarlo en la BBDD de Postgre.



## VER LISTA TOPICS creados
```docker exec kafka_docker_v2-kafka-1 kafka-topics --list --bootstrap-server localhost:9092```

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