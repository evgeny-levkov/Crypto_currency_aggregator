class AlertFactory():
    _alerts = {}
    @classmethod
    def registry_alerts(cls, name):
        def decorator(class_name):
            cls._alerts[name] = class_name
            return class_name
        return decorator

    @classmethod
    def give_alerts(cls, name, coin, source, **params):
        try:
            return cls._alerts[name](coin = coin, source = source, **params)
        except Exception as e:
            print(f'Нет такого алёрта: {e}')
            return None