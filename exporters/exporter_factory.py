from .base_exporter import BaseExporter
from ..model.coin_model import CoinModel


class ExporterFactory:
    _varients_export = {}

    @classmethod
    def register_exporters(cls, name):
        def decorator(register_class):
            cls._varients_export[name] = register_class
            return register_class
        return decorator

    @classmethod
    def give_register(cls, name):
        try:
            return cls._varients_export[name]()
        except Exception as e:
            print(f"Такого класса не существует{e}")
            return None