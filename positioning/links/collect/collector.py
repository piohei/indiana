from abc import ABCMeta, abstractmethod

from positioning.links.base import Base


class Collector(Base, metaclass=ABCMeta):
    @abstractmethod
    def to_fingertip(self, sample):
        pass

    def calculate(self, samples, **kwargs):
        return {"fingertips": list(map(self.to_fingertip, samples))}