import math
from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from shipping import CanBeShipped
from supplier import Supplier
from order import Order


def select_supplier(inventory: Inventory) -> Supplier | None:
    if not inventory.suppliers:
        print("No suppliers available. Please add a supplier first.")
        return None

    print("\nAvailable Suppliers")

    for supplier in inventory.suppliers:
        print(supplier.display_information())

    while True:
        supplier_id = input("Enter Supplier ID: ").strip()

        supplier = inventory.search_supplier(supplier_id)

        if supplier:
            return supplier

        print("Supplier not found. Please try again.")


# Handles user input and validation for adding a physical or digital product.
def handle_add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")

    # 1. Select product type
    while True:
        product_type = input(
            "Enter product type (physical/digital): "
        ).strip().lower()

        if product_type in ["physical", "digital"]:
            break

        print("Invalid product type. Please enter physical or digital.")

    # 2. Enter product ID
    while True:
        try:
            product_id = int(input("Product ID: "))

            if product_id <= 0:
                print("Product ID must be a positive integer.")
                continue

            if inventory.search_product(product_id):
                print("Product ID already exists.")
                continue

            break

        except ValueError:
            print("Please enter a valid numeric product ID.")

    # 3. Enter product name
    while True:
        product_name = input("Product Name: ").strip()

        if product_name:
            break

        print("Product name cannot be empty.")

    # 4. Enter product price
    while True:
        try:
            price = float(input("Price: $"))

            if not math.isfinite(price) or price < 0:
                print("Price must be a valid non-negative number.")
                continue

            break

        except ValueError:
            print("Please enter a valid price.")

    # 5. Enter product stock
    while True:
        try:
            stock = int(input("Stock Quantity: "))

            if stock < 0:
                print("Stock cannot be negative.")
                continue

            break

        except ValueError:
            print("Please enter a valid stock quantity.")

    # 6. Select an existing supplier
    supplier = select_supplier(inventory)

    if supplier is None:
        print("Product creation cancelled.")
        return

    # 7. Create the product based on its type
    try:
        if product_type == "physical":

            while True:
                try:
                    weight = float(input("Product Weight (kg): "))

                    if not math.isfinite(weight) or weight <= 0:
                        print("Weight must be a valid positive number.")
                        continue

                    break

                except ValueError:
                    print("Please enter a valid weight.")

            new_product = PhysicalProduct(
                product_id,
                product_name,
                price,
                stock,
                weight,
                supplier
            )

        else:

            while True:
                try:
                    download_size = float(
                        input("Download Size (MB): ")
                    )

                    if not math.isfinite(download_size) or download_size <= 0:
                        print("Download size must be a valid positive number.")
                        continue

                    break

                except ValueError:
                    print("Please enter a valid download size.")

            new_product = DigitalProduct(
                product_id,
                product_name,
                price,
                stock,
                download_size,
                supplier
            )

        # 8. Add product and record transaction
        inventory.add_product(new_product)
        inventory.add_transaction(product_id, stock)

        print("\nProduct added successfully!")
        print(f"Assigned Supplier: {supplier.name}")

    except (ValueError, TypeError) as error:
        print(f"Product could not be added: {error}")


# Handles user input and logic for updating product stock.
def handle_update_stock(inventory: Inventory) -> None:
    product_id_input = input("Product ID: ")

    try:
        product_id = int(product_id_input)
    except ValueError:
        print("Product ID must be a number.")
        return

    product = inventory.search_product(product_id)

    if product:
        quantity_input = input("Stock Quantity to Add: ")

        try:
            quantity = int(quantity_input)
        except ValueError:
            print("Stock quantity must be a number.")
            return

        if quantity < 0:
            print("Stock quantity cannot be negative.")
            return

        try:
            product.update_stock(quantity)
            inventory.add_transaction(product_id, quantity)

            print("Stock updated successfully!")

        except (ValueError, TypeError) as error:
            print(f"Stock update failed: {error}")

    else:
        print("Product not found.")


# Handles searching for a product by ID and displaying its details.
def handle_search_product(inventory: Inventory) -> None:
    while True:
        product_id_input = input("Product ID to Search: ")

        try:
            product_id = int(product_id_input)
        except ValueError:
            print("Product ID must be a number.")
            continue

        product = inventory.search_product(product_id)

        if product:
            print("\nProduct Found")
            product.display_information()

            if isinstance(product, CanBeShipped):
                print(
                    f"  -> Shipping Cost: "
                    f"${product.calculate_shipping_cost():.2f}"
                )

            break

        print("Product not found.")


# Handles adding a new supplier.
def handle_add_supplier(inventory: Inventory) -> None:
    print("\nAdd New Supplier")

    while True:
        supplier_id = input("Supplier ID: ").strip()

        if not supplier_id:
            print("Supplier ID cannot be empty.")
            continue

        if inventory.search_supplier(supplier_id):
            print("Supplier ID already exists.")
            continue

        break

    while True:
        name = input("Supplier Name: ").strip()

        if not name:
            print("Supplier name cannot be empty.")
            continue

        break

    while True:
        email = input("Contact Email: ").strip()

        if not email:
            print("Email cannot be empty.")
            continue

        if "@" not in email:
            print("Please enter a valid email.")
            continue

        break

    try:
        new_supplier = Supplier(supplier_id, name, email)
        inventory.add_supplier(new_supplier)

        try:
            inventory.save_to_file()
            print("Supplier added successfully!")

        except OSError as error:
            print(f"Supplier added, but saving failed: {error}")

    except (ValueError, TypeError) as error:
        print(f"Supplier could not be added: {error}")


# Handles creating a new order.
def handle_create_order(
    inventory: Inventory,
    orders: list[Order]
) -> None:

    if not inventory.products:
        print("\nInventory is empty. Add products before creating an order.")
        return

    # Validate order ID.
    while True:
        order_id = input("Enter Order ID: ").strip()

        try:
            new_order = Order(order_id)
            break

        except ValueError as error:
            print(error)

    # Track quantities already added for each product.
    ordered_quantities: dict[int, int] = {}

    while True:
        inventory.display_all()

        pid_input = input(
            "Enter Product ID to add to order (or type 'done' to finish): "
        ).strip()

        if pid_input.lower() == "done":
            break

        try:
            pid = int(pid_input)
        except ValueError:
            print("Please enter a valid product ID.")
            continue

        product = inventory.search_product(pid)

        if not product:
            print("Product ID not found.")
            continue

        try:
            qty = int(input(f"Enter quantity for {product.name}: "))
        except ValueError:
            print("Please enter a valid quantity.")
            continue

        if qty <= 0:
            print("Quantity must be greater than zero.")
            continue

        # Check the combined quantity for repeated product entries.
        current_quantity = ordered_quantities.get(pid, 0)

        if current_quantity + qty > product.stock:
            available = product.stock - current_quantity
            print(
                f"Insufficient stock. Only {available} more "
                f"unit(s) can be added to this order."
            )
            continue

        try:
            # Order internally creates the OrderLine (Composition).
            new_order.add_order_line(product, qty)

            ordered_quantities[pid] = current_quantity + qty

            print(f"Added {qty}x {product.name} to order.")

        except (ValueError, TypeError) as error:
            print(f"Could not add product to order: {error}")

    # Do not save an empty order.
    if not new_order.order_lines:
        print("No products were added. Order creation cancelled.")
        return

    # Deduct stock after the order is completed.
    try:
        for product_id, quantity in ordered_quantities.items():
            product = inventory.search_product(product_id)

            if product is None:
                raise ValueError(
                    f"Product {product_id} could not be found."
                )

            product.update_stock(-quantity)

            # Record stock deduction in transaction history.
            inventory.add_transaction(product_id, -quantity)

        # Save updated inventory so deductions persist.
        inventory.save_to_file()

    except (ValueError, TypeError, OSError) as error:
        print(f"Order could not be completed: {error}")
        return

    orders.append(new_order)

    print(
        f"Order {order_id} created successfully! "
        f"Total: ${new_order.calculate_total():.2f}"
    )


# Main application.
def main() -> None:
    inventory = Inventory()

    try:
        inventory.load_from_file()

    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Could not load inventory: {error}")
        print("Starting with an empty inventory.")
        inventory = Inventory()

    orders: list[Order] = []

    print("\n========================================================")
    print("        INVENTORY & ORDER MANAGEMENT SYSTEM (LAB 8)")
    print("========================================================")

    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product (Physical/Digital)")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Add New Supplier")
        print("6. Create New Order")
        print("7. View All Orders")
        print("8. Save Inventory")
        print("9. Exit")
        print("----------------------------")

        option = input("Enter option: ").strip()

        if option == "1":
            inventory.display_all()

        elif option == "2":
            handle_add_product(inventory)

        elif option == "3":
            handle_update_stock(inventory)

        elif option == "4":
            handle_search_product(inventory)

        elif option == "5":
            handle_add_supplier(inventory)

        elif option == "6":
            handle_create_order(inventory, orders)

        elif option == "7":
            if not orders:
                print("No orders recorded.")

            else:
                for order in orders:
                    print(f"\nOrder ID: {order.order_id}")

                    for line in order.order_lines:
                        print(
                            f"  - {line.product.name} x {line.quantity} "
                            f"= ${line.calculate_subtotal():.2f}"
                        )

                    print(f"  Total: ${order.calculate_total():.2f}")

        elif option == "8":
            try:
                inventory.save_to_file()

            except OSError as error:
                print(f"Could not save inventory: {error}")

        elif option == "9":
            print("Exiting System.")
            break

        else:
            print("Invalid option. Please choose 1-9.")


if __name__ == "__main__":
    main()