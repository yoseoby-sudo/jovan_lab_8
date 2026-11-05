from abc import ABC, abstractmethod

# Abstract base class representing a generic product
class Product(ABC):

    def __init__(self, product_id, name, price, stock):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock = stock

    @property
    def product_id(self):
        return self._product_id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def stock(self):
        return self._stock

    def update_stock(self, quantity):
        # Updates the stock quantity securely through a method
        self._stock += quantity

    def display_information(self):
        # Displays formatted common product information
        print(
            f"ID: {self._product_id} | "
            f"Name: {self._name} | "
            f"Price: ${self._price:.2f} | "
            f"Stock: {self._stock}",
            end=" | "
        )

    @abstractmethod
    def get_fulfilment_info(self):
        # Abstract method to define fulfilment details
        pass

    @abstractmethod
    def to_dict(self):
        # Abstract method to convert product to dictionary for JSON persistence
        pass