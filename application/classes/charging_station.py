from charging_car import Charging_car

class Charging_station:
    def __init__(self, car:Charging_car, time_period=0.25):
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
        if self.car.charge_level * self.car.car_capacity - self.car.charger_power * self.time_period < self.car.start_charge_level * self.car.car_capacity:
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
            self.order = max(0.5, order)      # or 0.5?
        elif self.below_start:
            self.order = max(0, order)    # or 0?
        else:
            self.order = order
