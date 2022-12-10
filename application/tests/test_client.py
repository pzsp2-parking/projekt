import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import unittest
from unittest.mock import patch, Mock
from classes.account import Account, Client
from classes.car import Car

TEST_CAR1 = {
    "vin": '1234',
    "reg_no": 'WZ123',
    'model': 'Taycan',
    'brand': 'Porsche',
    'capacity': 100,
    'owner_id': 1
}

TEST_CAR2 = {
    "vin": '2345',
    "reg_no": 'WZ234',
    'model': 'S',
    'brand': 'Tesla',
    'capacity': 40,
    'owner_id': 2
}


TEST_CLIENT1 = {
    "username": 'client',
    "password": 'XXXX',
    'mail': 'client@gmail.com',
    'phone_no': '123456789',
    'cars': []
}

# TODO: test Account


class TestClient(unittest.TestCase):

    def test_create_client(self):
        new_client = Client(**TEST_CLIENT1)
        self.assertEqual(new_client.username, TEST_CLIENT1['username'])
        self.assertEqual(new_client.phone_no, TEST_CLIENT1['phone_no'])
        self.assertEqual(new_client.mail, TEST_CLIENT1['mail'])

    @patch('classes.account.car.Car')
    @patch('classes.account.db_cur')
    def test_get_client_from_db(self, patch_db_cur, patch_car):
        patch_db_cur.fetchone.return_value = list(TEST_CLIENT1.values())[1:-1]
        patch_car.get_client_cars.return_value = [Car(**TEST_CAR1)]
        client_with_cars = Client.get_client(TEST_CLIENT1['username'])
        self.assertEqual(client_with_cars.cars[0].reg_no, TEST_CAR1['reg_no'])
        self.assertEqual(len(client_with_cars.cars), 1)
        self.assertEqual(client_with_cars.username, TEST_CLIENT1['username'])

    @patch('classes.account.db_conn')
    def test_add_client_to_db(self, patch_db_conn):
        new_client = Client.add_client(*list(TEST_CLIENT1.values())[:-1])
        patch_db_conn.exec_change.assert_called_once()
        self.assertEqual(new_client.username, TEST_CLIENT1['username'])
        self.assertEqual(new_client.mail, TEST_CLIENT1['mail'])

    @patch('classes.account.car.Car')
    def test_add_client_car(self, patch_car):
        client = Client(**TEST_CLIENT1)
        patch_car.add_car.return_value = Car(**TEST_CAR1)
        new_car=client.add_car(*list(TEST_CAR1.values())[:-1])
        self.assertEqual(new_car.reg_no, TEST_CAR1['reg_no'])
        self.assertEqual(new_car.model, TEST_CAR1['model'])

    def test_save_client_cars(self):
        client = Client(**TEST_CLIENT1)
        cars = [Car(**TEST_CAR1), Car(**TEST_CAR2)]
        client.save_cars(cars)
        self.assertEqual(client.username, TEST_CLIENT1['username'])
        self.assertEqual(len(client.cars), len(cars))
        self.assertEqual(client.cars[0].reg_no, TEST_CAR1['reg_no'])
        self.assertEqual(client.cars[1].reg_no, TEST_CAR2['reg_no'])

    def test_save_client_cars_duplicates(self):
        client = Client(**TEST_CLIENT1)
        cars = [Car(**TEST_CAR1), Car(**TEST_CAR2), Car(**TEST_CAR1)]
        client.save_cars(cars)
        self.assertEqual(client.username, TEST_CLIENT1['username'])
        self.assertEqual(len(client.cars), 2)
        self.assertEqual(client.cars[0].reg_no, TEST_CAR1['reg_no'])
        self.assertEqual(client.cars[1].reg_no, TEST_CAR2['reg_no'])

if __name__ == '__main__':
    unittest.main()