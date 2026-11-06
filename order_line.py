from product import Product

class OrderLine:
    def __init__(self, product: Product, quantity: int):

        if not isinstance(product, Product):
            raise TypeError("Product must be a Product object.")

        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        if quantity > product.stock:
            raise ValueError("Insufficient stock for this product.")

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
