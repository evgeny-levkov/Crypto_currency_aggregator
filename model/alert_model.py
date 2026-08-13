class AlertModel:
    def __init__(self, alert_type, coin, source, id = None, **params):
        self.id = id
        self.alert_type = alert_type
        self.coin = coin
        self.source = source
        self.alert_params = params