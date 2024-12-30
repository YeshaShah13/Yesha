import sqlite3

class GroceryItem:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

class GroceryStore:
    def __init__(self, db_name="grocery_store.db"):
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL
                )
            """)
            conn.commit()

    def add_item(self, item):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)",
                           (item.name, item.quantity, item.price))
            conn.commit()
        print(f"Item '{item.name}' added to the store.")

    def remove_item(self, item_name):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM items WHERE name = ?", (item_name,))
            if cursor.rowcount > 0:
                print(f"'{item_name}' removed from the store.")
            else:
                print(f"'{item_name}' not found in the store.")
            conn.commit()

    def update_quantity(self, item_name, new_quantity):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE items SET quantity = ? WHERE name = ?",
                           (new_quantity, item_name))
            if cursor.rowcount > 0:
                print(f"Quantity of '{item_name}' updated to {new_quantity}.")
            else:
                print(f"'{item_name}' not found in the store.")
            conn.commit()

    def display_items(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, quantity, price FROM items")
            rows = cursor.fetchall()
            if rows:
                print("Grocery Items:")
                for row in rows:
                    print(f"{row[0]}: {row[1]} x ${row[2]:.2f}")
            else:
                print("No items in the store.")

    def calculate_total_cost(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(quantity * price) FROM items")
            total_cost = cursor.fetchone()[0]
            return total_cost if total_cost else 0.0

def main():
    store = GroceryStore()

    while True:
        print("\nGrocery Management System")
        print("1. Add Item")
        print("2. Remove Item")
        print("3. Update Quantity")
        print("4. Display Items")
        print("5. Calculate Total Cost")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter item name: ")
            quantity = int(input("Enter item quantity: "))
            price = float(input("Enter item price: "))
            item = GroceryItem(name, quantity, price)
            store.add_item(item)
        elif choice == "2":
            item_name = input("Enter item name to remove: ")
            store.remove_item(item_name)
        elif choice == "3":
            item_name = input("Enter item name to update: ")
            new_quantity = int(input("Enter new quantity: "))
            store.update_quantity(item_name, new_quantity)
        elif choice == "4":
            store.display_items()
        elif choice == "5":
            total_cost = store.calculate_total_cost()
            print(f"Total cost: ${total_cost:.2f}")
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()