from abc import abstractmethod, ABCMeta


class AbstractLocationStrategy(metaclass=ABCMeta):
    @abstractmethod
    def initialise(self, kwargs):
        pass

    @abstractmethod
    def locate(self, measures):
        pass
