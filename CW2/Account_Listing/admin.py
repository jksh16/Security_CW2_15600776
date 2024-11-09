import sqlite3
import hashlib


def login():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    username = input("Admin username: ")
    password = input("Admin password: ")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cur.execute("SELECT account_type FROM users WHERE username = ? AND password = ?",
                (username, hashed_password))
    result = cur.fetchone()

    conn.close()

    if result and result[0] == "Admin":
        print(f"Welcome Admin, {username}!")
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


def delete_product():
    conn_items = sqlite3.connect("items.db")
    conn_comments = sqlite3.connect("comment.db")
    cur_items = conn_items.cursor()
    cur_comments = conn_comments.cursor()

    cur_items.execute("SELECT id, product_name FROM products")
    products = cur_items.fetchall()

    if not products:
        print("No products available to delete.")
        return

    print("Select a product to delete:")
    for idx, product in enumerate(products, start=1):
        print(f"{idx}. {product[1]}")

    try:
        choice = int(
            input("Enter the number of the product you want to delete: ")) - 1
        if choice < 0 or choice >= len(products):
            print("Invalid selection.")
            return
        selected_product_id = products[choice][0]
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    cur_items.execute("DELETE FROM products WHERE id = ?",
                      (selected_product_id,))
    cur_comments.execute(
        "DELETE FROM comments WHERE product_id = ?", (selected_product_id,))

    conn_items.commit()
    conn_comments.commit()
    conn_items.close()
    conn_comments.close()

    print("Product and its associated comments deleted successfully!")


def edit_product():
    conn = sqlite3.connect("items.db")
    cur = conn.cursor()

    cur.execute("SELECT id, product_name, price, description FROM products")
    products = cur.fetchall()

    if not products:
        print("No products available to edit.")
        return

    print("Select a product to edit:")
    for idx, product in enumerate(products, start=1):
        print(f"{idx}. {product[1]}")

    try:
        choice = int(
            input("Enter the number of the product you want to edit: ")) - 1
        if choice < 0 or choice >= len(products):
            print("Invalid selection.")
            return
        selected_product_id = products[choice][0]
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    new_name = input(
        "Enter the new product name (leave blank to keep current): ").strip()
    new_price = input(
        "Enter the new price (leave blank to keep current): ").strip()
    new_description = input(
        "Enter the new description (leave blank to keep current): ").strip()

    current_product = products[choice]
    updated_name = new_name if new_name else current_product[1]
    updated_price = float(new_price) if new_price else current_product[2]
    updated_description = new_description if new_description else current_product[3]

    cur.execute("""
    UPDATE products 
    SET product_name = ?, price = ?, description = ? 
    WHERE id = ?
    """, (updated_name, updated_price, updated_description, selected_product_id))

    conn.commit()
    conn.close()

    print("Product details updated!")


def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. Add New Product")
        print("2. Delete Product")
        print("3. Edit Product")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            add_product()
        elif choice == '2':
            delete_product()
        elif choice == '3':
            edit_product()
        elif choice == '4':
            print("Exiting Admin Menu.")
            break
        else:
            print("Invalid option. Please try again.")


if login():
    admin_menu()
