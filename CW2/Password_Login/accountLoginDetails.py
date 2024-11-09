import sqlite3

def show_all_users():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT username, password, account_type FROM users")
    users = cur.fetchall()

    if not users:
        print("No users found in the database.")
    else:
        print("List of Users:")
        print("-" * 60)
        for user in users:
            username, hashed_password, account_type = user
            print(f"Username: {username}")
            print(f"Password (hashed): {hashed_password}")
            print(f"Account Type: {account_type}")
            print("-" * 60)

    conn.close()

show_all_users()
