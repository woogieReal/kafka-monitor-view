import json
import time

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

BOOTSTRAP_SERVERS = ["kafka1:9092", "kafka2:9092", "kafka3:9092"]
TOPIC = "system-metrics"


def create_consumer():
    return KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="latest",
    )


if __name__ == "__main__":
    consumer = None
    while consumer is None:
        try:
            consumer = create_consumer()
        except NoBrokersAvailable:
            print("Kafka 브로커에 연결할 수 없습니다. 5초 후 재시도합니다.")
            time.sleep(5)

    print("Consumer 시작. 메시지 대기 중...")
    for message in consumer:
        data = message.value
        cpu_usage = data["metrics"]["cpu_usage"]

        if cpu_usage > 1.0:
            print(f"🚨 CPU 경고! cpu_usage={cpu_usage} | {data}")
        else:
            print(f"수신: {data}")
