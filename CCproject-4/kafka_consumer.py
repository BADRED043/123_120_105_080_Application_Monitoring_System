import json
import requests
import time
from kafka import KafkaConsumer
from datetime import datetime

# Kafka Consumer Setup
consumer = KafkaConsumer(
    'chatbot_logs', 'sentiment_analysis', 'chatbot_analytics', 'error_logs', 'user_activity',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
print("-->> Kafka consumer initialized")

# Loki HTTP endpoint
LOKI_URL = "http://loki:3100/loki/api/v1/push"

def send_to_loki(log, topic):
    loki_payload = {
        "streams": [
            {
                "stream": {
                    "job": topic,
                    "level": log.get("level", "info"),
                    "user": log.get("user_id", "unknown")
                },
                "values": [[str(int(time.time() * 1e9)), json.dumps(log)]]
            }
        ]
    }

    for attempt in range(3):
        try:
            response = requests.post(LOKI_URL, json=loki_payload, timeout=5)
            if response.status_code == 204:
                print(f"-->> Sent log to Loki for {topic}: {log}")
                return
            else:
                print(f"\/\/ Attempt {attempt+1}: Failed to send log: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"\/\/ Attempt {attempt+1}: Error sending log to Loki: {e}")
        time.sleep(2)

# 🧠 Topic-wise processing logic
def process_log(topic, log):
    if topic == "sentiment_analysis":
        label = log.get("sentiment", "").lower()
        score_map = {"positive": 1, "neutral": 0, "negative": -1}
        log["sentiment_score"] = score_map.get(label, 0)

    elif topic == "chatbot_logs":
        if "event" in log and log["event"] == "Bot response":
            log["response_type"] = "bot"
        elif "event" in log and log["event"] == "User message":
            log["response_type"] = "user"
        log["text_length"] = len(log.get("text", ""))

    elif topic == "chatbot_analytics":
        total = log.get("total_messages", 0)
        users = log.get("unique_users", 1)
        log["avg_msgs_per_user"] = round(total / users, 2) if users else 0

    elif topic == "user_activity":
        action = log.get("action", "").lower()
        log["session_flag"] = 1 if action == "login" else -1

    return log

print("-> Listening for messages...")
for msg in consumer:
    print(f"-|| Received from {msg.topic}: {msg.value}")

    processed_log = process_log(msg.topic, msg.value)
    send_to_loki(processed_log, msg.topic)
