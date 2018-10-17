from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def __iter__():
        pass

    @abstractmethod
    def __getitem__(key):
        pass
