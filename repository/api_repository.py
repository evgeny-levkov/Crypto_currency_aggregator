from .base_repository import BaseRepository
from .api.base_api import BaseApi
from ..model.coin_model import CoinModel


class ApiRepository(BaseRepository):
    def __init__(self, api_dict: dict[str, BaseApi]) -> None:
        self.api_dict = api_dict

    def get_actual_price(self, coin: str, source: str) -> CoinModel | None:
       return self.api_dict[source].get_data(coin)[-1]

    def get_history_price(self, coin: str, limit: int =10000) -> list[CoinModel] | None:
        raise NotImplementedError