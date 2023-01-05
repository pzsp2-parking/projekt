import sys
from pathlib import Path
import datetime

sys.path.append(str(Path(__file__).parent.parent))
import unittest
from unittest.mock import patch, Mock
from classes.account import Account, Client
from classes.car import Car

TEST_CAR1 = {
    "vin": "1234",
    "reg_no": "WZ123",
    "model": "Taycan",
    "brand": "Porsche",
    "capacity": 100,
    "owner_id": 1,
}

TEST_CAR2 = {
    "vin": "2345",
    "reg_no": "WZ234",
    "model": "S",
    "brand": "Tesla",
    "capacity": 40,
    "owner_id": 2,
}


TEST_CLIENT1 = {
    "username": "client1",
    "password": "XXXX",
    "mail": "client@gmail.com",
    "phone_no": "123456789",
    "cars": [],
}

TEST_CLIENT2 = {
    "username": "client2",
    "password": "XXXX",
    "mail": "client2@gmail.com",
    "phone_no": "234567891",
    "cars": [Car(**TEST_CAR1)],
}

# TODO: test Account


class TestClient(unittest.TestCase):
    def test_create_client(self):
        new_client = Client(**TEST_CLIENT1)
        self.assertEqual(new_client.username, TEST_CLIENT1["username"])
        self.assertEqual(new_client.phone_no, TEST_CLIENT1["phone_no"])
        self.assertEqual(new_client.mail, TEST_CLIENT1["mail"])

    @patch("classes.account.car.Car")
    @patch("classes.account.db_cur")
    def test_get_client_from_db(self, patch_db_cur, patch_car):
        patch_db_cur.fetchone.return_value = list(TEST_CLIENT1.values())[1:-1]
        patch_car.get_client_cars.return_value = [Car(**TEST_CAR1)]
        client_with_cars = Client.get_client(TEST_CLIENT1["username"])
        self.assertEqual(client_with_cars.cars[0].reg_no, TEST_CAR1["reg_no"])
        self.assertEqual(len(client_with_cars.cars), 1)
        self.assertEqual(client_with_cars.username, TEST_CLIENT1["username"])

    @patch("classes.account.db_conn")
    def test_add_client_to_db(self, patch_db_conn):
        new_client = Client.add_client(*list(TEST_CLIENT1.values())[:-1])
        patch_db_conn.exec_change.assert_called_once()
        self.assertEqual(new_client.username, TEST_CLIENT1["username"])
        self.assertEqual(new_client.mail, TEST_CLIENT1["mail"])

    @patch("classes.account.car.Car")
    def test_add_client_car(self, patch_car):
        client = Client(**TEST_CLIENT1)
        patch_car.add_car.return_value = Car(**TEST_CAR1)
        new_car = client.add_car(*list(TEST_CAR1.values())[:-1])
        self.assertEqual(new_car.reg_no, TEST_CAR1["reg_no"])
        self.assertEqual(new_car.model, TEST_CAR1["model"])

    def test_save_client_cars(self):
        client = Client(**TEST_CLIENT1)
        cars = [Car(**TEST_CAR1), Car(**TEST_CAR2)]
        client.save_cars(cars)
        self.assertEqual(client.username, TEST_CLIENT1["username"])
        self.assertEqual(len(client.cars), len(cars))
        self.assertEqual(client.cars[0].reg_no, TEST_CAR1["reg_no"])
        self.assertEqual(client.cars[1].reg_no, TEST_CAR2["reg_no"])

    def test_save_client_cars_duplicates(self):
        client = Client(**TEST_CLIENT1)
        cars = [Car(**TEST_CAR1), Car(**TEST_CAR2), Car(**TEST_CAR1)]
        client.save_cars(cars)
        self.assertEqual(client.username, TEST_CLIENT1["username"])
        self.assertEqual(len(client.cars), 2)
        self.assertEqual(client.cars[0].reg_no, TEST_CAR1["reg_no"])
        self.assertEqual(client.cars[1].reg_no, TEST_CAR2["reg_no"])

    @patch("classes.car.db_conn")
    def test_park_car(self, patch_db_conn):
        vin = TEST_CAR1["vin"]
        charge_level = 10
        charger_id = 2
        client = Client(**TEST_CLIENT2)
        self.assertEqual(client.cars[0].reg_no, TEST_CAR1["reg_no"])
        client.park_car(vin, charge_level, charger_id)
        patch_db_conn.exec_change.assert_called_once()

    def test_park_parked_car(self):
        vin = TEST_CAR2["vin"]
        charge_level = 10
        charger_id = 2
        client = Client(**TEST_CLIENT2)
        self.assertEqual(client.cars[0].reg_no, TEST_CAR1["reg_no"])
        with self.assertRaises(Exception) as context:
            client.park_car(vin, charge_level, charger_id)

    @patch("classes.car.Car.is_parked")
    @patch("classes.car.db_conn")
    @patch("classes.car.db_cur")
    def test_unpark_car(self, patch_db_cur, patch_db_conn, patch_parked):
        patch_parked.return_value = True
        patch_db_cur.fetchone.return_value = (1, 2)
        vin = TEST_CAR1["vin"]
        client = Client(**TEST_CLIENT2)
        self.assertEqual(client.cars[0].reg_no, TEST_CAR1["reg_no"])
        client.unpark_car(vin)
        patch_db_cur.execute.assert_called_once()
        patch_db_conn.exec_change.assert_called()

    @patch("classes.car.Car.change_departure")
    def test_change_car_departure(self, patch_car_change_dep):
        vin = TEST_CAR1["vin"]
        new_time = datetime.datetime(2022, 12, 24)
        client = Client(**TEST_CLIENT2)
        self.assertEqual(client.cars[0].reg_no, TEST_CAR1["reg_no"])
        client.change_car_departure(vin, new_time)
        patch_car_change_dep.assert_called_once()
        patch_car_change_dep.assert_called_with(new_time)

    def test_change_dep_unowned_car(self):
        vin = TEST_CAR2["vin"]
        client = Client(**TEST_CLIENT2)
        self.assertEqual(client.cars[0].reg_no, TEST_CAR1["reg_no"])
        with self.assertRaises(Exception) as context:
            client.change_car_departure(vin, datetime.datetime(2022, 12, 24))


if __name__ == "__main__":
    unittest.main()
