#!/usr/bin/env python3

from fastavro.schema import load_schema
from fastavro import reader

schema_registry_url = 'http://localhost:8081/subjects/postgres.public.student-value/versions/1'
sample_bytes = b'\x00\x00\x00\x00\x02\x02\x02\x02\x10superman\x02\x02\x02\x10superman\x161.4.2.Final\x14postgresql\x10postgres\xc4\xf9\xa4\xd1\x87e\x00\nfalse\x12exampledb\x0cpublic\x0estudent\x02\x90\x15\x02\x90\x8a\x8c\x17\x00\x02u\x02\x92\xfd\xa4\xd1\x87e\x00'


# def get_schema_from_registry(subject):
#     from requests import get
#     response = get(schema_registry_url)
#     return response.json()['schema']

def decode_avro(msg):
    from io import BytesIO
    from fastavro import schemaless_reader
    # schema = load_schema(BytesIO(schema_str.encode('utf-8')))
    # schema = load_schema(schema_str)
    schema = load_schema('something.avsc')
    breakpoint()
    return schemaless_reader(BytesIO(msg), schema)


#schema_str = get_schema_from_registry('postgres.public.student-value')
deserialized_data = decode_avro(sample_bytes)
print(deserialized_data)

