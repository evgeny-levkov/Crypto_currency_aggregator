from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass(init=False)
class AlertModel:
    alert_type: str
    coin: str
    source: str
    id: Optional[int]
    alert_params: dict

    def __init__(self, alert_type: str, coin: str, source: str, id: Optional[int] = None, **params: Any) -> None:
        self.id = id
        self.alert_type = alert_type
        self.coin = coin
        self.source = source
        self.alert_params: dict[str, Any] = params