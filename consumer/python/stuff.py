#!/usr/bin/env python3
import json

something =''
with open('schema.avsc' , 'r') as e:
    something = e.read()


with open('something.avsc', 'w') as e:
    e.write(json.loads(something))

print("wrote something to something.avsc")

