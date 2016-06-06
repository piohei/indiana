import math

class Location:
    def __init__(self, x=0, y=0, z=0, dictionary=None):
        if dictionary is not None:
            x = dictionary['x']
            y = dictionary['y']
            z = dictionary['z']
        self.x = x
        self.y = y
        self.z = z

    def to_dict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}

    def __str__(self, *args, **kwargs):
        return str(self.x) + ';' + str(self.y) + ';' + str(self.z)

    def distance_from(self, loc):
        return math.sqrt(math.pow(self.x - loc.x, 2) + math.pow(self.y - loc.y, 2) + math.pow(self.z - loc.z, 2))


class APData(object):
    def __init__(self, device_MAC='', router_MAC='', timestamp='', rssi=0, channel=-1, tuple=None, dictionary=None):
        if tuple is not None:
            device_MAC = tuple[0]
            router_MAC = tuple[1]
            timestamp = tuple[2]
            rssi=tuple[3]
            channel = tuple[4]
        elif dictionary is not None:
            device_MAC = dictionary['device_MAC']
            router_MAC = dictionary['router_MAC']
            timestamp = dictionary['timestamp']
            rssi = dictionary['rssi']
            channel = dictionary['channel']
        self.device_MAC = device_MAC
        self.router_MAC = router_MAC
        self.timestamp = timestamp
        self.rssi = rssi
        self.channel = channel

    def to_dict(self):
        return self.__dict__
