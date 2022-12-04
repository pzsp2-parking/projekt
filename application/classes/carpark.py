from charging_station import Charging_station

class Carpark:
    def __init__(self, id):
        self.parking_id = id
        self.active_charging_stations = []
        self.current_time = None
        self.max_energy_usage = 0

    def actualize(self):
        self.active_charging_stations.clear()
        # read database and repopulate active charging stations
        # read current time from database

    def tag_cars(self):
        for station in self.active_charging_stations:
            station.set_tags(self.current_time)
            station.set_status()

    def sort_cars(self):
        self.active_charging_stations.sort(key=lambda x: x.status)

    def calculate_max_energy_use(self):
        self.max_energy_usage = 0
        for station in self.active_charging_stations:
            self.max_energy_usage += station.max_energy_usage()

    def set_all_stations(self, order):
        usage = 0
        for station in self.active_charging_stations:
            station.set_order(order)
            usage += station.energy_usage()
        return usage

    def calculate_real_energy_use(self):
        usage = 0
        for station in self.active_charging_stations:
            usage += station.energy_usage()
        return usage
