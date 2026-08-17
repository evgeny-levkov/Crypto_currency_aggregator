from ..repository.crypto_repository import CryptoRepository
from ..exporters.exporter_factory import ExporterFactory
from ..exporters.base_exporter import BaseExporter
from typing import Any


class ExportService:
    def __init__(self, repository: CryptoRepository) -> None:
        self.repository = repository

    def export(self, exporter: str, coin: str, limit: int, filepath: str) -> Any | None:
        cls_exporter: BaseExporter = ExporterFactory.give_register(exporter)
        try:
            if cls_exporter is not None:
                return cls_exporter.export(self.repository.get_history_price(coin, limit), filepath)
            else:
                return 'Нет такого экспортёра'
        except Exception as e:
            return f'Ошибка{e}'