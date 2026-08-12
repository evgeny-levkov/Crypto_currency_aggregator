class AlertModel:
    def __init__(self, alert_price, coin: str, source, opr, id = None):
        self.id = id
        self.alert_price = alert_price
        self.coin = coin
        self.source = source
        self.opr = opr