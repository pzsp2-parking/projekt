from __future__ import annotations
from database.db_connector import db_cur

class Account:
    def __init__(self, account_nr, username, password, mail, phone_nr):
        self.account_nr = account_nr
        self.username=username
        self._password=password
        self.mail=mail
        self.phone_nr=phone_nr

    def check_password(self, pwd):
        return pwd==self._password

class Client (Account):
    def __init__(self, account_nr, username, password, mail, phone_nr, cars):
        super().__init__(account_nr, username, password, mail, phone_nr)
        self.cars=cars

    @staticmethod
    def get_client(username: str):
        stmt_client = f"SELECT acc_account_no, acc_password, acc_email_address, acc_phone_no FROM accounts WHERE acc_name=\'{username}\'"
        db_cur.execute(stmt_client)
        acc_nr, pwd, mail, phone_nr = db_cur.fetchone()
        stmt_cars = f"SELECT registration_no FROM cars WHERE acc_account_no=\'{acc_nr}\'"
        db_cur.execute(stmt_cars)
        cars = [nr for nr in db_cur.fetchall()]
        client = Client(acc_nr, username, pwd, mail, phone_nr, cars)
        return client

    @staticmethod
    def add_client(username, password, mail, phone_nr):
        stmt_create = f"INSERT INTO accounts (acc_name, acc_password, acc_email_address, acc_phone_no, acc_account_type) \
            VALUES (\'{username}\', \'{password}\', \'{mail}\', \'{phone_nr}\', 'CLIENT');"
        db_cur.execute(stmt_create)
        return 1


class Employee (Account):
    def __init__(self, account_nr, username, password, mail, phone_nr, role, parking):
        super().__init__(account_nr, username, password, mail, phone_nr)
        self.role=role
        self.parking=parking