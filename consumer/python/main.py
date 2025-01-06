#!/usr/bin/env python3

from requests import get
from fastavro.schema import load_schema
from confluent_kafka import Consumer
import fastavro
import io
import avro.io
import avro.datafile


# get schema from schema-registry: curl -s http://localhost:8081/subjects/postgres.public.student-value/versions/1 | jq .


def get_schema_from_registry(subject):
    schema_registry_url = 'http://localhost:8081/subjects/postgres.public.student-value/versions/1'
    url = f"{schema_registry_url}/subjects/{subject}/versions/1"
    response = get(schema_registry_url)
    print('this is response: ', response)
    result = avro.schema.parse(response.json()['schema'])
    return result


if __name__ == '__main__':
    topic = "postgres.public.student"
    get_schema_from_registry(topic)
    
    config = {
        'bootstrap.servers': 'localhost:9092',
        'sasl.mechanisms':   'PLAIN',
        'group.id':          'rmintz',
        'auto.offset.reset': 'earliest',
        # 'sasl.username':     'docker',
        # 'sasl.password':     'docker',
        # # Fixed properties
        # 'security.protocol': 'SASL_SSL',        
    }

    # Create Consumer instance
    consumer = Consumer(config)

    # Subscribe to topic

    consumer.subscribe([topic])

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                print("Waiting...")
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
            else:
                # Extract the (optional) key and value, and print.
                print("message.topic: ", msg.topic())
                print("message key: ", msg.key())
                print("value: ", msg.value())
                print("value type: ", type(msg.value()))
                # handle deserialize
                #schema = avro.schema.parse(open("something.avsc", "rb").read())
                schema = get_schema_from_registry(msg.topic())
                message_bytes = io.BytesIO(msg.value())
                message_bytes.seek(5)
                decoder = avro.io.BinaryDecoder(message_bytes)
                reader = avro.io.DatumReader(schema)
                event_dict = reader.read(decoder)
                print(event_dict)

    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
