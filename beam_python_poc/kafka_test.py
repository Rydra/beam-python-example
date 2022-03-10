import uuid


KAFKA_SECURITY_PROTOCOL = False


from typing import Dict

from confluent_kafka import Producer
import json
import sys


class KafkaMessageProducer:
    def __init__(self, config: Dict) -> None:
        self.producer = Producer(config)

    def send_message(self, topic: str, key: str, payload: Dict) -> None:
        value = json.dumps(payload)
        try:
            self.producer.produce(topic, key=key, value=value)
            self.producer.flush(30)
        except Exception:
            print("Unexpected error:", sys.exc_info()[0])
            raise


def send_request_to_kafka(request: Dict, topic: str) -> None:
    conf = {
        "bootstrap.servers": "localhost:9093",
    }
    if KAFKA_SECURITY_PROTOCOL:
        conf["security.protocol"] = "SSL"

    kafka_producer = KafkaMessageProducer(conf)
    process_id = str(uuid.uuid4())
    request["metadata"] = {"correlation_id": process_id}
    kafka_producer.send_message(
        topic=topic,
        key=process_id,
        payload=request,
    )


if __name__ == "__main__":
    for i in range(1):
        send_request_to_kafka(
            {
                "analysis_id": "1",
                "treaty_id": "1",
            },
            "test.source.topic",
        )
