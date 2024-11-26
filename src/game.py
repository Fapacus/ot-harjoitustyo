import sqlite3
from database_connection import create_connection

class MemoryGame:
    def __init__(self, connection):
        #self.user_data = user_data
        self.connection = connection #sqlite3.connect(user_data)
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT
            );
        """)
        self.connection.commit()

    def load_users(self):
        users = {}
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT username, password FROM users")
            for row in cursor.fetchall():
                username, password = row
                users[username] = password
        except sqlite3.DatabaseError:
            print("There is no user data yet.")
        return users

    def save_user(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        self.connection.commit()

    def register_user(self):
        while True:
            username = input("Enter username: ").strip()
            if self.check_user_existence(username):
                print("Copycat. Please try again!")
            else:
                password = input("Enter password: ").strip()
                self.save_user(username, password)
                print("User registered successfully!")
                break

    def login_user(self):
        while True:
            username = input("Enter username: ").strip()
            if not self.check_user_existence(username):
                print("There is no such user. Please try again!")
            else:
                password = input("Enter password: ").strip()
                if self.check_user_password(username) == password:
                    print("You in!")
                    break
                print("Password lacking. Please try again!")

    def check_user_existence(self, username):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT 1 FROM users WHERE username = ?", (username,)
        )
        return cursor.fetchone() is not None

    def check_user_password(self, username):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE username = ?", (username,)
        )
        result = cursor.fetchone()
        return result[0]

    def print_users(self):
        users = self.load_users()
        if len(users) == 0:
            print("There is no user data yet.")
            return
        for username, password in users.items():
            print(f"Username: {username}, Password: {password}")

    def empty_database(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM users")
        self.connection.commit()

    def main(self):
        while True:
            choice = input(
                "What u wanna do?\n"
                "1. Register\n"
                "2. Login\n"
                "3. Print all users\n"
                "4. Exit\n"
            )
            if choice == "1":
                self.register_user()
            elif choice == "2":
                self.login_user()
            elif choice == "3":
                self.print_users()
            elif choice == "4":
                print("Auf Wiedersehen!")
                self.connection.close()
                break
            else:
                print("Hell no! Please try again.")

if __name__ == "__main__":
    database_connection = create_connection()
    game = MemoryGame(database_connection)
    game.main()
