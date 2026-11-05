from abc import ABC, abstractmethod
from supplier import Supplier

class Product(ABC):
    def __init__(self, product_id: int, name: str, price: float, stock: int, supplier: Supplier):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock = stock
        self._supplier: Supplier = supplier

    @property
    def product_id(self) -> int:
        return self._product_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @property
    def stock(self) -> int:
        return self._stock

    @property
    def supplier(self) -> Supplier:
        return self._supplier

    def update_stock(self, quantity: int) -> None:
        self._stock += quantity

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    @abstractmethod
    def display_information(self) -> None:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass