
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

            if price < 0:
                print("Price cannot be negative.")
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
    if product_type == "physical":

        while True:
            try:
                weight = float(input("Product Weight (kg): "))

                if weight <= 0:
                    print("Weight must be greater than 0.")
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

                if download_size <= 0:
                    print("Download size must be greater than 0.")
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

        product.update_stock(quantity)
        inventory.add_transaction(product_id, quantity)

        print("Stock updated successfully!")

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


def handle_add_supplier(inventory: Inventory) -> None:
    print("\nAdd New Supplier")

    while True:
        supplier_id = input("Supplier ID: ").strip()

        if supplier_id == "":
            print("Supplier ID cannot be empty.")
            continue

        if inventory.search_supplier(supplier_id):
            print("Supplier ID already exists.")
            continue

        break

    while True:
        name = input("Supplier Name: ").strip()

        if name == "":
            print("Supplier name cannot be empty.")
            continue

        break

    while True:
        email = input("Contact Email: ").strip()

        if email == "":
            print("Email cannot be empty.")
            continue

        if "@" not in email:
            print("Please enter a valid email.")
            continue

        break

    new_supplier = Supplier(supplier_id, name, email)

    inventory.add_supplier(new_supplier)
    inventory.save_to_file()

    print("Supplier added successfully!")


def handle_create_order(
    inventory: Inventory,
    orders: list[Order]
) -> None:

    if not inventory.products:
        print("\nInventory is empty. Add products before creating an order.")
        return

    order_id = input("Enter Order ID: ").strip()
    new_order = Order(order_id)

    while True:
        inventory.display_all()

        pid_input = input(
            "Enter Product ID to add to order (or type 'done' to finish): "
        ).strip()

        if pid_input.lower() == "done":
            break

        try:
            pid = int(pid_input)
            product = inventory.search_product(pid)

            if not product:
                print("Product ID not found.")
                continue

            qty = int(input(f"Enter quantity for {product.name}: "))

            if qty <= 0:
                print("Quantity must be greater than zero.")
                continue

            # Order internally creates the OrderLine (Composition).
            new_order.add_order_line(product, qty)

            print(f"Added {qty}x {product.name} to order.")

        except ValueError:
            print("Invalid input.")

    orders.append(new_order)

    print(
        f"Order {order_id} created successfully! "
        f"Total: ${new_order.calculate_total():.2f}"
    )


def main() -> None:
    inventory = Inventory()
    inventory.load_from_file()

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
            inventory.save_to_file()

        elif option == "9":
            print("Exiting System.")
            break

        else:
            print("Invalid option. Please choose 1-9.")


if __name__ == "__main__":
    main()
