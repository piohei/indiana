from bson.objectid import ObjectId
from helpers.utils import generate_id

from .base_model import BaseModel


class BaseDBModel(BaseModel):
    def __init__(self, _id=None):
        _id = generate_id() if _id is None else _id
        self._id = ObjectId(_id)
