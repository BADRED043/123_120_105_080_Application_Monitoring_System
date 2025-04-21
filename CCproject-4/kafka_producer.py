import requests
import json
import time
from kafka import KafkaProducer

# Kafka Producer Setup
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# JSON Server URL
JSON_SERVER_URL = "http://json-server:5000"

# List of log endpoints
TOPIC_ENDPOINTS = [
    "chatbot_logs",
    "sentiment_analysis",
    "chatbot_analytics",
    "error_logs",
    "user_activity"
]

def fetch_and_send_logs():
    for topic in TOPIC_ENDPOINTS:
        try:
            response = requests.get(f"{JSON_SERVER_URL}/{topic}")
            if response.status_code == 200:
                logs = response.json()
                for log in logs:
                    producer.send(topic, value=log)
                    print(f"Sent to {topic}: {log}")
            else:
                print(f"->Failed to fetch logs from {topic}: {response.status_code}")
        except Exception as e:
            print(f"* Error fetching from {topic}: {e}")
    producer.flush()

if __name__ == "__main__":
    print("🚀 Producer is running infinitely. Ctrl+C to stop.")
    try:
        while True:
            fetch_and_send_logs()
            time.sleep(5)  # Simulate delay between log batches
    except KeyboardInterrupt:
        print("* Producer stopped by user.")
    finally:
        producer.close()
        print("*Producer connection closed.")
