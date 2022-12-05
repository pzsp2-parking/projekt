from __future__ import annotations
from database.db_connector import db_cur

class Parking:
    """Class representing a single parking"""
    def __init__(self, places: int, city: str, street: str, addr_nr: str) -> Parking:
        self.places=places
        self.city=city
        self.street=street
        self.addr_nr=addr_nr
        # id to be taken from database after creation in db
        self._id=0