from carpark import Carpark

class Balancer:
    def balance(self, carpark:Carpark, energy_usage_demand):
        usage = 0
        carpark.tag_cars()
        carpark.sort_cars()
        if energy_usage_demand > carpark.max_energy_usage:
            usage = self._balance_case(carpark, energy_usage_demand, (1,))
        elif energy_usage_demand > 0.5 * carpark.max_energy_usage:
            usage = self._balance_case(carpark, energy_usage_demand, (1, 0.5, 0, 1))
        elif energy_usage_demand > 0:
            usage = self._balance_case(carpark, energy_usage_demand, (0.5, 0, -1))
        elif energy_usage_demand > -1 * carpark.max_energy_usage:
            usage = self._balance_case(carpark, energy_usage_demand, (0, -1))
        else:
            usage = self._balance_case(carpark, energy_usage_demand, (-1))
        return usage
    

    def _set_orders(self, carpark:Carpark, energy_usage_demand, usage, order_to_balance, margin=0.1):
        sign = -1 if energy_usage_demand < 0 else 1
        demand_met = False
        for station in carpark.active_charging_stations:
            if usage < energy_usage_demand * (1 + sign * margin):       # we start with usage bigger than expected so we end balancing when usage is smaller than expected usage + margin
                demand_met = True
                break
            station.set_order(order_to_balance)
            usage = carpark.calculate_real_energy_use()
        return usage, demand_met


    def _balance_case(self, carpark:Carpark, energy_usage_demand, orders_to_balance:tuple):
        balance_attempts = len(orders_to_balance)
        curr_order_index = 0
        usage = carpark.set_all_stations(orders_to_balance[curr_order_index])
        curr_order_index += 1
        demand_met = False
        while curr_order_index < balance_attempts and not demand_met:
            usage, demand_met = self._set_orders(carpark, energy_usage_demand, usage, orders_to_balance[curr_order_index])
            curr_order_index += 1
        return usage
