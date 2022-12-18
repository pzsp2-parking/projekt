from random import randint

class Operator_mockup:
    def __init__(self, min, max) -> None:
        self.min = min
        self.max = max

    def createDemand(self):
        return randint(self.min, self.max)