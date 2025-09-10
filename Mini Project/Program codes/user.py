import sqlite3
from tabulate import tabulate
from datetime import datetime

DB_NAME = "restaurant.db"


# Function to show full menu (all items)
def show_menu():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("\n--- MENU ---")

    cursor.execute("""
        SELECT item_id, name, category, price, time_slot 
        FROM Menu_table 
        WHERE available='yes'
        ORDER BY category
    """)

    rows = cursor.fetchall()
    if rows:
        print(tabulate(rows, headers=["ID", "Name", "Category", "Price", "Time Slot"], tablefmt="fancy_grid"))
    else:
        print("No items available right now.")

    conn.close()
    return rows  


# Function to place an order
def place_order():
    items = show_menu()
    if not items:
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    customer_name = input("\nEnter your name: ").strip()
    order_items = []
    total_price = 0.0

    while True:
        try:
            item_id = input("\nEnter item ID to order (or 'done' to finish): ")
            if item_id.lower() == "done":
                break

            cursor.execute("SELECT name, price FROM Menu_table WHERE item_id=? AND available='yes'", (item_id,))
            item = cursor.fetchone()

            if item:
                qty = int(input(f"Enter quantity for {item[0]}: "))
                order_items.append(f"{item[0]} x{qty}")
                total_price += item[1] * qty
            else:
                print("❌ Invalid item ID or not available.")
        except ValueError:
            print("⚠ Invalid input, try again.")

    if not order_items:
        print("No items selected. Order cancelled.")
        return

    order_summary = ", ".join(order_items)
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO orders (customer_name, items, total_price, order_date)
        VALUES (?, ?, ?, ?)
    """, (customer_name, order_summary, total_price, order_date))

    conn.commit()
    conn.close()

    print("\n✅ Order placed successfully!")
    print("------- ORDER SUMMARY -------")
    print(f"Customer: {customer_name}")
    print(f"Items: {order_summary}")
    print(f"Total Price: ₹{total_price:.2f}")
    print(f"Date: {order_date}")
    print("----------------------------")


# User panel (main function)
def user_panel():
    while True:
        print("\n====== User Panel ======")
        print("1. View Menu")
        print("2. Place Order")
        print("3. Exit User Panel")
        choice = input("Enter choice: ")

        if choice == "1":
            show_menu()
        elif choice == "2":
            place_order()
        elif choice == "3":
            print("👋 Exiting User Panel...")
            break
        else:
            print("⚠ Invalid choice. Try again.")


# Run only if executed directly (not imported)
if __name__ == "__main__":
    user_panel()
