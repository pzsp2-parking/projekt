import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import unittest
import datetime
from decimal import Decimal
from classes.charging_car import Charging_car
from classes.charging_station import Charging_station
from classes.carpark import Carpark

TEST_CAR1 = {
    "charge_level": Decimal(50),    # below_start sets for this car
    "start_charge_level": Decimal(40),
    "pickup_time": datetime.datetime(2023, 6, 9),
    "car_capacity": Decimal(90),
    "charger_type": "DC",
    "charger_power": Decimal(100)
}
TEST_CAR4 = {
    "charge_level": Decimal(90),
    "start_charge_level": Decimal(40),
    "pickup_time": datetime.datetime(2023, 6, 9),
    "car_capacity": Decimal(100),
    "charger_type": "DC",
    "charger_power": Decimal(80)
}
car = Charging_car(**TEST_CAR1)
car2 = Charging_car(**TEST_CAR4)
station1 = Charging_station(car, 1, 20)
station2 = Charging_station(car, 2, 20)
station3 = Charging_station(car2, 3, 20)
station4 = Charging_station(car2, 4, 20)

class TestCarpark(unittest.TestCase):
    def test_create_carpark(self):
        carpark = Carpark(20)
        self.assertEqual(carpark.id, 20)


    def test_max_energy_use(self):
        carpark = Carpark(20)
        carpark.active_charging_stations.append(station1)
        carpark.active_charging_stations.append(station2)
        carpark.calculate_max_energy_use()
        self.assertEqual(carpark.max_energy_usage, 50)


    def test_real_energy_use(self):
        carpark = Carpark(20)
        station1.order = 0.5
        station2.order = 0
        carpark.active_charging_stations.append(station1)
        carpark.active_charging_stations.append(station2)
        usage = carpark.calculate_real_energy_use()
        self.assertEqual(usage, 12.5)


    def test_set_all_stations(self):
        carpark = Carpark(20)
        station1.below_start = True
        station2.hour_to_go = True
        carpark.active_charging_stations.append(station1)
        carpark.active_charging_stations.append(station2)
        carpark.active_charging_stations.append(station3)
        carpark.set_all_stations(-1)
        self.assertEqual(station1.order, 0)
        self.assertEqual(station2.order, 0.5)
        self.assertEqual(station3.order, -1)


    def test_sort_cars(self):
        carpark = Carpark(20)
        station1.status = 9
        station2.status = 7
        station3.status = 8
        station4.status = 6
        carpark.active_charging_stations.append(station1)
        carpark.active_charging_stations.append(station2)
        carpark.active_charging_stations.append(station3)
        carpark.active_charging_stations.append(station4)
        carpark.sort_cars()
        self.assertEqual(carpark.active_charging_stations[0], station4)
        self.assertEqual(carpark.active_charging_stations[1], station2)
        self.assertEqual(carpark.active_charging_stations[2], station3)
        self.assertEqual(carpark.active_charging_stations[3], station1)


        

if __name__ == '__main__':
    unittest.main()