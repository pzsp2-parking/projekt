import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import unittest
from unittest.mock import patch
from classes.parking import Parking
import classes.account as account

TEST_PARKING1 = {
    "places": 15,
    "city": "Warszawa",
    "street": "Prosta",
    "addr_nr": "10",
    "id": "1",
}

TEST_EMPLOYEE1 = {
    "username": "employee1",
    "password": "XXXX",
    "mail": "client@gmail.com",
    "phone_no": "123456789",
    "parking": "1",
}


class TestParking(unittest.TestCase):
    def test_create_parking(self):
        parking = Parking(**TEST_PARKING1)
        self.assertEqual(parking.places, TEST_PARKING1["places"])
        self.assertEqual(parking.id, TEST_PARKING1["id"])

    @patch("classes.parking.db_cur")
    def test_get_parking_from_db(self, patch_db_cur):
        patch_db_cur.fetchone.return_value = list(TEST_PARKING1.values())[:-1]
        parking = Parking.get_parking(TEST_PARKING1["id"])
        self.assertEqual(parking.id, TEST_PARKING1["id"])
        self.assertEqual(parking.city, TEST_PARKING1["city"])

    @patch("classes.parking.account")
    def test_get_employee_parking(self, patch_account):
        patch_account.Employee.get_employee.return_value = account.Employee(
            **TEST_EMPLOYEE1
        )
        parking = Parking.get_employee_parking(TEST_EMPLOYEE1["username"])
        self.assertEqual(parking.id, TEST_PARKING1["id"])
        self.assertEqual(parking.city, TEST_PARKING1["city"])

    @patch("classes.parking.db_cur")
    def test_get_all_parkings(self, patch_db_cur):
        patch_db_cur.fetchall.return_value = [list(TEST_PARKING1.values())]
        parkings = Parking.get_all_parkings()
        self.assertEqual(parkings[0].id, TEST_PARKING1["id"])
        self.assertEqual(parkings[0].city, TEST_PARKING1["city"])

    @patch("classes.parking.db_cur")
    def test_get_park_map(self, patch_db_cur):
        patch_db_cur.fetchall.return_value = [["01-01-01"]]
        expected_map = [[0, 0], [0, 1]]
        result_map = Parking.get_parking_map("1")
        self.assertEqual(expected_map, result_map)


if __name__ == "__main__":
    unittest.main()
