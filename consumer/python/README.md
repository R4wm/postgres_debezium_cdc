# example output from our python application when change is applied to the PostgreSQL DB

Our python application is subscribed to kafka. 
The layout looks like this: 

client -> postgres <= debezium (streams changes on events) -> kafka <= main.py (do something with the changes)

change made to our source postgres DB
```bash
exampledb=# insert into student (id, name) values (9,'robin'); 
INSERT 0 1
exampledb=# 

```

our python app `main.py` is subscribed to kafka, we poll every second and can see the changes made
```bash
Waiting...
Waiting...
message.topic:  postgres.public.student
message key:  b'\x00\x00\x00\x00\x01\x12'
value:  b'\x00\x00\x00\x00\x02\x00\x02\x12\x02\nrobin\x161.4.2.Final\x14postgresql\x10postgres\x9e\xbc\xfa\x98\x88e\x00\nfalse\x12exampledb\x0cpublic\x0estudent\x02\xf2\x07\x02\xe0\xa2\xe5\x16\x00\x02c\x02\xae\xbc\xfa\x98\x88e\x00'
value type:  <class 'bytes'>
this is response:  <Response [200]>
{'before': None, 'after': {'id': 9, 'name': 'robin'}, 'source': {'version': '1.4.2.Final', 'connector': 'postgresql', 'name': 'postgres', 'ts_ms': 1736266698511, 'snapshot': 'false', 'db': 'exampledb', 'schema': 'public', 'table': 'student', 'txId': 505, 'lsn': 23898288, 'xmin': None}, 'op': 'c', 'ts_ms': 1736266698519, 'transaction': None}
Waiting...
Waiting...

```

From here we can do anything we want with this data. We can transform and load the data to another store for our ML team to query for example. This keeps our source DB safe and efficient for its original intention. In this case lets pretend that it powers our user dashboards which shouldn't have too much load on it.

