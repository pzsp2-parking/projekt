from database.db_connector import db_cur, DBConn
from classes.account import Client


def prepare_db():
    """Either create database and tables using DBConn().execute(schema_path)
        or just insert sample data with insert_path"""
    schema_path = "database/schema_16112022.sql"
    insert_path = "database/populate_db_16112022.sql"
    # DBConn().execute(schema_path)
    DBConn().execute(insert_path)


def example(username):
    my_client = Client.get_client(username)
    print(f"Username: {my_client.username}, cars: {my_client.cars}")


if __name__ == "__main__":
    # prepare_db()
    example("ola")
