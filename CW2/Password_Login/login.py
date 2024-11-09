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

    if result:
        account_type = result[0]
        print(f"Welcome {account_type}, {username}!")
    else:
        print("Invalid username or password. Please try again.")

    conn.close()


login()
