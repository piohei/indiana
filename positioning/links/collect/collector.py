from abc import ABCMeta, abstractmethod

from positioning.links.base import Base


class Collector(Base, metaclass=ABCMeta):
    @abstractmethod
    def to_fingertip(self, sample):
        pass

    def calculate(self, samples):
        return [list(map(self.to_fingertip, samples))]