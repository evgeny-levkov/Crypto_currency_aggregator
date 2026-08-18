from .base_alert import BaseAlert
from typing import Callable, Any


class AlertFactory:
    _alerts: dict[str, type[BaseAlert]] = {}

    @classmethod
    def registry_alerts(cls, name: str) -> Callable:
        def decorator(class_name: type[BaseAlert]) -> type[BaseAlert]:
            cls._alerts[name] = class_name
            return class_name
        return decorator

    @classmethod
    def give_alerts(cls, name: str, coin: str, source: str, **params: Any) -> BaseAlert | None:
        try:
            return cls._alerts[name](coin = coin, source = source, **params)
        except Exception as e:
            print(f'Нет такого алёрта: {e}')
            return None
    @classmethod
    def get_alert_fields(cls, name: str) -> dict[str, Any] | None:
        try:
            return cls._alerts[name].get_fields()
        except Exception as e:
            print(f'Ошибка {e}')
            return None