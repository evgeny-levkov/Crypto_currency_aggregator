from abc import ABC, abstractmethod


class BaseAlert(ABC):
    @abstractmethod
    def check(self, price) -> bool:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass