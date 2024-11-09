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

    if result and result[0] == "User":
        print(f"Welcome, {username}!")
        return True
    else:
        print("You have no permission to asscess this page.")
        return False


def list_all_products():
    conn_items = sqlite3.connect("items.db")
    conn_comments = sqlite3.connect("comment.db")
    cur_items = conn_items.cursor()
    cur_comments = conn_comments.cursor()

    cur_comments.execute("""
    CREATE TABLE IF NOT EXISTS comments(
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        comment TEXT NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    """)

    cur_items.execute(
        "SELECT id, product_name, price, description FROM products")
    products = cur_items.fetchall()

    if not products:
        print("No products found.")
    else:
        print("Available Products:")
        print("-" * 50)
        for product in products:
            product_id, product_name, price, description = product
            print(f"Product Name: {product_name}")
            print(f"Price: ${price:.2f}")
            print(f"Description: {description}")

            cur_comments.execute(
                "SELECT comment FROM comments WHERE product_id = ?", (product_id,))
            comments = cur_comments.fetchall()

            if comments:
                print("Comments:")
                for comment in comments:
                    print(f"- {comment[0]}")
            else:
                print("No comments yet.")

            print("-" * 50)

    conn_items.close()
    conn_comments.close()


def add_comment():

    conn_items = sqlite3.connect("items.db")
    conn_comments = sqlite3.connect("comment.db")
    cur_items = conn_items.cursor()
    cur_comments = conn_comments.cursor()

    cur_items.execute("SELECT id, product_name FROM products")
    products = cur_items.fetchall()

    if not products:
        print("No products available to comment on.")
        return

    print("Select a product to comment on:")
    for idx, product in enumerate(products, start=1):
        print(f"{idx}. {product[1]}")

    try:
        choice = int(
            input("Enter the number of the product you want to comment on: ")) - 1
        if choice < 0 or choice >= len(products):
            print("Invalid selection.")
            return
        selected_product_id = products[choice][0]
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    comment = input("Enter your comment: ").strip()

    if comment:
        cur_comments.execute("INSERT INTO comments (product_id, comment) VALUES (?, ?)",
                             (selected_product_id, comment))
        conn_comments.commit()
        print("Comment added successfully!")
    else:
        print("No comment was entered.")

    conn_items.close()
    conn_comments.close()


if login():
    list_all_products()
    add_comment()
