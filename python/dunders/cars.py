from typing import List
from collections import namedtuple


class CarList:
    def __init__(self, cars: List):
        """Set up a hard-coded namedtuple class we can use"""
        self.cars = cars
        tuple_name = "Car"
        fields = ["price", "brand", "model", "year", "mileage", "color"]
        self.tuple_class = namedtuple(tuple_name, fields)

    def __iter__(self):
        """Start the iterator on the list of lists"""
        self.list_iterator = iter(self.cars)
        return self

    def __next__(self):
        """Convert each element to a named tuple"""
        try:
            row = self.list_iterator.__next__()
            return self.tuple_class(*row)
        # Redunancy explained in text below.
        except StopIteration:
            raise StopIteration


cars = [["6300", "toyota", "cruiser", "2008", "274117.0", "black"],
        ["2899", "ford", "se", "2011", "190552.0", "silver"],
        ["5350", "dodge", "mpv", "2018", "39590.0", "silver"],
        ["25000", "ford", "door", "2014", "64146.0", "blue"]]

car_tuples = CarList(cars)
for car in car_tuples:
    print(f"Found a car with brand = {car.brand} and model = {car.model}")
