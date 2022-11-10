import mysql.connector

db_connection = mysql.connector.connect(
  host="localhost",
  user="pzsp2",
  password="parking",
  #database="parpa"
)

db_cursor = db_connection.cursor()

#db_cursor.execute("CREATE DATABASE parpa")

#db_cursor.execute("CREATE TABLE cars (nr int);")

