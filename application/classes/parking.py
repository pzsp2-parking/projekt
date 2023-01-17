from __future__ import annotations
from database.db_connector import db_cur, db_conn
import classes.account as account
import classes.car as car

EMPTY = 0
OCCUPIED = 1


class Parking:
    """Class representing a single parking"""

    def __init__(self, places: int, city: str, street: str, addr_nr: str, id: str = 0):
        """
        Args:
            places:     Number of places on the parking.
            city:       City where parking is located.
            street:     Street where parking is located.
            addr_nr:    Address number where parking is located.
            id:         Unique id of the parking.
        """
        self.places = places
        self.city = city
        self.street = street
        self.addr_nr = addr_nr
        self.id = id

    @staticmethod
    def get_parking(id: str) -> Parking:
        """
        Fetching parking information from database using unique id.

        Args:
            id:        Parking's id.

        Returns:
            A new Parking object.
        """
        stmt_parking = (
            f"SELECT spaces_no, city, street, building_no "
            f"FROM car_parks WHERE car_park_id='{id}';"
        )
        db_cur.execute(stmt_parking)
        places, city, street, addr_nr = db_cur.fetchone()
        parking = Parking(places, city, street, addr_nr, id)
        return parking

    @staticmethod
    def get_employee_parking(username: str) -> Parking:
        """
        Fetching parking using employee's username

        Args:
            username:       Employee's username working on the parking.

        Returns:
            A new Parking object.
        """
        employee = account.Employee.get_employee(username)
        parking = Parking.get_parking(employee.parking)
        return parking

    @staticmethod
    def get_all_parkings() -> list[Parking]:
        """
        Getting all available parkings from db.

        Returns:
            List of Parking objects.
        """
        result = []
        stmt = (
            "SELECT spaces_no, city, street, building_no, car_park_id FROM car_parks;"
        )
        db_cur.execute(stmt)
        parkings = db_cur.fetchall()
        for parking in parkings:
            spaces_no = str(parking[0])
            city = str(parking[1])
            street = str(parking[2])
            addr_no = str(parking[3])
            id = str(parking[4])
            new_parking = Parking(spaces_no, city, street, addr_no, id)
            result.append(new_parking)
        return result

    @staticmethod
    def get_parking_map(id) -> list[list]:
        """
        Creates a parking map as a matrix.
        With places marked either as EMPTY or OCCUPIED.

        Args:
            id:     Id of the parking.

        Returns:
            A matrix with empty and occupied places with chargers on the parking.
        """
        max_row, max_col = 0, 0
        stmt_all = f"SELECT charger_code FROM chargers WHERE cpa_car_park_id={id};"
        db_cur.execute(stmt_all)
        for code in db_cur.fetchall():
            row, col = charger_place(code[0])
            if row > max_row:
                max_row = row
            if col > max_col:
                max_col = col
        park_map = empty_parking(max_row + 1, max_col + 1)
        stmt_occupied = (
            f"SELECT charger_code FROM cars_charging WHERE car_park_id={id};"
        )
        db_cur.execute(stmt_occupied)
        for code in db_cur.fetchall():
            row, col = charger_place(code[0])
            park_map[row][col] = OCCUPIED
        return park_map

    def get_all_cars(self) -> list[car.Car]:
        """
        Getting all parked cars on given parking from db.

        Returns:
            List of parked Car objects.
        """
        cars = []
        stmt = f"SELECT vin FROM cars_charging WHERE car_park_id='{self.id}'"
        db_cur.execute(stmt)
        vin_list = [vin[0] for vin in db_cur.fetchall()]
        for vin in vin_list:
            parked_car = car.Car.get_car(vin)
            cars.append(parked_car)
        return cars


def charger_place(charger_code: str) -> tuple:
    """
    Get charger's place on the parking: row and column positions

    Args:
        charger_code:   Unique code of the charger.

    Returns:
        Row and column position of the charger on a parking.

    """
    parking, row, col = charger_code.split("-")
    return (int(row), int(col))


def empty_parking(col: int, row: int) -> list:
    """
    Creates a map of empty parking - with all zeros

    Args:
        row:    Number of rows.
        col:    Number of columns.

    Returns:
        List acting as a map of parking.
    """
    parking = [EMPTY for _ in range(col)]
    for c in range(col):
        parking[c] = [EMPTY for _ in range(row)]
    return parking
