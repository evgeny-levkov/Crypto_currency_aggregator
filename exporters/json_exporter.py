from .base_exporter import BaseExporter
from ..model.coin_model import CoinModel
import json
from .exporter_factory import ExporterFactory


@ExporterFactory.register_exporters("json")
class JsonExporter(BaseExporter):
    def export(self, data: list[CoinModel], filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            data_dict = [{"name":coins.name, "time": coins.time, "price": coins.price, "source": coins.source} for coins in data]
            json.dump(data_dict, f, ensure_ascii=False, indent=4)