from database.db_connector import db_cur, DBConn
from classes.account import Client
from classes.car import Car


def prepare_db():
    """Either create database and tables using DBConn().execute(schema_path)
        or just insert sample data with insert_path"""
    schema_path = "database/schema_16112022.sql"
    insert_path = "database/populate_db_16112022.sql"
    # DBConn().execute(schema_path)
    DBConn().execute(insert_path)


def example(user):
    vin='VIN1'
    reg_no='WZ1234'
    model='Taycan'
    brand='Porsche'
    capacity=100
    my_client = Client.get_client(user)
    Car.add_car(my_client, vin, reg_no, model, brand, capacity)
    print(f"Username: {my_client.username}")


if __name__ == "__main__":
    # prepare_db()
    example("employee")
