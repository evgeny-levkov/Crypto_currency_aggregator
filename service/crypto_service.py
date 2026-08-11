from ..repository.crypto_repository import CryptoRepository


class CryptoService():
    def __init__(self, crypto_repository: CryptoRepository):
        self.crypto_repository = crypto_repository
