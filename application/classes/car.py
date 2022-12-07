from __future__ import annotations
from application.database.db_connector import db_cur
import application.classes.account as account


class Car:
    """Class representing a single car"""

    def __init__(self, vin: str, reg_no: str, model: str, brand: str, capacity: float, owner_id: int):
        """
        Args:
            vin:        VIN number of the car.
            reg_no:     Registration number of the car.
            model:      Model of the car.
            brand:      Brand of the car.
            capacity:   Maximum capacity of car's tank.
            owner_id:   ID of the owner client.
        """
        self.vin = vin
        self.reg_no = reg_no
        self.model = model
        self.brand = brand
        self.capacity = capacity
        self.owner_id = owner_id

    @staticmethod
    def add_car(client: account.Client, vin: str, reg_no: str, model: str, brand: str, capacity: float) -> Car:
        car = Car(vin, reg_no, model, brand, capacity, client.get_id())
        # TODO: change account_no to appropriate foreign key
        stmt_create = (
            f"INSERT INTO cars (vin, registration_no, model, brand, capacity, account_no)"
            f"VALUES (\'{car.vin}\', \'{car.reg_no}\', \'{car.model}\', \'{car.brand}\',"
            f" \'{car.capacity}\', \'{car.owner_id}\');"
        )
        try:
            db_cur.execute(stmt_create)
        except Exception as e:
            print(e)
            raise
        return car

    @staticmethod
    def get_car(vin: str) -> Car:
        stmt_cars = f"SELECT registration_no, model, brand, capacity, account_no FROM car WHERE vin=\'{vin}\'"
        db_cur.execute(stmt_cars)
        reg_no, model, brand, capacity, acc_no = db_cur.fetchone()
        car = Car(vin, reg_no, model, brand, capacity, acc_no)
        return car

    @staticmethod
    def get_client_cars(client: account.Client) -> list[Car]:
        cars = []
        stmt = f"SELECT vin FROM car WHERE acc_no={client.get_id()};"
        db_cur.execute(stmt)
        vin_list = [vin for vin in db_cur.fetchall()]
        for vin in vin_list:
            cars.append(Car.get_car(vin))
        return cars
