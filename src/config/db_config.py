import os
import pymysql

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_DATABASE')

connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor object
cursor = connection.cursor()

# Execute SQL query
cursor.execute("UPDATE your_table SET column_name = 'new_value' WHERE condition")

# Commit changes and close the connection
connection.commit()
connection.close()