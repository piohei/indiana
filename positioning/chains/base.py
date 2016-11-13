class Base(object):
    def __init__(self, **kwargs):
        self.params = kwargs

    def links(self):
        return []

    def calculate(self, **kwargs):
        res = kwargs
        for link in self.links():
            res = link(**self.params).calculate(**res)

        return res
