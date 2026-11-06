import math
from product import Product
from supplier import Supplier


class DigitalProduct(Product):

    def __init__(
        self,
        product_id: int,
        name: str,
        price: float,
        stock: int,
        download_size: float,
        supplier: Supplier
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)

        if not isinstance(download_size, (int, float)) or isinstance(download_size, bool) or not math.isfinite(download_size) or download_size <= 0:
            raise ValueError("Download size must be a valid positive number.")

        self._download_size = download_size

    @property
    def download_size(self) -> float:
        return self._download_size

    def get_fulfilment_info(self) -> str:
        return f"Digital item. Download size: {self._download_size}MB."

    def display_information(self) -> None:
        print(
            f"Product ID: {self._product_id} | "
            f"Name: {self._name} | "
            f"Price: ${self._price:.2f} | "
            f"Stock: {self._stock} | "
            f"Download Size: {self._download_size}MB"
        )

        print(
            f"  -> Supplier: "
            f"{self._supplier.name} "
            f"({self._supplier.contact_email})"
        )

    def to_dict(self) -> dict:
        return {
            "type": "digital",
            "id": self._product_id,
            "name": self._name,
            "price": self._price,
            "stock": self._stock,
            "download_size": self._download_size,
            "supplier_id": self._supplier.supplier_id
        }
