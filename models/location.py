# -*- coding: utf-8 -*-

class Location:
    def __init__(self, x=0, y=0, z=0, dictionary=None):
        if dictionary is not None:
            x = dictionary['x']
            y = dictionary['y']
            z = dictionary['z']
        self.x = x
        self.y = y
        self.z = z

    def distnace_from(self, loc):
        return math.sqrt(
                   math.pow(self.x - loc.x, 2) + \
                   math.pow(self.y - loc.y, 2) + \
                   math.pow(self.z - loc.z, 2)
               )    

    def save(self):
        return db.replace_one(filter={
                                  'location.x': fingertip.location['x'],
                                  'location.y': fingertip.location['y'],
                                  'location.z': fingertip.location['z']
                              },
                              replacement=self.to_dict()
                             )

    def to_dict(self):
        return self.__dict__

    def __str__(self, *args, **kwargs):
        return "Location[{}; {}; {}]".format(self.x, self.y, self.z)
