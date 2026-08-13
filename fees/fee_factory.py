from .base_fee import BaseFeeStrategy


class FeeFactory:
    fees = {}

    @classmethod
    def register_fee(cls, name):
        def decorator(register_class):
            cls.fees[name] = register_class
            return register_class
        return decorator

    @classmethod
    def give_fee(cls, name) -> BaseFeeStrategy:
        try:
            return cls.fees[name]()
        except Exception as e:
            print(f'Такого класса не существует:{e}')
            return None