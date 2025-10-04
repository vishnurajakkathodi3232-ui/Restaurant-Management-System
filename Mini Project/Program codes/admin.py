
import sqlite3
from tabulate import tabulate

DB_NAME = "restaurant.db"

# ---------- Admin Authentication ----------
def admin_login():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
    admin = cursor.fetchone()

    conn.close()

    if admin:
        print("\n✅ Login successful! Welcome, Admin.")
        return True
    else:
        print("\n❌ Invalid credentials. Try again.")
        return False


# ---------- Admin Functions ----------
def add_menu_item():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    name = input("Enter item name: ")
    category = input("Enter category (e.g., Starter, Main Course, Dessert): ")
    price = float(input("Enter price: "))
    available = input("Available? (yes/no): ").lower()
    time_slot = input("Time slot (breakfast/lunch/dinner/all): ").lower()

    cursor.execute("""
        INSERT INTO Menu_table (name, category, price, available, time_slot)
        VALUES (?, ?, ?, ?, ?)
    """, (name, category, price, available, time_slot))

    conn.commit()
    conn.close()
    print("✅ Item added successfully!")


def update_menu_item():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    item_id = int(input("Enter item ID to update: "))

    print("\nWhat do you want to update?")
    print("1. Price")
    print("2. Availability")
    print("3. Category")
    print("4. Time Slot")

    choice = input("Enter choice: ")

    if choice == "1":
        new_price = float(input("Enter new price: "))
        cursor.execute("UPDATE Menu_table SET price=? WHERE item_id=?", (new_price, item_id))

    elif choice == "2":
        new_avail = input("Enter new availability (yes/no): ").lower()
        cursor.execute("UPDATE Menu_table SET available=? WHERE item_id=?", (new_avail, item_id))

    elif choice == "3":
        new_cat = input("Enter new category: ")
        cursor.execute("UPDATE Menu_table SET category=? WHERE item_id=?", (new_cat, item_id))

    elif choice == "4":
        new_slot = input("Enter new time slot (breakfast/lunch/dinner/all): ").lower()
        cursor.execute("UPDATE Menu_table SET time_slot=? WHERE item_id=?", (new_slot, item_id))

    else:
        print("❌ Invalid choice")

    conn.commit()
    conn.close()
    print("✅ Item updated successfully!")


def delete_menu_item():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    item_id = int(input("Enter item ID to delete: "))

    cursor.execute("DELETE FROM Menu_table WHERE item_id=?", (item_id,))
    conn.commit()

    if cursor.rowcount > 0:
        print("✅ Item deleted successfully!")
    else:
        print("❌ Item not found.")

    conn.close()


def view_orders():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()

    if orders:
        print("\n📋 Orders List:")
        print(tabulate(orders, headers=["ID", "Customer", "Items", "Total Price", "Date"], tablefmt="grid"))

        cursor.execute("SELECT COUNT(*), SUM(total_price) FROM orders")
        total_orders, total_amount = cursor.fetchone()
        print(f"\n🔢 Total Orders: {total_orders}")
        print(f"💰 Total Revenue: {total_amount}")
    else:
        print("No orders found.")

    conn.close()


# ---------- Admin Menu ----------
def admin_panel():
    while True:
        print("\n--- Admin Panel ---")
        print("1. Add Menu Item")
        print("2. Update Menu Item")
        print("3. Delete Menu Item")
        print("4. View Orders")
        print("5. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            add_menu_item()
        elif choice == "2":
            update_menu_item()
        elif choice == "3":
            delete_menu_item()
        elif choice == "4":
            view_orders()
        elif choice == "5":
            print("👋 Logged out.")
            break
        else:
            print("❌ Invalid choice. Try again.")

