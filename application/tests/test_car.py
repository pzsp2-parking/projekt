import sys
from pathlib import Path
import datetime

sys.path.append(str(Path(__file__).parent.parent))
import unittest
from unittest.mock import patch, Mock
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


class TestCar(unittest.TestCase):
    def test_create_car(self):
        new_car = Car(**TEST_CAR1)
        self.assertEqual(new_car.vin, TEST_CAR1["vin"])
        self.assertEqual(new_car.brand, TEST_CAR1["brand"])
        self.assertEqual(new_car.owner_id, TEST_CAR1["owner_id"])

    @patch("classes.car.db_conn")
    def test_add_car_to_db(self, patch_db_conn):
        mock_client = Mock()
        mock_client.get_id.return_value = TEST_CAR1["owner_id"]
        new_car = Car.add_car(mock_client, *list(TEST_CAR1.values())[:-1])
        patch_db_conn.exec_change.assert_called_once()
        self.assertEqual(new_car.owner_id, TEST_CAR1["owner_id"])
        self.assertEqual(new_car.reg_no, TEST_CAR1["reg_no"])

    @patch("classes.car.db_cur")
    def test_get_car_from_db(self, patch_db_cur):
        patch_db_cur.fetchone.return_value = list(TEST_CAR1.values())[1:]
        new_car = Car.get_car(TEST_CAR1["vin"])
        patch_db_cur.execute.assert_called_once()
        patch_db_cur.fetchone.assert_called_once()
        self.assertEqual(new_car.owner_id, TEST_CAR1["owner_id"])
        self.assertEqual(new_car.reg_no, TEST_CAR1["reg_no"])

    @patch("classes.car.Car.get_car")
    @patch("classes.car.db_cur")
    def test_get_client_cars_from_db(self, patch_db_cur, patch_get_car):
        patch_db_cur.fetchall.return_value = [TEST_CAR1["vin"]]
        patch_get_car.return_value = Car(**TEST_CAR1)
        mock_client = Mock()
        mock_client.get_id.return_value = TEST_CAR1["owner_id"]
        cars = Car.get_client_cars(mock_client)
        self.assertEqual(cars[0].vin, TEST_CAR1["vin"])
        self.assertEqual(cars[0].brand, TEST_CAR1["brand"])

    @patch("classes.car.db_cur")
    def test_is_parked_true(self, patch_db_cur):
        patch_db_cur.fetchall.return_value = [TEST_CAR1["vin"]]
        new_car = Car(**TEST_CAR1)
        parked = new_car.is_parked()
        self.assertEqual(parked, True)

    @patch("classes.car.db_cur")
    def test_is_parked_true(self, patch_db_cur):
        patch_db_cur.fetchall.return_value = []
        new_car = Car(**TEST_CAR1)
        parked = new_car.is_parked()
        self.assertEqual(parked, False)

    @patch("classes.car.db_conn")
    def test_car_park(self, patch_db_conn):
        new_car = Car(**TEST_CAR1)
        charge_level = 10
        charger_id = 2
        new_car.park(charge_level, charger_id)
        patch_db_conn.exec_change.assert_called_once()

    def test_car_park_parked(self):
        charge_level = 10
        charger_id = 2
        new_car = Car(**TEST_CAR1)
        with self.assertRaises(Exception) as context:
            new_car.park(charge_level, charger_id)

    @patch("classes.car.Car.is_parked")
    @patch("classes.car.db_conn")
    @patch("classes.car.db_cur")
    def test_unpark_car(self, patch_db_cur, patch_db_conn, patch_parked):
        patch_parked.return_value = True
        patch_db_cur.fetchone.return_value = (1, 2)
        new_car = Car(**TEST_CAR1)
        new_car.unpark()
        patch_db_cur.execute.assert_called_once()
        patch_db_conn.exec_change.assert_called()

    @patch("classes.car.Car.is_parked")
    def test_unpark_unparked_car(self, patch_parked):
        new_car = Car(**TEST_CAR1)
        patch_parked.return_value = False
        with self.assertRaises(Exception) as context:
            new_car.unpark()

    @patch("classes.car.db_conn")
    @patch("classes.car.Car.is_parked")
    def test_unpark_car(self, patch_parked, patch_db_conn):
        patch_parked.return_value = True
        new_car = Car(**TEST_CAR1)
        new_car.change_departure(datetime.datetime(2022, 12, 24))
        patch_db_conn.exec_change.assert_called()

    @patch("classes.car.Car.is_parked")
    def test_change_dep_unparked(self, patch_parked):
        new_car = Car(**TEST_CAR1)
        patch_parked.return_value = False
        with self.assertRaises(Exception) as context:
            new_car.change_departure(datetime.datetime(2022, 12, 24))


if __name__ == "__main__":
    unittest.main()
