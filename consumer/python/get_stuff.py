#!/usr/bin/env python3
import os
import psycopg2

dbpass = os.getenv("DB_PASS")
try:
    connection = psycopg2.connect(
        host="localhost",
        database = "exampledb",
        user='docker',
        password = dbpass,
    )
    print("connection to database ok")

    cursor = connection.cursor()
    select_query = "SELECT * FROM student"
    cursor.execute(select_query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # can i update here on same conncetion ?
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
