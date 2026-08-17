from .base_fee import BaseFeeStrategy
from typing import Callable


class FeeFactory:
    fees = {}

    @classmethod
    def register_fee(cls, name: str) -> Callable:
        def decorator(register_class: type[BaseFeeStrategy]) -> type[BaseFeeStrategy]:
            cls.fees[name] = register_class
            return register_class
        return decorator

    @classmethod
    def give_fee(cls, name: str) -> BaseFeeStrategy | None:
        try:
            return cls.fees[name]()
        except Exception as e:
            print(f'Такого класса не существует:{e}')
            return None