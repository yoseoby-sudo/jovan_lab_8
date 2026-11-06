import math
from abc import ABC, abstractmethod
from supplier import Supplier

class Product(ABC):
    def __init__(self, product_id: int, name: str, price: float, stock: int, supplier: Supplier):

        if not isinstance(product_id, int) or isinstance(product_id, bool) or product_id <= 0:
            raise ValueError("Product ID must be a positive integer.")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty.")

        if not isinstance(price, (int, float)) or isinstance(price, bool) or not math.isfinite(price) or price < 0:
            raise ValueError("Price must be a valid non-negative number.")

        if not isinstance(stock, int) or isinstance(stock, bool) or stock < 0:
            raise ValueError("Stock must be a non-negative integer.")

        if not isinstance(supplier, Supplier):
            raise TypeError("Supplier must be a Supplier object.")

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
        if not isinstance(quantity, int) or isinstance(quantity, bool):
             raise TypeError("Stock quantity must be an integer.")

        if self._stock + quantity < 0:
            raise ValueError("Insufficient stock.")

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