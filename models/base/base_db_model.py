import random

from bson.objectid import ObjectId

from .base_model import BaseModel


class BaseDBModel(BaseModel):
    def __init__(self, _id=None):
        _id = self.generate_id() if _id is None else _id
        self._id = ObjectId(_id)

    @staticmethod
    def generate_id():
        return ''.join(random.choice("abcdef0123456789") for _ in range(24))
