# imagen oficial de Kafka Connect (basada en Debian)
# FROM confluentinc/cp-kafka-connect:7.5.0

# # USER root
# # RUN yum install -y gcc python3-devel

# # carpeta específica para plugin connect http
# # RUN mkdir -p /usr/share/java/plugins
# # RUN mkdir -p /usr/share/java/kafka-connect-http

# # ENV CONNECT_PLUGIN_PATH=/usr/share/java
# # RUN confluent-hub install --no-prompt confluentinc/kafka-connect-http:latest
# # RUN confluent-hub install --no-prompt --component-dir /usr/share/filestream-connectors confluentinc/kafka-connect-http:latest
# RUN confluent-hub install --no-prompt confluentinc/kafka-connect-http:latest

# # CREAR ENTORNO VIRTUAL (aisla dependencias del sistema)
# # RUN python3 -m venv /opt/venv
# # ENV PATH="/opt/venv/bin:$PATH"

# # librerías de Python desde tu requirements.txt
# COPY requirements.txt .

# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt --ignore-installed

# # entorno de aplicación
# WORKDIR /app
# COPY ./src /app
# COPY ./schemas /app/schemas

FROM confluentinc/cp-kafka-connect:7.5.0

USER root

# Instalar conector HTTP desde Confluent Hub
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-http:latest
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-http-source:latest