class Train:
    def get_fuels(self):
        return 'diesel'

    def get_speed(self):
        return "200Km/hr"

    def get_type(self):
        return "A train"


class Bus:
    def get_fuels(self):
        return 'electricity'

    def get_speed(self):
        return "80Km/hr"

    def get_type(self):
        return "A bus"


class Transport:
    def __init__(self, transport):
        self.transport = transport

    def travel(self):
        fuels = self.transport.get_fuels()
        return f'{self.transport.get_type()} uses {fuels}'

    def distance_covered(self, hrs):
        km = int(self.transport.get_speed().strip("Km/hr")) * hrs
        return f'{self.transport.get_type()} covers {km}Km in {hrs} hours'


train = Transport(Train())
bus = Transport(Bus())

print(train.travel())
print(bus.travel())
print(train.distance_covered(3))
print(bus.distance_covered(3))
