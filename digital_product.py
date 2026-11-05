from product import Product

# Represents a digital product that has a download size
class DigitalProduct(Product):

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self._download_size = download_size

    @property
    def download_size(self):
        return self._download_size

    def display_information(self):
        # Overrides parent display_information to include digital attributes
        super().display_information()
        print(f"Size: {self._download_size}MB | Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self):
        return "Delivered instantly via download link."

    def to_dict(self):
        return {
            "type": "digital",
            "id": self._product_id,
            "name": self._name,
            "price": self._price,
            "stock": self._stock,
            "download_size": self._download_size
        }

