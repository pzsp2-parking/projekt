import unittest
from unittest.mock import patch, Mock
from application.classes.car import Car

TEST_CAR1 = {
    "vin": '1234',
    "reg_no": 'WZ123',
    'model': 'Panamera',
    'brand': 'Porsche',
    'capacity': 100,
    'owner_id': 1
}


class TestCar(unittest.TestCase):

    def test_create_car(self):
        new_car = Car(**TEST_CAR1)
        self.assertEqual(new_car.vin, TEST_CAR1['vin'])
        self.assertEqual(new_car.brand, TEST_CAR1['brand'])
        self.assertEqual(new_car.owner_id, TEST_CAR1['owner_id'])

    @patch('application.classes.car.db_cur')
    def test_add_car_to_db(self, patch_db_cur):
        mock_client = Mock()
        mock_client.get_id.return_value = TEST_CAR1['owner_id']
        new_car = Car.add_car(mock_client, *list(TEST_CAR1.values())[:-1])
        patch_db_cur.execute.assert_called_once()
        self.assertEqual(new_car.owner_id, TEST_CAR1['owner_id'])
        self.assertEqual(new_car.reg_no, TEST_CAR1['reg_no'])

    @patch('application.classes.car.db_cur')
    def test_get_car_from_db(self, patch_db_cur):
        patch_db_cur.fetchone.return_value = list(TEST_CAR1.values())[1:]
        new_car = Car.get_car(TEST_CAR1['vin'])
        patch_db_cur.execute.assert_called_once()
        patch_db_cur.fetchone.assert_called_once()
        self.assertEqual(new_car.owner_id, TEST_CAR1['owner_id'])
        self.assertEqual(new_car.reg_no, TEST_CAR1['reg_no'])

    # @patch('application.classes.car.db_cur')
    # def test_get_client_cars_from_db(self, patch_db_cur):
