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
        """
        Adds a new car to the system.
        Car has to be already owned by a client.

        Args:
            client:     Client owner of the car.
            vin:        VIN number of the car.
            reg_no:     Registration number of the car.
            model:      Model of the car.
            brand:      Brand of the car.
            capacity:   Maximum capacity of car's tank.

        Returns:
            A new Car object.
        """
        car = Car(vin, reg_no, model, brand, capacity, client.get_id())
        stmt_create = (
            f"INSERT INTO cars (vin, registration_no, model, brand, capacity, acc_account_no)"
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
        """
        Fetches a car with given VIN number.

        Args:
            vin:        VIN number of searched car.

        Returns:
            A new car object.
        """
        stmt_cars = (f"SELECT registration_no, model, brand, capacity, acc_account_no "
                     f"FROM cars WHERE vin=\'{vin}\'")
        db_cur.execute(stmt_cars)
        reg_no, model, brand, capacity, acc_no = db_cur.fetchone()
        car = Car(vin, reg_no, model, brand, capacity, acc_no)
        return car

    @staticmethod
    def get_client_cars(client: account.Client) -> list[Car]:
        """
        Fetches all cars belonging to given client's account.

        Args:
            client:     Client's account to search for cars.

        Returns:
            A list of cars belonging to the client.
        """
        cars = []
        stmt = f"SELECT vin FROM cars WHERE acc_account_no={client.get_id()};"
        db_cur.execute(stmt)
        vin_list = [[vin] for vin in db_cur.fetchall()]
        for vin in vin_list:
            cars.append(Car.get_car(vin))
        return cars
