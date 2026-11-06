import os
import json
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from shipping import CanBeShipped
from supplier import Supplier


# Responsible for managing products, suppliers,
# transactions, and file persistence.
class Inventory:

    def __init__(self) -> None:
        self._products: list[Product] = []
        self._transaction_history: list[dict[str, int]] = []
        self._suppliers: list[Supplier] = []

    def add_product(self, product: Product) -> None:
        """Adds a Product object to the inventory."""

        if not isinstance(product, Product):
            raise TypeError("Product must be a Product object.")

        if self.find_product(product.product_id) is not None:
            raise ValueError("A product with this ID already exists.")

        self._products.append(product)

    def find_product(self, product_id: int) -> Product | None:
        """Finds and returns a product by its ID."""
        for product in self._products:
            if product.product_id == product_id:
                return product

        return None

    def search_product(self, product_id: int) -> Product | None:
        """Compatibility method for existing code."""
        return self.find_product(product_id)

    def remove_product(self, product_id: int) -> bool:
        """Removes a product from inventory using its ID."""
        product = self.find_product(product_id)

        if product is not None:
            self._products.remove(product)
            return True

        return False

    def display_all(self) -> None:
        """Displays all products currently in inventory."""
        print("\nCurrent Inventory")
        print("-" * 80)

        if not self._products:
            print("No products in inventory.")

        else:
            for product in self._products:
                # Polymorphism: each subclass displays its own information.
                product.display_information()

                # Polymorphism: each subclass provides its own fulfilment info.
                print(f"  -> Fulfilment: {product.get_fulfilment_info()}")

                # Show shipping cost if the product supports shipping.
                if isinstance(product, CanBeShipped):
                    print(
                        f"  -> Shipping Cost: "
                        f"${product.calculate_shipping_cost():.2f}"
                    )

        print("-" * 80)

    def add_transaction(self, product_id: int, amount: int) -> None:
        """Records a transaction entry."""
        self._transaction_history.append({
            "product_id": product_id,
            "amount": amount
        })

    def add_supplier(self, supplier: Supplier) -> None:
        """Adds a Supplier object to the supplier collection."""

        if not isinstance(supplier, Supplier):
            raise TypeError("Supplier must be a Supplier object.")

        if self.find_supplier(supplier.supplier_id) is not None:
            raise ValueError("A supplier with this ID already exists.")

        self._suppliers.append(supplier)

    def find_supplier(self, supplier_id: str) -> Supplier | None:
        """Finds and returns a supplier using its ID."""
        for supplier in self._suppliers:
            if supplier.supplier_id == supplier_id:
                return supplier

        return None

    def search_supplier(self, supplier_id: str) -> Supplier | None:
        """Compatibility method for existing code."""
        return self.find_supplier(supplier_id)

    @property
    def suppliers(self) -> list[Supplier]:
        return self._suppliers.copy()

    @property
    def products(self) -> list[Product]:
        return self._products.copy()

    def load_from_file(self, filename: str = "inventory.json") -> None:
        """Loads suppliers, products, and transactions from JSON."""

        if not os.path.exists(filename):
            print(
                f"{filename} not found. "
                "Starting with empty inventory."
            )

            self._products = []
            self._suppliers = []
            self._transaction_history = []
            return

        print(f"{filename} found.")

        try:
            with open(filename, "r") as file:
                data = json.load(file)

        except json.JSONDecodeError as error:
            raise ValueError(
                f"Invalid JSON format in {filename}."
            ) from error
        
        if not isinstance(data, dict):
            raise ValueError("Inventory file must contain a JSON object.")

        for key in ("inventory", "suppliers", "transaction_history"):
            if not isinstance(data.get(key, []), list):
                raise ValueError(f"'{key}' must contain a list.")
        
        # Load transaction history.
        self._transaction_history = data.get(
            "transaction_history", []
        )

        # Load suppliers first so products can reference them.
        self._suppliers = []

        for item in data.get("suppliers", []):
            if not isinstance(item, dict):
                raise ValueError("Each supplier record must be a JSON object.")

            supplier = Supplier(
                item["supplier_id"],
                item["name"],
                item["contact_email"]
            )

            self.add_supplier(supplier)

        # Load products and connect each product to its supplier.
        self._products = []

        for item in data.get("inventory", []):
            if not isinstance(item, dict):
                raise ValueError("Each product record must be a JSON object.")

            supplier_id = item.get("supplier_id")

            if supplier_id is None:
                raise ValueError(
                    f"Product {item.get('id', 'Unknown')} is missing supplier_id "
                    "in inventory.json."
                )

            supplier = self.find_supplier(supplier_id)

            if supplier is None:
                raise ValueError(
                    f"Supplier {supplier_id} was not found "
                    f"for product {item['id']}."
                )

            product_type = item.get("type")

            if product_type == "physical":
                product = PhysicalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item["weight"],
                    supplier
                )

            elif product_type == "digital":
                product = DigitalProduct(
                    item["id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                    item["download_size"],
                    supplier
                )

            else:
                raise ValueError(
                    f"Unknown product type '{product_type}' "
                    f"for product {item['id']}."
                )

            self.add_product(product)

        print("Inventory loaded successfully.")

    def save_to_file(self, filename: str = "inventory.json") -> None:
        """Saves suppliers, products, and transactions to JSON."""

        # Convert suppliers into dictionaries.
        raw_suppliers = [
            {
                "supplier_id": supplier.supplier_id,
                "name": supplier.name,
                "contact_email": supplier.contact_email
            }
            for supplier in self._suppliers
        ]

        # Convert products into dictionaries.
        raw_inventory = [
            product.to_dict()
            for product in self._products
        ]

        data = {
            "inventory": raw_inventory,
            "suppliers": raw_suppliers,
            "transaction_history": self._transaction_history
        }

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print("Inventory saved successfully!")
