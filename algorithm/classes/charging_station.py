from classes.charging_car import Charging_car
from decimal import Decimal
import datetime


class Charging_station:
    def __init__(
        self, car: Charging_car, charger_id, carpark_id, time_period=Decimal(0.25)
    ):
        """
        Args:
            car:            Charging_car object representing car connected to this station.
            charger_id:     Charging station id.
            carpark_id:     Carpark id.
            time_period:    how long is order going to be set up.
        """
        self.car = car
        self.charger_id = charger_id
        self.carpark_id = carpark_id  # Charging station id
        self.order = 0  # -1 take energy 0 do nothing 1/2 charge with half power 1 charge with full power
        self.below_start = (
            False  # taking energy would result in unaccteptable energy level
        )
        self.hour_to_go = False  # hour or less remained from pickup
        self.status = 0  # bigger status results in car more likely being charged
        self.time_period = time_period
        self.new_charge_level = 0

    def __str__(self) -> str:
        return f"carpark: {self.carpark_id}, charger: {self.charger_id}\ncar:\n{self.car}\n\n\torder: {self.order}\n\tnew charge level: {self.new_charge_level}"

    def set_tags(self, current_time):
        """
        Checks if discharging car would bring it's energy level below starting energy level and sets tag.
        Checks if car is about to get picked up in less than an hour and sets appropriate tag.

        Args:
            current_time:      Current time.
        """
        # I do not know how datetime sql type will be handled in python so I will keep it abstract
        self.set_below_start()
        self.set_hour_to_go(current_time)

    def set_hour_to_go(self, current_time):
        """
        Checks if car is about to get picked up in less than an hour and sets appropriate tag.

        Args:
            current_time:      Current time.
        """
        time_to_go = self.car.pickup_time - current_time
        if (
            time_to_go <= datetime.timedelta(hours=1)
            and time_to_go >= datetime.timedelta()
        ):
            self.hour_to_go = True

    def set_below_start(self):
        """
        Checks if discharging car would bring it's energy level below starting energy level and sets tag.

        Args:
            current_time:      Current time.
        """
        if (
            self.car.charge_level * self.car.car_capacity / 100
            - self.car.charger_power * self.time_period
            < self.car.start_charge_level * self.car.car_capacity / 100
        ):
            self.below_start = True

    def charge(self):
        """
        Sets new battery level of a car (in real project it would be sensed by the real charging station).
        """
        new = (
            (
                self.car.charge_level * self.car.car_capacity / 100
                + Decimal(self.order) * self.car.charger_power * self.time_period
            )
            / self.car.car_capacity
            * 100
        )
        self.new_charge_level = min(new, 100)

    def set_status(self):
        """
        Sets charging station priority to be receive higher order.
        """
        if self.hour_to_go:
            self.status += 10
        if self.below_start:
            self.status += 5
        if self.car.charger_type == "AC":
            self.status += 5
        if self.car.charge_level > 80:
            self.status -= 5
        self.status += (100 - self.car.charge_level) / 10

    def energy_usage(self):
        """
        Calculates charging station's energy usage.

        Returns:
            Energy usage.
        """
        return Decimal(self.order) * self.car.charger_power * self.time_period

    def max_energy_usage(self):
        """
        Calculates max posible charging station's energy usage.

        Returns:
            Max posiible energy usage.
        """
        return self.car.charger_power * self.time_period

    def set_order(self, order):
        """
        Sets station's order to given power, respecting constraints.
        Args:
            order:  Power on with charging power should now operate.
        """
        if self.hour_to_go:
            self.order = max(0.5, order)  # or 0.5?
        elif self.below_start:
            self.order = max(0, order)  # or 0?
        else:
            self.order = order
