from product import Product

class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self._product: Product = product
        self._quantity: int = quantity

    @property
    def product(self) -> Product:
        return self._product

    @property
    def quantity(self) -> int:
        return self._quantity

    def calculate_subtotal(self) -> float:
        return self._product.price * self._quantity