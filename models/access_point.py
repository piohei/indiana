from models.base.base_db_model import BaseDBModel
from models.primitives.location import Location
from models.primitives.mac import Mac


class AccessPoint(BaseDBModel):
    def __init__(self, number, name, location, mac, active, _id=None):
        super().__init__(_id)
        if type(mac) != Mac:
            raise ValueError('Argument mac must be type of models.Mac')
        if type(location) != Location:
            raise ValueError("Argument location must be type of models.Location")
        if type(number) != int:
            raise ValueError('Argument number must be of type int')
        if type(name) != str:
            raise ValueError('Argument name must be of type str')
        if type(active) != bool:
            raise ValueError('Argument active must be of type bool')
        self.active = active
        self.mac = mac
        self.location = location
        self.name = name
        self.number = number

    def __str__(self):
        return "AccessPoint(id={}, name={}, location={}, mac={}, number={}, active={})".format(
                self._id, self.name, self.location, self.mac, self.number, self.active)
