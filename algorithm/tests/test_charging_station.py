import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import unittest
from decimal import Decimal
import datetime
from classes.charging_car import Charging_car
from classes.charging_station import Charging_station


TEST_CAR1 = {
    "charge_level": Decimal(50),  # below_start sets for this car
    "start_charge_level": Decimal(40),
    "pickup_time": datetime.datetime(2023, 6, 9),
    "car_capacity": Decimal(90),
    "charger_type": "DC",
    "charger_power": Decimal(90),
}
TEST_CAR4 = {
    "charge_level": Decimal(90),
    "start_charge_level": Decimal(40),
    "pickup_time": datetime.datetime(2023, 6, 9),
    "car_capacity": Decimal(100),
    "charger_type": "DC",
    "charger_power": Decimal(80),
}
TEST_CAR3 = {
    "charge_level": Decimal(70),
    "start_charge_level": Decimal(40),
    "pickup_time": datetime.datetime(2023, 6, 9),
    "car_capacity": Decimal(110),
    "charger_type": "DC",
    "charger_power": Decimal(80),
}
TEST_CAR2 = {
    "charge_level": Decimal(50),
    "start_charge_level": Decimal(45),
    "pickup_time": datetime.datetime(2023, 6, 9),
    "car_capacity": Decimal(100),
    "charger_type": "AC",
    "charger_power": Decimal(15),
}


class TestCharging_station(unittest.TestCase):
    def test_create_station(self):
        new_car = Charging_car(**TEST_CAR1)
        new_station = Charging_station(new_car, 12, 20)
        self.assertEqual(new_station.car, new_car)
        self.assertEqual(new_station.charger_id, 12)
        self.assertEqual(new_station.carpark_id, 20)
        self.assertEqual(new_station.carpark_id, 20)
        self.assertEqual(new_station.order, 0)
        self.assertEqual(new_station.below_start, False)
        self.assertEqual(new_station.hour_to_go, False)
        self.assertEqual(new_station.time_period, Decimal(0.25))

    def test_set_hour_to_go(self):
        new_car = Charging_car(**TEST_CAR1)
        new_station = Charging_station(new_car, 12, 20)
        new_station.set_hour_to_go(
            TEST_CAR1["pickup_time"] + datetime.timedelta(minutes=-30)
        )
        self.assertEqual(new_station.hour_to_go, True)

    def test_set_hour_to_go2(self):
        new_car = Charging_car(**TEST_CAR1)
        new_station = Charging_station(new_car, 12, 20)
        new_station.set_hour_to_go(
            TEST_CAR1["pickup_time"] + datetime.timedelta(minutes=-90)
        )
        self.assertEqual(new_station.hour_to_go, False)

    def test_set_below_start2(self):
        car = Charging_car(**TEST_CAR2)
        new_station = Charging_station(car, 12, 20)
        new_station.set_below_start()
        self.assertEqual(new_station.below_start, False)

    def test_set_below_start(self):
        car = Charging_car(**TEST_CAR1)
        new_station = Charging_station(car, 12, 20)
        new_station.set_below_start()
        self.assertEqual(new_station.below_start, True)

    def test_set_status(self):
        car = Charging_car(**TEST_CAR3)
        station = Charging_station(car, 12, 20)
        station.set_tags(TEST_CAR3["pickup_time"] + datetime.timedelta(minutes=-90))
        station.set_status()
        self.assertEqual(station.status, 3)

    def test_set_status2(self):
        car = Charging_car(**TEST_CAR1)
        station = Charging_station(car, 12, 20)
        station.set_tags(TEST_CAR3["pickup_time"] + datetime.timedelta(minutes=-90))
        station.set_status()
        self.assertEqual(station.status, 10)

    def test_set_status3(self):
        car = Charging_car(**TEST_CAR2)
        station = Charging_station(car, 12, 20)
        station.set_tags(TEST_CAR3["pickup_time"] + datetime.timedelta(minutes=-90))
        station.set_status()
        self.assertEqual(station.status, 10)

    def test_set_status4(self):
        car = Charging_car(**TEST_CAR2)
        station = Charging_station(car, 12, 20)
        station.set_tags(TEST_CAR3["pickup_time"] + datetime.timedelta(minutes=-20))
        station.set_status()
        self.assertEqual(station.status, 20)

    def test_set_status5(self):
        car = Charging_car(**TEST_CAR4)
        station = Charging_station(car, 12, 20)
        station.set_tags(TEST_CAR3["pickup_time"] + datetime.timedelta(minutes=-90))
        station.set_status()
        self.assertEqual(station.status, -4)

    def test_max_energy_usage(self):
        car = Charging_car(**TEST_CAR4)
        station = Charging_station(car, 12, 20)
        self.assertEqual(station.max_energy_usage(), Decimal(20))

    def test_set_order(self):
        car = Charging_car(**TEST_CAR2)
        station = Charging_station(car, 12, 20)
        station.set_tags(TEST_CAR2["pickup_time"] + datetime.timedelta(minutes=-90))
        station.set_order(1)
        self.assertEqual(station.order, 1)
        station.set_order(0.5)
        self.assertEqual(station.order, 0.5)
        station.set_order(0)
        self.assertEqual(station.order, 0)
        station.set_order(-1)
        self.assertEqual(station.order, -1)

    def test_set_order2(self):
        car = Charging_car(**TEST_CAR1)
        station = Charging_station(car, 12, 20)
        station.set_tags(TEST_CAR2["pickup_time"] + datetime.timedelta(minutes=-90))
        station.set_order(1)
        self.assertEqual(station.order, 1)
        station.set_order(0.5)
        self.assertEqual(station.order, 0.5)
        station.set_order(0)
        self.assertEqual(station.order, 0)
        station.set_order(-1)
        self.assertEqual(station.order, 0)

    def test_set_order3(self):
        car = Charging_car(**TEST_CAR2)
        station = Charging_station(car, 12, 20)
        station.set_tags(TEST_CAR2["pickup_time"] + datetime.timedelta(minutes=-20))
        station.set_order(1)
        self.assertEqual(station.order, 1)
        station.set_order(0.5)
        self.assertEqual(station.order, 0.5)
        station.set_order(0)
        self.assertEqual(station.order, 0.5)
        station.set_order(-1)
        self.assertEqual(station.order, 0.5)

    def test_energy_usage(self):
        car = Charging_car(**TEST_CAR4)
        station = Charging_station(car, 12, 20)
        station.set_tags(TEST_CAR4["pickup_time"] + datetime.timedelta(minutes=-90))
        station.set_order(0)
        self.assertEqual(station.energy_usage(), Decimal(0))
        station.set_order(-1)
        self.assertEqual(station.energy_usage(), Decimal(-20))
        station.set_order(0.5)
        self.assertEqual(station.energy_usage(), Decimal(10))


if __name__ == "__main__":
    unittest.main()
