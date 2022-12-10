import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import unittest
from decimal import Decimal
from datetime import datetime
from classes.charging_car import Charging_car

TEST_CAR1 = {
    "charge_level": Decimal(50),
    "start_charge_level": 40,
    "pickup_time": datetime(2023, 6, 9),
    "car_capacity": Decimal(90),
    "charger_type": "AC",
    "charger_power": Decimal(90)
}


class TestCharging_car(unittest.TestCase):

    def test_create_car(self):
        new_car = Charging_car(**TEST_CAR1)
        self.assertEqual(new_car.charge_level, TEST_CAR1['charge_level'])
        self.assertEqual(new_car.start_charge_level, TEST_CAR1['start_charge_level'])
        self.assertEqual(new_car.pickup_time, TEST_CAR1['pickup_time'])
        self.assertEqual(new_car.car_capacity, TEST_CAR1['car_capacity'])
        self.assertEqual(new_car.charger_type, TEST_CAR1['charger_type'])
        self.assertEqual(new_car.charger_power, TEST_CAR1['charger_power'])

if __name__ == '__main__':
    unittest.main()
