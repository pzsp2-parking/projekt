from prometheus_client import start_http_server, Gauge
from time import sleep
import random

from classes.carpark import Carpark
from classes.operator_mockup import Operator_mockup
from classes.balancer import Balancer
from database.to_database import To_database
PORT_PROMET=8000



def main():
    start_http_server(PORT_PROMET)
    e_usg = Gauge('energy_usg', 'Energy usage')
    e_req = Gauge('energy_req', 'Energy requested usage')
    cars_nr = Gauge('cars_nr', 'Number of cars on the parking')
    
    op = Operator_mockup(-50, 150)
    b = Balancer()
    cp = Carpark(1)

    cp.charge()
    while True:
        demand = op.createDemand()
        cp.actualize()
        usage = b.balance(cp, demand)
        To_database.insert_new_charging(cp.active_charging_stations)
        To_database.insert_requests(demand, usage, 1)
        e_usg.set(usage)
        e_req.set(demand)
        cars_nr.set(len(cp.active_charging_stations))
        sleep(5)
    

if __name__=="__main__":
    main()