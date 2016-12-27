from abc import ABCMeta, abstractmethod

from positioning.links.base import Base


class Collector(Base, metaclass=ABCMeta):
    @abstractmethod
    def to_fingerprint(self, sample):
        pass

    def calculate(self, samples, **kwargs):
        return {"fingerprints": list(map(self.to_fingerprint, samples))}