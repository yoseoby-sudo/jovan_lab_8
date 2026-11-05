from product import Product
from order_line import OrderLine

class Order:
    def __init__(self, order_id: str):
        self._order_id: str = order_id
        self._order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> str:
        return self._order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        return self._order_lines

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self._order_lines.append(order_line)

    def calculate_total(self) -> float:
        total = 0.0
        for line in self._order_lines:
            total += line.calculate_subtotal()
        return total