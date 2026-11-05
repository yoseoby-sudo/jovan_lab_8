import os
import json
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from shipping import CanBeShipped

# Responsible for managing a collection of products, transactions, and file persistence
class Inventory:

    def __init__(self):
        self._products = []
        self._transaction_history = []

    def add_product(self, product):
        # Adds a Product object to the inventory list
        self._products.append(product)

    def search_product(self, product_id):
        # Searches for and returns a Product object by its ID, or None if not found
        for product in self._products:
            if product.product_id == product_id:
                return product
        return None

    def display_all(self):
        # Displays all products currently in the inventory
        print("\nCurrent Inventory")
        print("-" * 80)
        if not self._products:
            print("No products in inventory.")
        else:
            for product in self._products:
                product.display_information()
                # If the product can be shipped, show its shipping cost
                if isinstance(product, CanBeShipped):
                    print(f"  -> Shipping Cost: ${product.calculate_shipping_cost():.2f}")
        print("-" * 80)

    def add_transaction(self, product_id, amount):
        # Records a transaction entry
        self._transaction_history.append({
            "product_id": product_id,
            "amount": amount
        })

    def load_from_file(self, filename="inventory.json"):
        # Loads inventory data and transaction history from JSON file supporting subclasses
        if os.path.exists(filename):
            print(f"{filename} found.")
            with open(filename, "r") as file:
                data = json.load(file)
            print("Inventory loaded successfully.")

            raw_inventory = data.get("inventory", [])
            self._transaction_history = data.get("transaction_history", [])

            self._products = []
            for item in raw_inventory:
                prod_type = item.get("type")
                if prod_type == "physical":
                    product = PhysicalProduct(
                        item["id"],
                        item["name"],
                        item["price"],
                        item["stock"],
                        item["weight"]
                    )
                elif prod_type == "digital":
                    product = DigitalProduct(
                        item["id"],
                        item["name"],
                        item["price"],
                        item["stock"],
                        item["download_size"]
                    )
                else:
                    continue
                self._products.append(product)
        else:
            print(f"{filename} not found. Starting with empty inventory.")
            self._products = []
            self._transaction_history = []

    def save_to_file(self, filename="inventory.json"):
        # Saves current inventory and transaction history to JSON file
        raw_inventory = [product.to_dict() for product in self._products]
        data = {
            "inventory": raw_inventory,
            "transaction_history": self._transaction_history
        }
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print("Inventory saved successfully!")
