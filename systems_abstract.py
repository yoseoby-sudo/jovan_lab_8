from inventory import Inventory
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from shipping import CanBeShipped

# Handles user input and validation for adding a physical or digital product
def handle_add_product(inventory):
    print("\nAdd New Product")
    
    while True:
        prod_type = input("Product Type (1: Physical, 2: Digital): ").strip()
        if prod_type in ["1", "2"]:
            break
        print("Invalid choice. Please enter 1 for Physical or 2 for Digital.")

    while True:
        product_id_input = input("Product ID: ").strip()
        try:
            product_id = int(product_id_input)
        except ValueError:
            print("Product ID must be a number.")
            continue

        if inventory.search_product(product_id) is not None:
            print("Product ID already exists.")
            continue
        break

    while True:
        product_name = input("Product Name: ").strip()
        if product_name == "":
            print("Product name cannot be empty.")
            continue
        break

    while True:
        price_input = input("Price: ")
        try:
            price = float(price_input)
        except ValueError:
            print("Price must be a number.")
            continue
        if price < 0:
            print("Price cannot be negative.")
            continue
        break

    while True:
        stock_input = input("Stock Quantity: ")
        try:
            stock = int(stock_input)
        except ValueError:
            print("Stock quantity must be a number.")
            continue
        if stock < 0:
            print("Stock quantity cannot be negative.")
            continue
        break

    if prod_type == "1":
        while True:
            weight_input = input("Weight (kg): ")
            try:
                weight = float(weight_input)
            except ValueError:
                print("Weight must be a number.")
                continue
            if weight < 0:
                print("Weight cannot be negative.")
                continue
            break
        new_product = PhysicalProduct(product_id, product_name, price, stock, weight)
    else:
        while True:
            size_input = input("Download Size (MB): ")
            try:
                download_size = float(size_input)
            except ValueError:
                print("Download size must be a number.")
                continue
            if download_size < 0:
                print("Download size cannot be negative.")
                continue
            break
        new_product = DigitalProduct(product_id, product_name, price, stock, download_size)

    inventory.add_product(new_product)
    inventory.add_transaction(product_id, stock)
    print("Product added successfully!")


# Handles user input and logic for updating product stock
def handle_update_stock(inventory):
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


# Handles searching for a product by ID and displaying its details
def handle_search_product(inventory):
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
                print(f"  -> Shipping Cost: ${product.calculate_shipping_cost():.2f}")
            break

        print("Product not found.")


# Main application loop and menu controller
def main():
    inventory = Inventory()
    inventory.load_from_file()

    print("\n========================================================")
    print("        INVENTORY MANAGEMENT SYSTEM (LAB 7)")
    print("========================================================")

    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product (Physical/Digital)")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")

        option = input("Enter option: ")

        if option == "1":
            inventory.display_all()
        elif option == "2":
            handle_add_product(inventory)
        elif option == "3":
            handle_update_stock(inventory)
        elif option == "4":
            handle_search_product(inventory)
        elif option == "5":
            inventory.save_to_file()
        elif option == "6":
            print("Exiting Inventory Management System.")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()