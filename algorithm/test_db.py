from classes.carpark import Carpark
from classes.operator_mockup import Operator_mockup
from classes.balancer import Balancer
from database.to_database import To_database



def example():
    op = Operator_mockup(-50, 150)
    b = Balancer()
    cp = Carpark(1)

    demand = op.createDemand()
    cp.actualize()
    usage = b.balance(cp, demand)
    cp.charge()
    To_database.insert_new_charging(cp.active_charging_stations)
    To_database.insert_requests(demand, usage, 1)
    print(cp)
    print("Demand", demand)
    print("Usage:", usage)


if __name__=="__main__":
    example()

