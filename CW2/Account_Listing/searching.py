import sqlite3


def search_product():
    conn = sqlite3.connect("items.db")
    conn_comments = sqlite3.connect("comment.db")
    cur = conn.cursor()
    cur_comments = conn_comments.cursor()

    search_name = input("Enter the product name to search for: ").strip()

    cur.execute("SELECT id, product_name, price, description FROM products WHERE product_name LIKE ?",
                ('%' + search_name + '%',))
    products = cur.fetchall()

    if not products:
        print("No matching products found.")
    else:
        print("Search Results:")
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

    conn.close()
    conn_comments.close()


search_product()
