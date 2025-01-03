#!/usr/bin/env python3

from confluent_kafka import Consumer

if __name__ == '__main__':

    config = {
        # User-specific properties that you must set
        'bootstrap.servers': 'localhost:9092',
        # 'sasl.username':     'docker',
        # 'sasl.password':     'docker',

        # # Fixed properties
        # 'security.protocol': 'SASL_SSL',
        'sasl.mechanisms':   'PLAIN',
        'group.id':          'rmintz',
        'auto.offset.reset': 'earliest'
    }

    # Create Consumer instance
    consumer = Consumer(config)

    # Subscribe to topic
    topic = "postgres.public.student"
    consumer.subscribe([topic])

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                # Extract the (optional) key and value, and print.
                print("message.topic: ", msg.topic())
                print("message key: ", msg.key())
                print("value: ", msg.value())
                print("value type: ", type(msg.value()))
                print("message decoded: ", msg.value().decode('utf-8'))

                # TODO
                # may have to decode using kafka avro
                
                # print("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                #     topic=msg.topic(), key=msg.key(),
                #     value=msg.value()
                # )
                # )
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
