from classes.carpark import Carpark
from classes.operator_mockup import Operator_mockup
from classes.balancer import Balancer



def example():
    op = Operator_mockup(-50, 150)
    b = Balancer()
    cp = Carpark(1)

    demand = op.createDemand()
    cp.actualize()
    usage = b.balance(cp, demand)
    # cp.charge()
    print(cp)
    print("Demand", demand)
    print("Usage:", usage)


if __name__=="__main__":
    example()