class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def __sub__(self, other: Point):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)


p = Point(10, 5)
print(p)

points_list = [Point(i, i * 2) for i in range(1, 5)]
print(points_list)

points_dict = {str(i): Point(i, i * 3) for i in range(1, 5)}
print(points_dict)
