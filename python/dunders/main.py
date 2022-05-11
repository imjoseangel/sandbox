import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)

    def magnitude(self):
        """gives a more precise distance from origin"""
        return math.sqrt((self.x * self.x) + (self.y * self.y))

    def __len__(self):
        """returns the approximate distance from origin"""
        return round(self.magnitude())


p = Point(10, 5)
print(p)

points_list = [Point(i, i * 2) for i in range(1, 5)]
print(points_list)

points_dict = {str(i): Point(i, i * 3) for i in range(1, 5)}
print(points_dict)

p = Point(0, 0)
q = Point(1, 2)
print(q - p)

print(len(Point(3, 4)))
