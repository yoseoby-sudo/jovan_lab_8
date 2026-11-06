import math
from product import Product
from shipping import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):

    def __init__(
        self,
        product_id: int,
        name: str,
        price: float,
        stock: int,
        weight: float,
        supplier: Supplier
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)

        if not isinstance(weight, (int, float)) or isinstance(weight, bool) or not math.isfinite(weight) or weight <= 0:
            raise ValueError("Weight must be a valid positive number.")

        self._weight = weight

    @property
    def weight(self) -> float:
        return self._weight

    def calculate_shipping_cost(self) -> float:
        return self._weight * 5.0

    def get_fulfilment_info(self) -> str:
        return f"Physical item. Shipping weight: {self._weight}kg."

    def display_information(self) -> None:
        print(
            f"Product ID: {self._product_id} | "
            f"Name: {self._name} | "
            f"Price: ${self._price:.2f} | "
            f"Stock: {self._stock} | "
            f"Weight: {self._weight}kg"
        )

        print(
            f"  -> Supplier: "
            f"{self._supplier.name} "
            f"({self._supplier.contact_email})"
        )

    def to_dict(self) -> dict:
        return {
            "type": "physical",
            "id": self._product_id,
            "name": self._name,
            "price": self._price,
            "stock": self._stock,
            "weight": self._weight,
            "supplier_id": self._supplier.supplier_id
        }
