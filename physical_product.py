from product import Product
from shipping import CanBeShipped

# Represents a physical product that has weight and requires shipping
class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self._weight = weight

    @property
    def weight(self):
        return self._weight

    def display_information(self):
        # Overrides parent display_information to include physical attributes
        super().display_information()
        print(f"Weight: {self._weight}kg | Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self):
        return "Requires physical shipping and warehousing."

    def calculate_shipping_cost(self):
        # Example rule: $5 base fee + $2 per kg
        return 5.00 + (self._weight * 2.00)

    def to_dict(self):
        return {
            "type": "physical",
            "id": self._product_id,
            "name": self._name,
            "price": self._price,
            "stock": self._stock,
            "weight": self._weight
        }