#!/usr/bin/env python3

from fastavro.schema import load_schema
from fastavro import reader

schema_registry_url = conf['http://localhost:8081/']

def get_schema_from_registry(subject):
    from requests import get
    url = f"{schema_registry_url}/subjects/{subject}/versions/latest"
    response = get(url, auth=('<<USER>>', '<<API_KEY>>'))
    return response.json()['schema']

def decode_avro(msg, schema_str):
    from io import BytesIO
    from fastavro import schemaless_reader
    schema = load_schema(BytesIO(schema_str.encode('utf-8')))
    return schemaless_reader(BytesIO(msg), schema)

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue
    
    schema_str = get_schema_from_registry(msg.topic())
    deserialized_data = decode_avro(msg.value(), schema_str)
    print(deserialized_data)

consumer.close()
