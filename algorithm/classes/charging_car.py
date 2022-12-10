class Charging_car:
    def __init__(self, charge_level, start_charge_level, pickup_time, car_capacity, charger_type, charger_power):
        """
        Args:
            charge_level:           Current charging level of car battery.
            start_charge_level:     Charging level at which car was parked.
            pickup_time:            Time at which car is going to get picked up.
            car_capacity:           Car battery capacity.
            charger_type:           AC or DC.
            charger_power:          Max power of the charger.
        """
        self.charge_level = charge_level
        self.start_charge_level = start_charge_level
        self.pickup_time = pickup_time
        self.car_capacity = car_capacity
        self.charger_type = charger_type
        self.charger_power = charger_power
