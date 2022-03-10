from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = "localhost:9093"
KAFKA_SECURITY_PROTOCOL = False


def run():
    local_conf = {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "group.id": "mygroup",
        "auto.offset.reset": "earliest",
    }
    if KAFKA_SECURITY_PROTOCOL:
        local_conf["security.protocol"] = "SSL"

    consumer = KafkaConsumer(
        "test.output.topic",
        group_id="mygroup",
        bootstrap_servers=BOOTSTRAP_SERVERS,
    )
    for msg in consumer:
        print(msg)


if __name__ == '__main__':
    run()
