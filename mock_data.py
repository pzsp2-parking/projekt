from prometheus_client import start_http_server, Gauge
from time import sleep
import random

PORT_PROMET = 8000
PARK_CHARGE = 20
ENERGY_CHARGE = 0.8
OPERATOR_CHARGE = 450

def main():
    start_http_server(PORT_PROMET)
    e_usg = Gauge("energy_usg", "Energy usage")
    e_req = Gauge("energy_req", "Energy requested usage")
    cars_nr = Gauge("cars_nr", "Number of cars on the parking")

    g_money_parked = Gauge("money_parked", "Funds obtained from parking fee.")
    g_money_charging = Gauge("money_charging", "Funds obtained from providing energy for cars charging.")
    g_money_operator = Gauge("money_operator", "Funds obtained from operator for fulfilling energy requests.")
    g_total_money = Gauge("total_money", "Total amount of already gathered payments.")
    g_total_capacity = Gauge("total_e_capacity", "Total energy capacity of cars gathered on the parking.")

    cars = [12]*7
    cars.extend([11]*4)
    cars.extend([10]*8)
    cars.extend([12]*7)
    cars.extend([11]*4)
    cars.extend([10]*8)

    usage = []
    requests = []

    money_parked = []
    money_charging = []
    money_operator = []
    total_money = []
    total_capacity = [850]
    print(len(cars))

    for i in range(len(cars)):
        usage.append(random.randint((cars[i]*15*3/5), int(cars[i]*15)))
        requests.append(usage[i]-random.randint(1, 40)+random.randint(1, 40))
        money_parked.append(cars[i]*PARK_CHARGE)
        money_charging.append(usage[i]*ENERGY_CHARGE)
        if (usage[i]-requests[i]):
            money_operator.append(1/abs(usage[i]-requests[i])*OPERATOR_CHARGE)
        else:
            money_operator.append(80)
        total_money.append(money_charging[i]+money_operator[i]+money_parked[i])
        total_capacity.append(cars[i]*total_capacity[i]*random.uniform(1.05, 1.3))

    #while True:
    for i in range(len(cars)):
        e_usg.set(usage[i])
        e_req.set(requests[i])
        cars_nr.set(cars[i])
        g_money_parked.set(money_parked[i])
        g_money_charging.set(money_charging[i])
        g_money_operator.set(money_operator[i])
        g_total_capacity.set(total_capacity[i])
        g_total_money.set(total_money[i])
        sleep(5)


if __name__ == "__main__":
    main()
