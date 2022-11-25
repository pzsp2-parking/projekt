from prometheus_client import start_http_server, Gauge
from time import sleep
import random
PORT_PROMET=8000

def curr_energy_usg():
    return random.randint(20, 40) 

def curr_car_nr():
    return random.randint(80, 120) 

def energy_req():
    return random.randint(15, 45) 

def main():
    start_http_server(PORT_PROMET)
    e_usg = Gauge('energy_usg', 'Energy usage')
    e_req = Gauge('energy_req', 'Energy requested usage')
    cars_nr = Gauge('cars_nr', 'Number of cars on the parking')
    while True:
        e_usg.set(curr_energy_usg())
        e_req.set(energy_req())
        cars_nr.set(curr_car_nr())
        sleep(5)
    

if __name__=="__main__":
    main()