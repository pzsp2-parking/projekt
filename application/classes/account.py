from __future__ import annotations
from application.database.db_connector import db_cur
import psycopg2
import application.classes.car as car


class Account:
    def __init__(self, username: str, password: str, mail: str, phone_nr: str):
        """
        Args:
            username:   Unique username for the client account.
            password:   Account's password.
            mail:       Mail associated with the account.
            phone_nr:   Phone number to the client account.

        Returns:
            
        """
        self.username = username
        self._password = password
        self.mail = mail
        self.phone_nr = phone_nr

    def check_password(self, pwd: str) -> bool:
        """
        Checking if account can be authenticated.
        If password provided by the user matches the one in the database.

        Args:
            pwd:        Provided password to be verified.

        Returns:
            True:       When password is correct.
            False:      When password is incorrect.
        """
        return pwd == self._password

    def get_id(self) -> int:
        """
        Get account unique id.

        Returns:
            Account's primary key from database.
        """
        stmt = f"SELECT acc_account_nr FROM account WHERE acc_name=\'{self.username}\';"
        try:
            db_cur.execute(stmt)
            id = db_cur.fetchone()
        except Exception as e:
            print(e)
        return id


class Client(Account):
    def __init__(self, username: str, password: str, mail: str, phone_nr: str, cars: list = []):
        super().__init__(username, password, mail, phone_nr)
        self.cars = cars

    @staticmethod
    def get_client(username: str) -> Client:
        stmt_client = f"SELECT acc_password, acc_mail_address, acc_phone_no FROM account WHERE username=\'{username}\';"
        db_cur.execute(stmt_client)
        pwd, mail, phone_no = db_cur.fetchone()
        client = Client(username, pwd, mail, phone_no)
        cars = car.Car.get_client_cars(client)
        client.save_cars(cars)
        return client

    @staticmethod
    def add_client(username: str, password: str, mail: str, phone_nr: str) -> Client:
        """
        Adds a new client to the database

        Args:
            username:   Unique username for the client account.
            password:   Account's password.
            mail:       Mail associated with the account.
            phone_nr:   Phone number to the client account.

        Returns:
            A new client.

        Raises:
            UniqueViolation.
        """
        client = Client(username, password, mail, phone_nr)
        stmt_create = (
            f"INSERT INTO account (username, password, mail, phone_nr)"
            f"VALUES (\'{client.username}\', \'{client._password}\', \'{client.mail}\', \'{client.phone_nr}\');"
        )
        try:
            db_cur.execute(stmt_create)
        except psycopg2.errors.UniqueViolation as e:
            # TODO: better error handler
            print(e)
        return client

    def add_car(self, vin: str, nr_reg: str, model: str, brand: str, capacity: float) -> car.Car:
        """
        Adds provided car and saves it to client.
        """
        try:
            new_car = car.Car.add_car(self, vin, nr_reg, model, brand, capacity)
            self.cars.append(new_car)
        except Exception as e:
            print(e)
            raise
        return new_car

    def save_cars(self, cars: list[car.Car]) -> None:
        for new_car in cars:
            if new_car not in self.cars:
                self.cars.append(new_car)


class Employee(Account):
    def __init__(self, username, password, mail, phone_nr, parking):
        super().__init__(username, password, mail, phone_nr)
        self.parking = parking
