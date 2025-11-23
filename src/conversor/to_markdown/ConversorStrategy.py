from abc import ABC, abstractmethod


class ConversorStrategy(ABC):
    @abstractmethod
    def convert(self):
        pass