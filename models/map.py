from models.base.base_db_model import BaseDBModel


class Map(BaseDBModel):
    def __init__(self, name, floor, walls, _id=None):
        super().__init__(_id)
        self.walls = walls
        self.floor = floor
        self.name = name

    def __str__(self):
        return "Map(name={})".format(self.name)
