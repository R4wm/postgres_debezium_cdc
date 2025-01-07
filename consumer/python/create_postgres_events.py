#!/usr/bin/env python3
'''
simple script to simulate changes to postgresql
'''

import os
import psycopg2
import string
import secrets
    
dbpass = os.getenv("DB_PASS")
N = 7
try:
    connection = psycopg2.connect(
        host="localhost",
        database = "exampledb",
        user='docker',
        password = dbpass,
    )
    print("connection to database ok")

    cursor = connection.cursor()
    # get latest id and increment it for next insert
    # TODO: update the DB to just serial the id / auto increment
    get_last_id = "SELECT max(id) from student"
    cursor.execute(get_last_id)
    last_id = cursor.fetchone()[0]
    print(f"last_id: {last_id}")
    last_id += 1
    rando_str =  ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(N))

    # #INSERT into the db
    # breakpoint()
    # insert_stmt = 'INSERT INTO student(id, name) VALUES(%s, %s)'
    # cursor.execute(insert_stmt, (id, rando_str))
    # print("inserted {last_id} {rando_str} into exampledb")

    # # SELECT STMT
    # select_query = "SELECT * FROM student"
    # cursor.execute(select_query)
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)

    update_query = "UPDATE student set name=%s where id=%s"
    name = 'superman'
    id=1
    cursor.execute(update_query, (name, id))
    
    connection.commit()
    cursor.close()
    connection.close()
    print("ran connection.commmit()")
except Exception as a:
    print("error --> ", a)
