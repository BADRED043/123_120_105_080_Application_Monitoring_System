# 📌 Application Monitoring System

- This project implements a containerized application monitoring system that leverages Apache Kafka, Grafana Loki, and Docker for scalable log processing and real-time monitoring.

## ✨ Key Components

## Dockerized Infrastructure:

- All services (Kafka broker, Zookeeper, Loki, and supporting components) run in isolated containers using Docker and Docker Compose for easy setup and scalability.

## Kafka Producer (Python):

- A Python script generates and sends synthetic or real-time application logs to Kafka topics.
- Supports JSON-formatted logs for structured processing.

## Kafka Consumer (Python):

- A Python service consumes log data from Kafka topics.
- Parses, filters, and forwards relevant logs to Loki for centralized storage and querying.

## Loki Integration:

- Logs from Kafka are shipped to Loki, enabling fast, cost-efficient log indexing.
- Compatible with Grafana for visualization and monitoring.

## Visualization:

- Logs stored in Loki are queried and visualized through Grafana dashboards for real-time insights into application performance, errors, and operational metrics.

## ⚙️ Tech Stack

- Containerization: Docker, Docker Compose
- Messaging: Apache Kafka, Zookeeper
- Log Aggregation: Loki
- Programming Language: Python (Kafka Producer & Consumer)

## Visualization: Grafana

- Real-time log collection from distributed applications.
- Centralized storage and querying of application logs.
- Scalable log processing pipeline for monitoring, alerting, and troubleshooting.
