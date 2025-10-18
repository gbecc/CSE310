from contextlib import contextmanager
from pathlib import Path
import sqlite3

# Config
database_file = Path("inventory.db") # Creates local database. Your database will be different than mine.


# DB helpers
@contextmanager
def open_connection():
    # Open a SQLite connection with foreign keys enabled. We need these keys to reference data in/from other tables.
    connection = sqlite3.connect(database_file)
    connection.execute("PRAGMA foreign_keys = ON;")
    try:
        # Commit, rollback and close allow us to only commit changes if everything succeeds, undo them if something breaks and close the connection at the end.
        yield connection
        connection.commit() 
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database():
    # Create the products table if it doesn't exist.
    create_products_table_sql = (
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name    TEXT    NOT NULL UNIQUE,
            brand_name      TEXT,
            volume_ml       INTEGER,
            stock_on_hand   INTEGER NOT NULL DEFAULT 0,
            created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
        );
        """
    )
    with open_connection() as connection:
        connection.execute(create_products_table_sql)


# Core Operations -- CRUD

def create_product(product_name: str, brand_name: str | None = None, volume_ml: int | None = None, starting_stock: int = 0) -> None:
    # int should suffice for stick and volume, and string for brand and product.
    insert_sql = (
        """
        INSERT INTO products (product_name, brand_name, volume_ml, stock_on_hand)
        VALUES (?, ?, ?, ?);
        """
    )
    with open_connection() as connection:
        connection.execute(insert_sql, (product_name, brand_name, volume_ml, int(starting_stock)))

"""
Note:

You will see that the functions in this program often contain type hints. 
It just helps to track exactly what to expect from each function, which helps a ton when writing code over the span of multiple days.

"""

def list_all_products() -> list[tuple]:
    # We have to consider cleanliness for our printed list, so COALESCE will help with returning empty values instead of null.
    select_sql = (
        """
        SELECT product_id, product_name, COALESCE(brand_name, ''), COALESCE(volume_ml, ''), stock_on_hand
        FROM products
        ORDER BY product_id;
        """
    )
    with open_connection() as connection:
        return connection.execute(select_sql).fetchall()


def read_product(product_id: int) -> tuple | None:
    select_sql = (
        """
        SELECT product_id, product_name, brand_name, volume_ml, stock_on_hand, created_at
        FROM products
        WHERE product_id = ?;
        """
    )
    with open_connection() as connection:
        return connection.execute(select_sql, (product_id,)).fetchone()


def update_product(product_id: int, *, product_name: str | None = None, brand_name: str | None = None, volume_ml: int | None = None) -> None:
    updates: list[str] = []
    parameters: list[object] = []
    if product_name is not None:   # Ignore empty values so we don't overwrite existing values with empty values (since it usually indicates you don't want chance).
        updates.append("product_name = ?"); parameters.append(product_name)
    if brand_name is not None:
        updates.append("brand_name = ?"); parameters.append(brand_name)
    if volume_ml is not None:
        updates.append("volume_ml = ?"); parameters.append(volume_ml)

    if not updates:
        return  # nothing to change

    update_sql = f"UPDATE products SET {', '.join(updates)} WHERE product_id = ?;"
    parameters.append(product_id)

    with open_connection() as connection:
        connection.execute(update_sql, parameters)


def delete_product(product_id: int) -> None:
    delete_sql = "DELETE FROM products WHERE product_id = ?;"
    with open_connection() as connection:
        connection.execute(delete_sql, (product_id,))


# Adjusting Stock / Inventory

def increase_stock(product_id: int, quantity: int) -> None:
    """Add to stock_on_hand (simulating restock)."""
    quantity = int(quantity)
    if quantity <= 0:
        print("Quantity must be positive.")
        return
    update_sql = "UPDATE products SET stock_on_hand = stock_on_hand + ? WHERE product_id = ?;"
    with open_connection() as connection:
        connection.execute(update_sql, (quantity, product_id))


def decrease_stock(product_id: int, quantity: int) -> None:
    """Subtract from stock_on_hand (simulating sale/use). Prevent going below zero."""
    quantity = int(quantity)
    if quantity <= 0:
        print("Quantity must be positive.")
        return

    # Check current level to avoid negative stock
    current = read_product(product_id)
    if not current:
        print("Product not found.")
        return
    current_stock = int(current[4])
    if quantity > current_stock:
        print(f"Cannot remove {quantity}. Only {current_stock} in stock.")
        return

    update_sql = "UPDATE products SET stock_on_hand = stock_on_hand - ? WHERE product_id = ?;"
    with open_connection() as connection:
        connection.execute(update_sql, (quantity, product_id))

# Stretch Challenge, aggregate functions. Easy SQL query that allows us to retrieve values available to provide an overview of the stock.

def show_stock_summary() -> None:
    """Summarize inventory using aggregate functions."""
    sql = """
    SELECT
        COUNT(*)                              AS product_count,
        COALESCE(SUM(stock_on_hand), 0)       AS total_units,
        COALESCE(AVG(stock_on_hand), 0.0)     AS avg_units_per_product,
        COALESCE(MIN(stock_on_hand), 0)       AS min_units,
        COALESCE(MAX(stock_on_hand), 0)       AS max_units
    FROM products;
    """
    with open_connection() as connection:
        row = connection.execute(sql).fetchone()
    print("\nInventory summary")
    print("-----------------")
    print(f"Products:            {row[0]}")
    print(f"Total units:         {row[1]}")
    print(f"Avg units/product:   {row[2]:.2f}")
    print(f"Min units in a SKU:  {row[3]}")
    print(f"Max units in a SKU:  {row[4]}")

# CLI Helpers to Organize Things!

def print_menu() -> None:
    print("\n Beverage Inventory; pick an option:")
    print(" 1) Add a new product")
    print(" 2) List all products")
    print(" 3) Edit a product (name/brand/size)")
    print(" 4) Remove a product")
    print(" 5) Increase stock (restock)")
    print(" 6) Decrease stock (sale/use)")
    print(" 7) View one product")
    print(" 8) Inventory summary (aggregates)")
    print(" 0) Exit")

def prompt_int(prompt_text: str) -> int:
    while True:
        raw = input(prompt_text).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a whole number.") # Whole numbers is standard practice for volume in ml & also for quantities.


def main() -> None:
    initialize_database()
    while True:
        print_menu()
        user_choice = input("> ").strip()

        if user_choice == "1":
            product_name = input("Product name: ").strip()
            brand_name = input("Brand (optional): ").strip() or None #  If we handle only one brand's products, it'd be a waste of resources, but I wanted the flexibility.
            volume_text = input("Volume in ml (optional): ").strip()
            volume_ml = int(volume_text) if volume_text else None
            starting_text = input("Starting stock (default 0): ").strip()
            starting_stock = int(starting_text) if starting_text else 0
            try:
                create_product(product_name, brand_name, volume_ml, starting_stock)
                print("Product added.")
            except sqlite3.IntegrityError as err:
                print(f"Couldn't add product: {err}")

        elif user_choice == "2":
            products = list_all_products()
            if not products:
                print("(no products yet)")
            else:
                print("ID | Name | Brand | Volume(ml) | Stock")
                for product in products:
                    print(f"{product[0]:>2} | {product[1]} | {product[2]} | {product[3]} | {product[4]}")

        elif user_choice == "3":
            product_id_input = prompt_int("Product ID to edit: ")
            new_name = input("New name (leave blank to keep): ").strip()
            new_brand = input("New brand (leave blank to keep): ").strip()
            new_volume = input("New volume ml (leave blank to keep): ").strip()
            updates: dict = {}
            if new_name:
                updates["product_name"] = new_name
            if new_brand:
                updates["brand_name"] = new_brand
            if new_volume:
                try:
                    updates["volume_ml"] = int(new_volume)
                except ValueError:
                    print("Volume must be a number; ignoring volume change.")
            update_product(product_id_input, **updates)
            print("Product updated.")

        elif user_choice == "4":
            product_id_input = prompt_int("Product ID to remove: ")
            confirmation = input("Type 'delete' to confirm: ").strip().lower()
            if confirmation == "delete":
                delete_product(product_id_input)
                print("Product deleted.")
            else:
                print("Deletion cancelled.")

        elif user_choice == "5":
            product_id_input = prompt_int("Product ID: ")
            quantity = prompt_int("Quantity to add: ")
            increase_stock(product_id_input, quantity)
            print("Stock increased.")

        elif user_choice == "6":
            product_id_input = prompt_int("Product ID: ")
            quantity = prompt_int("Quantity to remove: ")
            decrease_stock(product_id_input, quantity)
            print("Stock decreased.")

        elif user_choice == "7":
            product_id_input = prompt_int("Product ID to view: ")
            product = read_product(product_id_input)
            if product:
                print(
                    f"ID: {product[0]}\n"
                    f"Name: {product[1]}\n"
                    f"Brand: {product[2]}\n"
                    f"Volume (ml): {product[3]}\n"
                    f"Stock: {product[4]}\n"
                    f"Created: {product[5]}"
                )
            else:
                print("Not found.")

        elif user_choice == "8":
            show_stock_summary()

        elif user_choice == "0":
            print("Goodbye!")
            break

        else:
            print("Unknown option. Please choose 0-8.")


if __name__ == "__main__":
    main()
