from database_connection import database_connection
from highscore_connection import highscore_connection

class Game:
    def __init__(self, data_connection, score_connection):
        self.data_connection = data_connection
        self.score_connection = score_connection
        self.user = ""
        self.user_input = input
        self.create_datatable()
        self.create_scoretable()

    def create_datatable(self):
        cursor = self.data_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT
            );
        """)
        self.data_connection.commit()

    def create_scoretable(self):
        cursor = self.score_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                username TEXT,
                score INTEGER,
                timestamp DATETIME
            );
        """)
        self.score_connection.commit()

    def load_users(self):
        users = {}
        cursor = self.data_connection.cursor()
        cursor.execute("SELECT username, password FROM users")
        for row in cursor.fetchall():
            username, password = row
            users[username] = password
        return users

    def save_user(self, username, password):
        cursor = self.data_connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        self.data_connection.commit()

    def register_user(self):
        while True:
            username = self.user_input("Enter username: ").strip()
            if self.check_user_existence(username):
                print("Copycat. Please try again!")
            else:
                password = self.user_input("Enter password: ").strip()
                self.save_user(username, password)
                print("User registered successfully!")
                break

    def login_user(self):
        while True:
            username = self.user_input("Enter username: ").strip()
            if not self.check_user_existence(username):
                print("There is no such user. Please try again!")
            else:
                password = self.user_input("Enter password: ").strip()
                if self.check_user_password(username) == password:
                    self.user = username
                    print("You in!")
                    break
                print("Password lacking. Please try again!")

    def check_user_existence(self, username):
        cursor = self.data_connection.cursor()
        cursor.execute(
            "SELECT 1 FROM users WHERE username = ?", (username,)
        )
        return cursor.fetchone() is not None

    def check_user_password(self, username):
        cursor = self.data_connection.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE username = ?", (username,)
        )
        result = cursor.fetchone()
        return result[0]

    def print_users(self, status):
        users = self.load_users()
        if len(users) == 0:
            print("There is no user data yet.")
            return
        if status == "user":
            for username in users.items():
                print(f"Username: {username[0]}, Password: SECRET")
        elif status == "admin":
            for username in users.items():
                print(f"Username: {username[0]}, Password: {username[1]}")

    def save_score(self, score):
        print("Saving score for user:", self.user)
        username = self.user
        cursor = self.score_connection.cursor()
        cursor.execute(
            "INSERT INTO scores (username, score) VALUES (?, ?)",
            (username, score)
        )
        print("You made it to Scoreboard!")
        self.score_connection.commit()

    def print_scores(self):
        print("SCOREBOARD")
        print("--------------------------")
        if self.get_score_count() == 0:
            print("There are no scores yet.")
            return
        cursor = self.score_connection.cursor()
        cursor.execute("SELECT username, score FROM scores ORDER BY score DESC, timestamp ASC")
        count = 0
        for row in cursor.fetchall():
            count += 1
            username, score = row
            print(f"{count}: Username: {username}, Score: {score}")

        self.score_connection.commit()

    def get_lowest_score(self):
        cursor = self.score_connection.cursor()
        cursor.execute("SELECT MIN(score) FROM scores")
        return cursor.fetchone()[0]

    def del_lowest_score(self):
        cursor = self.score_connection.cursor()
        cursor.execute("DELETE FROM scores WHERE score = (SELECT MIN(score) FROM scores)")
        self.score_connection.commit()

    def get_score_count(self):
        cursor = self.score_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM scores")
        return cursor.fetchone()[0]

    def get_username(self):
        return self.user

    def empty_database(self):
        cursor = self.data_connection.cursor()
        cursor.execute("DELETE FROM users")
        self.data_connection.commit()

    def empty_scorebase(self):
        cursor = self.score_connection.cursor()
        cursor.execute("DELETE FROM scores")
        self.score_connection.commit()

databas_connection = database_connection()
scoreboard_connection = highscore_connection()
game = Game(databas_connection, scoreboard_connection)
