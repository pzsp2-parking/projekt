from classes.carpark import Carpark
from decimal import Decimal

class Balancer:
    def balance(self, carpark:Carpark, energy_usage_demand):
        """
        Sets chargers' power to satisfy energy usage demand.

        Args:
            carpark:                Carpark to preform balancing on..
            Energy_usage_demand:    energy usage requested by operator.

        Returns:
            Approximate energy to be used by given carpark.
        """
        usage = 0
        carpark.grade_cars()
        carpark.sort_cars()
        energy_usage_demand = Decimal(energy_usage_demand)
        if energy_usage_demand > carpark.max_energy_usage:
            usage = self._balance_case(carpark, energy_usage_demand, (1,))
        elif energy_usage_demand > Decimal(0.5) * carpark.max_energy_usage:
            usage = self._balance_case(carpark, energy_usage_demand, (1, 0.5, 0, 1))
        elif energy_usage_demand > 0:
            usage = self._balance_case(carpark, energy_usage_demand, (0.5, 0, -1))
        elif energy_usage_demand > Decimal(-1) * carpark.max_energy_usage:
            usage = self._balance_case(carpark, energy_usage_demand, (0, -1))
        else:
            usage = self._balance_case(carpark, energy_usage_demand, (-1,))
        return usage
    
    def _set_orders(self, carpark:Carpark, energy_usage_demand, usage, order_to_balance, margin=Decimal(0.1)):
        """
        Sets sets stations' orders by one, to new value (respecting constraints) untill energy usage demand is met or untill it runs out of stations.
        
        Args:
            carpark:                Carpark to preform this operation on.
            energy_usage_demand:    Demand to be met.
            usage:                  Estimated usage before any changes to stations' orders.
            order_to_balance:       New power value to set charging station power to.
            margin:     

        Returns:
            Approximate energy to be used by given carpark.
        """
        # sign = -1 if energy_usage_demand < 0 else 1
        sign = 1
        demand_met = False
        for station in carpark.active_charging_stations:
            if usage < energy_usage_demand * (1 + sign * margin):       # we start with usage bigger than expected so we end balancing when usage is smaller than expected usage + margin
                demand_met = True
                break
            station.set_order(order_to_balance)
            usage = carpark.calculate_real_energy_use()
        return usage, demand_met

    def _balance_case(self, carpark:Carpark, energy_usage_demand, orders_to_balance:tuple):
        """
        Calls _set_orders several times with diffrent orders untill energy usage demand is satisfied or we run out od orders.

        Args:
            carpark:                Carpark to preform operation on.
            energy_usage_demand:    Demand to met.
            orders_to_balance:      iterable of orders to apply to stations

        Returns:
            Approximate energy to be used by given carpark.
        """
        balance_attempts = len(orders_to_balance)
        curr_order_index = 0
        usage = carpark.set_all_stations(orders_to_balance[curr_order_index])
        curr_order_index += 1
        demand_met = False
        while curr_order_index < balance_attempts and not demand_met:
            usage, demand_met = self._set_orders(carpark, energy_usage_demand, usage, orders_to_balance[curr_order_index])
            curr_order_index += 1
        return usage
