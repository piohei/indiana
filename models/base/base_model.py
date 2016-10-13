from helpers.utils import deep_eq_dict

class BaseModel(object):
    def __eq__(self, other):
        return type(self) == type(other) and deep_eq_dict(self.__dict__, other.__dict__)
