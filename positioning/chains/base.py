class Base(object):
    def __init__(self, **kwargs):
        self.params = kwargs

    def links(self):
        return []

    def calculate(self, *args):
        res = args
        for link in self.links():
            res = link(**self.params).calculate(*res)

        return res
