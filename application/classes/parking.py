from __future__ import annotations
from database.db_connector import db_cur, db_conn
import classes.account as account

class Parking:
    """Class representing a single parking"""

    def __init__(self, places: int, city: str, street: str, addr_nr: str, id: str = 0):
        """
        Args:
            places:     Number of places on the parking.
            city:       City where parking is located.
            street:     Street where parking is located.
            addr_no:    Address number where parking is located.
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
            f"SELECT places, city, street, addr_nr"
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

    def get_parking_map(self):
        pass

