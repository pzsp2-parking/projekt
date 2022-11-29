from __future__ import annotations
from database.db_connector import db_cur

class Account:
    def __init__(self, account_nr, username, password, name, surname, mail, phone_nr):
        self.account_nr = account_nr
        self.username=username
        self._password=password
        self.name=name
        self.surname=surname
        self.mail=mail
        self.phone_nr=phone_nr

    def check_password(self, pwd):
        return pwd==self._password

class Client (Account):
    def __init__(self, account_nr, username, password, name, surname, mail, phone_nr, cars):
        super().__init__(account_nr, username, password, name, surname, mail, phone_nr)
        self.cars=cars
    
    @staticmethod
    def get_client(username: str):
        stmt_client=f"SELECT password, mail FROM clients WHERE username=\'{username}\'"
        stmt_cars=f"SELECT registration_nr FROM cars WHERE username=\'{username}\'"
        db_cur.execute(stmt_client)
        pwd, mail = db_cur.fetchone()
        db_cur.execute(stmt_cars)
        cars = [nr for nr in db_cur.fetchall()]
        client = Client(username, pwd, mail, cars)
        return client

    @staticmethod
    def add_client(client: Client):
        stmt_create=f"INSERT INTO clients (username, password, name, surname, mail) VALUES ('guest', 'guest', 'guest');"
        pass


class Employee (Account):
    def __init__(self, account_nr, username, password, name, surname, mail, phone_nr, role, parking):
        super().__init__(account_nr, username, password, mail, phone_nr)
        self.role=role
        self.parking=parking