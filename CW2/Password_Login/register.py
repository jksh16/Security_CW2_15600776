import sqlite3
import hashlib
import re


def is_strong_password(password):
    if (len(password) > 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'\d', password) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):
        return True
    return False


def create_account():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        account_type VARCHAR(50) NOT NULL
    )
    """)

    username = input("Enter a username: ")

    while True:
        print("Select account type:")
        print("1. User")
        print("2. Seller")
        print("3. Admin")
        account_type_choice = input("Enter 1, 2, or 3: ")

        if account_type_choice == '1':
            account_type = "User"
            break
        elif account_type_choice == '2':
            account_type = "Seller"
            break
        elif account_type_choice == '3':
            account_type = "Admin"
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

    while True:
        password = input("Enter a password: ")
        confirm_password = input("Confirm your password: ")

        if password != confirm_password:
            print("Passwords do not match. Please try again.")
        elif not is_strong_password(password):
            print(
                "Password is not strong enough. Please make sure it meets the following criteria:")
            print("• Length must be more than 8 characters")
            print("• At least one uppercase letter and one lowercase letter")
            print("• At least one number")
            print("• At least one symbol (e.g., !@#$%^&*)")
        else:
            break

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cur.execute("INSERT INTO users (username, password, account_type) VALUES (?, ?, ?)",
                (username, hashed_password, account_type))

    conn.commit()
    conn.close()

    print(f"{account_type} account created successfully!")


create_account()
