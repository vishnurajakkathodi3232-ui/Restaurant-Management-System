import sqlite3
from datetime import datetime
from admin import admin_login, admin_panel   # Admin functions
from user import user_panel                  # User functions

DB_NAME = "restaurant.db"

def create_db():
    conn = sqlite3.connect(DB_NAME)
    print(" Database Connected Successfully ")
    cursor = conn.cursor()

    # Create Menu Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Menu_table(
            item_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name VARCHAR(50) NOT NULL,
            category VARCHAR(50) NOT NULL,
            price REAL NOT NULL,
            available TEXT CHECK(available IN ('yes','no')) NOT NULL,
            time_slot TEXT CHECK(time_slot IN ('breakfast','lunch','dinner','all')) NOT NULL
        )
    """)

    # Create Orders Table
    cursor.execute("""    
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            items TEXT NOT NULL,
            total_price REAL NOT NULL,
            order_date TEXT NOT NULL
        )
    """)

    # Create Admin Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)

    
    cursor.execute("SELECT * FROM admin WHERE username='vishnu'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO admin (username, password) VALUES ('vishnu', '3232')")

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")


def main():
    create_db()

    while True:
        print("\n===== Welcome to Restaurant Management System =====")
        print("1. Admin Login")
        print("2. User (Customer)")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            if admin_login():
                admin_panel()
        elif choice == "2":
            user_panel()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice, try again.")


if __name__ == "__main__":
    main()
