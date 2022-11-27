class Charging_car:
    def __init__(self, charge_level, start_charge_level, parked_time, pickup_time, car_capacity, charger_type, charger_power, charger_id):
        self.charge_level = charge_level
        self.start_charge_level = start_charge_level
        self.parked_time = parked_time
        self.pickup_time = pickup_time
        self.car_capacity = car_capacity
        self.charger_type = charger_type
        self.charger_power = charger_power
        self.charger_id = charger_id



class Charging_station:
    def __init__(self, car, time_period=0.25):
        self.car = car
        self.order = 0     #-1 take energy 0 do nothing 1/2 charge with half power 1 charge with full power
        self.below_start = False    #taking energy would result in unaccteptable energy level
        self.hour_to_go = False     #hour or less remained from pickup
        self.status = 0             #bigger status results in car more likely being charged
        self.time_period = time_period

    def set_tags(self, current_time):
        # I do not know how datetime sql type will be handled in python so I will keep it abstract
        if self.car.pickup_time - current_time:
            self.hour_to_go = True
        if -self.car.charger_power * self.time_period + self.car.charge_level < self.car.start_charge_level:
            self.below_start = True

    def set_status(self):
        if self.hour_to_go:
            self.status += 10
        if self.below_start:
            self.status += 5
        if self.car.charger_type == 'AC':
            self.status += 5
        if self.car.charge_level > 80:
            self.status -= 5
        self.status += (100 - self.car.charge_level)/10

    def energy_usage(self):
        return self.order * self.car.charger_power * self.time_period
    
    def max_energy_usage(self):
        return self.car.charger_power * self.time_period
    
    def set_order(self, order):
        if self.hour_to_go:
            self.order = max(1, order)      # or 0.5?
        elif self.below_start:
            self.order = max(0.5, order)    # or 0?
        else:
            self.order = order
     
    

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

    def balance(self, energy_usage_demand):
        usage = 0
        if energy_usage_demand > self.max_energy_usage:
            usage = self.set_all_stations(1)
        elif energy_usage_demand > 0.5 * self.max_energy_usage:
            pass
            # to do
            # odpalić set_all_stations na 1 sprawdzić usage i zmniejszać ładowanie na 0.5 zaczynając od stacji z najniższym statusem?
        elif energy_usage_demand > 0:
            pass
            # to do
            # odpalić set_all_stations na 0.5 i idąc od najniższego statusu zmieniać na 0
        elif energy_usage_demand > -1 * self.max_energy_usage:
            # ustawić wszystko na 0 i od dołu listy zamieniać na -1 aż będzie wystarczajaco ok
            pass
        else:
            usage = self.set_all_stations(-1)
        return usage

    

    

    