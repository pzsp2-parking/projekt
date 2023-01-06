import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import unittest
from unittest.mock import patch
from classes.account import Employee

TEST_EMPLOYEE1 = {
    "username": "employee1",
    "password": "XXXX",
    "mail": "client@gmail.com",
    "phone_no": "123456789",
    "parking": "1",
}


class TestEmployee(unittest.TestCase):
    def test_create_employee(self):
        new_employee = Employee(**TEST_EMPLOYEE1)
        self.assertEqual(new_employee.username, TEST_EMPLOYEE1["username"])
        self.assertEqual(new_employee.phone_no, TEST_EMPLOYEE1["phone_no"])
        self.assertEqual(new_employee.parking, TEST_EMPLOYEE1["parking"])

    @patch("classes.account.db_cur")
    def test_get_employee_from_db(self, patch_db_cur):
        patch_db_cur.fetchone.return_value = list(TEST_EMPLOYEE1.values())[1:]
        employee = Employee.get_employee(TEST_EMPLOYEE1["username"])
        self.assertEqual(employee.parking, TEST_EMPLOYEE1["parking"])
        self.assertEqual(employee.username, TEST_EMPLOYEE1["username"])


if __name__ == "__main__":
    unittest.main()
