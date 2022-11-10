from database.db_setup import db_cursor

db_cursor.execute("SHOW tables;")

for x in db_cursor:
    print(x)