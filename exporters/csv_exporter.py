from .base_exporter import BaseExporter
from ..model.сoin_model import CoinModel
import csv
from .exporter_factory import ExporterFactory


@ExporterFactory.register_exporters("csv")
class CsvExporter(BaseExporter):
    def export(self, data: list[CoinModel], filepath):
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "time", "price", "source"])
            writer.writeheader()
            data_dict = [{"name":coins.name, "time": coins.time, "price": coins.price, "source": coins.source} for coins in data]
            for i in data_dict:
                writer.writerow(i)
        return writer