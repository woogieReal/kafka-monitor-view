import json
import psutil
import socket
from datetime import datetime, timezone

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

BOOTSTRAP_SERVERS = ["kafka:9092"]
TOPIC = "system-metrics"


def create_producer():
    return KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)


def collect_metrics():
    cpu_usage = psutil.cpu_percent(interval=None)
    mem_free_bytes = psutil.virtual_memory().available
    node_id = socket.gethostname()
    return node_id, cpu_usage, mem_free_bytes


def build_message(node_id, cpu_usage, mem_free_bytes):
    return json.dumps({
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "node_id": node_id,
        "metrics": {
            "cpu_usage": cpu_usage,
            "mem_free_bytes": mem_free_bytes,
        },
    }).encode("utf-8")


if __name__ == "__main__":
    import time

    producer = None
    while producer is None:
        try:
            producer = create_producer()
        except NoBrokersAvailable:
            print("Kafka 브로커에 연결할 수 없습니다. 5초 후 재시도합니다.")
            time.sleep(5)

    while True:
        node_id, cpu_usage, mem_free_bytes = collect_metrics()
        message = build_message(node_id, cpu_usage, mem_free_bytes)
        producer.send(TOPIC, value=message)
        producer.flush()
        print(f"발행 완료: {message.decode('utf-8')}")
        time.sleep(1)
