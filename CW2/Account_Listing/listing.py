import sqlite3
import hashlib


def login():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cur.execute("SELECT account_type FROM users WHERE username = ? AND password = ?",
                (username, hashed_password))
    result = cur.fetchone()

    conn.close()

    if result and result[0] == "Seller":
        print(f"Welcome Seller, {username}!")
        return True
    else:
        print("You have no permission to asscess this page.")
        return False


def add_product():
    conn = sqlite3.connect("items.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY,
        product_name VARCHAR(255) NOT NULL,
        price REAL NOT NULL,
        description TEXT NOT NULL
    )
    """)

    product_name = input("Enter the product name: ")

    while True:
        try:
            price = float(input("Enter the product price: "))
            if price < 0:
                print("Price cannot be negative. Please enter a valid price.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a numerical value for the price.")

    description = input("Enter a description of the product: ")

    cur.execute("INSERT INTO products (product_name, price, description) VALUES (?, ?, ?)",
                (product_name, price, description))

    conn.commit()
    conn.close()

    print(f"Product '{product_name}' added successfully!")


if login():
    add_product()
