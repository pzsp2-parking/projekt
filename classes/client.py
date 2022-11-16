from database.db_connector import db_cur

class Client:
    def __init__(self, username, password, mail, cars):
        self.username=username
        self.password=password
        self.mail=mail
        self.cars=cars
    
    @staticmethod
    def get_client(username: str):
        stmt_client=f"SELECT password, mail FROM clients WHERE username=\"{username}\""
        stmt_cars=f"SELECT registration_nr FROM cars WHERE username=\"{username}\""
        db_cur.execute(stmt_client)
        pwd, mail = db_cur.fetchone()
        db_cur.execute(stmt_cars)
        cars = [nr for nr in db_cur.fetchall()]
        client = Client(username, pwd, mail, cars)
        return client

