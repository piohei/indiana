class BaseModel(object):
    def __eq__(self, other):
        return type(self) == type(other) and self.deep_eq_dict(self.__dict__, other.__dict__)

    def deep_eq_dict(self, a, b):
        if a.keys() != b.keys():
            return False

        for k in a.keys():
            if type(k) == dict:
                if not self.deep_eq_dict(a, b):
                    return False
            else:
                if a != b:
                    return False

        return True
