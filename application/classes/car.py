from __future__ import annotations
from database.db_connector import db_cur, db_conn
import classes.account as account
from datetime import datetime, timedelta

DEPARTURE_HOURS = 8


class Car:
    """Class representing a single car"""

    def __init__(
        self,
        vin: str,
        reg_no: str,
        model: str,
        brand: str,
        capacity: float,
        owner_id: int,
    ):
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
    def add_car(
        client: account.Client,
        vin: str,
        reg_no: str,
        model: str,
        brand: str,
        capacity: float,
    ) -> Car:
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
            f"VALUES ('{car.vin}', '{car.reg_no}', '{car.model}', '{car.brand}',"
            f" '{car.capacity}', '{car.owner_id}');"
        )
        try:
            db_conn.exec_change(stmt_create)
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
        stmt_cars = (
            f"SELECT registration_no, model, brand, capacity, acc_account_no "
            f"FROM cars WHERE vin='{vin}'"
        )
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
        vin_list = [vin[0] for vin in db_cur.fetchall()]
        for vin in vin_list:
            cars.append(Car.get_car(vin))
        return cars

    def get_curr_charge_level(self) -> float:
        """
        Gets current charge level of a charging car.

        Returns:
            Current charge level.

        Raises:
            Exception: if chosen car is not parked.
        """
        if not self.is_parked():
            raise Exception("Car is not charging!")
        stmt = f"SELECT charge_level from charging WHERE car_vin='{self.vin}' ORDER BY datetime DESC LIMIT 1;"
        db_cur.execute(stmt)
        return float(db_cur.fetchone()[0])

    def get_charging_history(self, curr: bool = True) -> dict:
        """
        Gets history information from database from current charging.
        Dictionary keys of result are sorted in ascending order.

        Args:
            curr:       Determines if charging history should relate to current charging
                        or all past charging (if curr == False)

        Returns:
            Dictionary with keys - time of measurement, value - charge level
        """
        charge_history = []
        if curr:
            time_clause = "departure_datetime>now()"
        else:
            time_clause = "departure_datetime<=now()"
        stmt = f"SELECT datetime, charge_level from charging WHERE car_vin='{self.vin}' AND {time_clause} ORDER BY datetime ASC;"
        db_cur.execute(stmt)
        for entry in db_cur.fetchall():
            time = entry[0]
            charge_level = float(entry[1])
            charge_history.append({
                'x': time,
                'y': charge_level
            })
        return charge_history

    def get_all_charging_history(self) -> dict:
        """
        Gets all car's charging history divided by separate charging times
        and later by datetime.

        Return:
            A dictionary with keys as departure times that divide history into
            separate chargings.
            Further, values of the dict are dicts with keys as datetimes of given
            charging measurement and values - charge level.
        """
        time_clause = "departure_datetime<=now()"
        charge_history = {}
        stmt = f"SELECT datetime, charge_level, departure_datetime from charging WHERE car_vin='{self.vin}' AND {time_clause} ORDER BY departure_datetime DESC, datetime ASC;"
        db_cur.execute(stmt)
        for entry in db_cur.fetchall():
            time = entry[0]
            charge_level = float(entry[1])
            departure = entry[2]
            if str(departure) not in charge_history:
                charge_history[str(departure)] = []
            charge_history[str(departure)].append({
                'x': time,
                'y': charge_level
            })
        return charge_history

    def is_parked(self) -> bool:
        """
        Checks if given car is parked or not.

        Returns:
            True:   If car is parked.
            False:  If car is not parked.
        """
        stmt = f"SELECT * FROM cars_charging WHERE vin='{self.vin}'"
        db_cur.execute(stmt)
        if db_cur.fetchall():
            return True
        else:
            return False

    def park(
        self, charge_level: float, charger_id: str, departure_time: datetime = None
    ) -> None:
        """
        Parks a car updating information in the database.

        Args:
            charge_level:     Energy level of the parking car.
            charger_id:       Id of the used charger.
            departure_time:   Estimated departure time.

        Raises:
            Exception:        When chosen car is already parked.
        """
        if self.is_parked():
            raise Exception("Car is already parked")

        time = datetime.now()
        if not departure_time:
            departure_time = time + timedelta(hours=DEPARTURE_HOURS)

        stmt_insert = (
            f"INSERT INTO charging (datetime, base_charge_level, charge_level, departure_datetime, cha_charger_code, car_vin)"
            f"VALUES ('{time}', '{charge_level}', '{charge_level}', '{departure_time}',"
            f" '{charger_id}', '{self.vin}');"
        )

        db_conn.exec_change(stmt_insert)

    def change_departure(self, new_time: datetime) -> None:
        """
        Changes planned departure time of a parked car.

        Args:
            new_time:         New planned departure time.

        Raises:
            Exception:        When chosen car is not parked.
        """
        if not self.is_parked():
            raise Exception("Car is not parked")

        stmt = f"UPDATE charging SET departure_datetime = '{new_time}' WHERE car_vin='{self.vin}' AND departure_datetime>NOW();"
        db_conn.exec_change(stmt)

    def unpark(self) -> None:
        """
        Unparks a car updating information in the database.

        Raises:
            Exception:        When chosen car is not parked.
        """
        if not self.is_parked():
            raise Exception("Car is not parked")

        stmt = f"select charge_level, cha_charger_code from charging where car_vin='{self.vin}' ORDER BY datetime DESC;"

        db_cur.execute(stmt)
        charge_level, charger_id = db_cur.fetchone()

        time = datetime.now()

        self.change_departure(time)

        stmt_insert = (
            f"INSERT INTO charging (datetime, base_charge_level, charge_level, departure_datetime, cha_charger_code, car_vin)"
            f"VALUES ('{time}', '{charge_level}', '{charge_level}', '{time}',"
            f" '{charger_id}', '{self.vin}');"
        )

        db_conn.exec_change(stmt_insert)
