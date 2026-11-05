from product import Product
from supplier import Supplier

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size, supplier):
        super().__init__(product_id, name, price, stock, supplier)
        self._download_size = download_size

    @property
    def download_size(self) -> float:
        return self._download_size

    def get_fulfilment_info(self) -> str:
        return f"Digital item. Download size: {self._download_size}MB."

    def display_information(self) -> None:
        print(f"Product ID: {self._product_id} | Name: {self._name} | Price: ${self._price:.2f} | Stock: {self._stock} | Download Size: {self._download_size}MB")
        print(f"  -> Supplier: {self._supplier.name} ({self._supplier.contact_email})")

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