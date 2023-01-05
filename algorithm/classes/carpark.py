from database.char_stat_from_db_creator import Char_stat_from_db_creator
from decimal import Decimal


class Carpark:
    def __init__(self, id):
        """
        Args:
            id:     Parking id.
        """
        self.id = id
        self.active_charging_stations = []
        self.current_time = None
        self.max_energy_usage = 0

    def __str__(self) -> str:
        stations = f"curent time:{self.current_time}\n"
        i = 0
        for station in self.active_charging_stations:
            stations += f"{i}. {station}\n\n"
            i += 1
        return stations

    def charge(self):
        for station in self.active_charging_stations:
            station.charge()

    def actualize(self, time_period=Decimal(0.25)):
        """
        Actualizes time and active charging stations.
        """
        self.active_charging_stations.clear()
        self.active_charging_stations = Char_stat_from_db_creator.get_charging_stations(
            self.id, time_period
        )
        self.current_time = Char_stat_from_db_creator.get_curr_time()
        self.calculate_max_energy_use()

    def grade_cars(self):
        """
        Decides the priority of charging for each parked car.
        """
        for station in self.active_charging_stations:
            station.set_tags(self.current_time)
            station.set_status()

    def sort_cars(self):
        """
        Sorts cars in active_charging_stations according to their status.
        """
        self.active_charging_stations.sort(key=lambda x: x.status)

    def calculate_max_energy_use(self):
        """
        Calculated max possible energy usage for whole carpark.
        """
        self.max_energy_usage = 0
        for station in self.active_charging_stations:
            self.max_energy_usage += station.max_energy_usage()

    def set_all_stations(self, order):
        """
        Sets all stations orders to given value (respecting constraints).

        Returns:
            Energy usage of a whole carpark, after seting orders.
        """
        usage = 0
        for station in self.active_charging_stations:
            station.set_order(order)
            usage += station.energy_usage()
        return usage

    def calculate_real_energy_use(self):
        """
        Calculates real energy usage of a whole carpark.

        Returns:
            Real energy usage of a whole carpark.
        """
        usage = 0
        for station in self.active_charging_stations:
            usage += station.energy_usage()
        return usage
