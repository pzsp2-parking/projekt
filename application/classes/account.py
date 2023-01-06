from __future__ import annotations
from database.db_connector import db_cur, db_conn
import psycopg2
import classes.car as car
import datetime

CLIENT_TYPE = "CLIENT"


class Account:
    """
    Class representing a basic account
    """

    def __init__(self, username: str, password: str, mail: str, phone_no: str):
        """
        Args:
            username:   Unique username for the client account.
            password:   Account's password.
            mail:       Mail associated with the account.
            phone_no:   Phone number to the client account.
        """
        self.username = username
        self._password = password
        self.mail = mail
        self.phone_no = phone_no

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
        stmt = f"SELECT account_no FROM accounts WHERE name='{self.username}';"
        try:
            db_cur.execute(stmt)
            id = db_cur.fetchone()[0]
        except Exception as e:
            print(e)
        return id


class Client(Account):
    """
    Class representing a client's account
    """

    def __init__(
        self, username: str, password: str, mail: str, phone_no: str, cars: list = 0
    ):
        """
        Args:
            username, password, mail, phone_no: as in Account
            cars: list of cars added to the client's account
        """
        super().__init__(username, password, mail, phone_no)
        if not cars:
            self.cars = []
        else:
            self.cars = cars

    @staticmethod
    def get_client(username: str) -> Client:
        """
        Fetching client information from database using unique username.

        Args:
            username:        Client's username.

        Returns:
            A new Client object.
        """
        stmt_client = (
            f"SELECT password, email_address, phone_no "
            f"FROM accounts WHERE name='{username}';"
        )
        db_cur.execute(stmt_client)
        pwd, mail, phone_no = db_cur.fetchone()
        client = Client(username, pwd, mail, phone_no)
        cars = car.Car.get_client_cars(client)
        client.save_cars(cars)
        return client

    @staticmethod
    def add_client(username: str, password: str, mail: str, phone_no: str) -> Client:
        """
        Adds a new client to the database

        Args:
            username:   Unique username for the client account.
            password:   Account's password.
            mail:       Mail associated with the account.
            phone_no:   Phone number to the client account.

        Returns:
            A new Client instance.

        Raises:
            UniqueViolation.
        """
        client = Client(username, password, mail, phone_no)
        stmt_create = (
            f"INSERT INTO accounts (name, password, email_address, phone_no, account_type)"
            f"VALUES ('{client.username}', '{client._password}', '{client.mail}', '{client.phone_no}', '{CLIENT_TYPE}');"
        )
        try:
            db_conn.exec_change(stmt_create)
        except psycopg2.errors.UniqueViolation as e:
            # TODO: better error handler
            print(e)
        return client

    def add_car(
        self, vin: str, reg_no: str, model: str, brand: str, capacity: float
    ) -> car.Car:
        """
        Adds provided car and saves it to client.

        Args:
            vin:        Car's VIN number.
            reg_no:     Registration number of the car.
            model:      Model of the car.
            brand:      Brand of the car.
            capacity:   Maximum capacity of car's tank.

        Returns:
            A new Car object.
        """
        try:
            new_car = car.Car.add_car(self, vin, reg_no, model, brand, capacity)
            self.cars.append(new_car)
        except Exception as e:
            print(e)
            raise
        return new_car

    def save_cars(self, cars: list[car.Car]) -> None:
        """
        Saves provided list of cars to client's instance.
        Only new cars are being added (repetitions are omitted).

        Args:
            cars:       List of cars to ba added to client's account.

        Returns:
            None.
        """
        for new_car in cars:
            if new_car.vin not in ([x.vin for x in self.cars]):
                self.cars.append(new_car)

    def park_car(
        self,
        vin: str,
        charge_level: float,
        charger_id: int,
        departure_time: datetime = None,
    ) -> None:
        """
        Enables client to park a given car.

        Args:
            vin:              Car's VIN number to be parked.
            charge_level:     Energy level of the parking car.
            charger_id:       Id of the used charger.
            departure_time:   Estimated departure time.

        Returns:
            None
        """
        if not vin in [x.vin for x in self.cars]:
            # TODO: is it possible to choose not owned car or frontend does not allow?
            raise Exception
        car = [x for x in self.cars if x.vin == vin][0]
        car.park(charge_level, charger_id, departure_time)

    def unpark_car(self, vin: str) -> None:
        """
        Enables client to unpark a given car.

        Args:
            vin:        Car's VIN number to be parked.

        Returns:
            None
        """
        car = [x for x in self.cars if x.vin == vin][0]
        car.unpark()

    def change_car_departure(self, vin: str, new_time: datetime) -> None:
        """
        Client can change the planned departure time of parked car.

        Args:
            vin:        Parked car's VIN number.
        """
        if not vin in [x.vin for x in self.cars]:
            # TODO: better exception msg
            raise Exception
        car = [x for x in self.cars if x.vin == vin][0]
        car.change_departure(new_time)


class Employee(Account):
    """
    Class representing an employee's account.
    """

    def __init__(self, username, password, mail, phone_no, parking):
        """
        Args:
            username, password, mail, phone_no: as in Account
            parking:        Parking where employee works
        """
        super().__init__(username, password, mail, phone_no)
        self.parking = parking
