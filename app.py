from flask import Flask, render_template, request
import psycopg2




# Define database connection parameters
DB_NAME = 'Varshini'
DB_USER = 'Varshini'
DB_PASSWORD = 'Man_4569'
DB_HOST = 'local_pgdb'
DB_PORT = '5432'

# Define a function to connect to the PostgreSQL database
def connect_to_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn



    conn.close()

    return 'Data submitted successfully'

