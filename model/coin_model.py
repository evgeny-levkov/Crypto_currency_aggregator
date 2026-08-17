from datetime import datetime
from dataclasses import dataclass


@dataclass
class CoinModel:
    name: str
    time: datetime | None
    price: float | None
    source: str