from __future__ import annotations
from database.db_connector import db_cur

class Car:
    """Class representing a single car"""
    def __init__(self, VIN: str, nr_reg: str, en_level: float, model: str, brand: str, capacity: float) -> Car:
        """
        Args:
            VIN: VIN number of the car
            nr_reg: registration number of the car
            en_level: current energy level of the car
            model: model of the car
            brand: brand of the car
            capacity:   maximum capacity of car's tank

        Kwargs:
            kwarg:  A keyword argument.

        Returns:
            A new car instance.
        """
        self.VIN=VIN
        self.nr_reg = nr_reg
        self.en_level=en_level
        self.model=model
        self.brand=brand
        self.capacity=capacity

    @staticmethod
    def add_car(car: Car) -> None:
        stmt=f"INSERT INTO cars ({car.VIN}, password, name, surname, mail) VALUES ('guest', 'guest', 'guest');"

