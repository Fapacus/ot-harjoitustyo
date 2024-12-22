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
        """
        Creates the 'users' table in the database if it does not exist.
        The table includes columns for 'username' as the primary key and 'password'.
        """
        cursor = self.data_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT
            );
        """)
        self.data_connection.commit()

    def create_scoretable(self):
        """
        Creates the 'scores' table in the database if it does not exist.
        The table includes columns for 'username', 'score', and 'timestamp'.
        """
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
        """
        Loads all users from the 'users' table in the database.

        Returns:
            A dictionary where the keys are usernames and the values are passwords.
        """
        users = {}
        cursor = self.data_connection.cursor()
        cursor.execute("SELECT username, password FROM users")
        for row in cursor.fetchall():
            username, password = row
            users[username] = password
        return users

    def save_user(self, username, password):
        """
        Saves a user to the 'users' table in the database.

        Args:
            username: The username of the user to be saved.
            password: The password of the user to be saved.
        """
        cursor = self.data_connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        self.data_connection.commit()

    def register_user(self):
        """
        Registers a user to the 'users' table in the database.
        
        Asks the user for a username and password, and if the username does not exist yet,
        saves the user to the database and prints a success message. If the username already exists,
        prints a message and asks again.
        """
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
        """
        Logs in a user to the game.

        Asks the user for a username and password, and if the username exists and the
        password is correct, sets the user to the current user and prints a success message.
        If the username does not exist, prints a message and asks again. If the password is
        incorrect, prints a message and asks again.
        """
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
        """
        Checks if a user exists in the database.

        Args:
            username: The username to check.

        Returns:
            True if the user exists, otherwise False.
        """
        cursor = self.data_connection.cursor()
        cursor.execute(
            "SELECT 1 FROM users WHERE username = ?", (username,)
        )
        return cursor.fetchone() is not None

    def check_user_password(self, username):
        """
        Checks the password of a user in the database.

        Args:
            username: The username for which to check the password.

        Returns:
            The password of the user if it exists, otherwise None.
        """
        cursor = self.data_connection.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE username = ?", (username,)
        )
        result = cursor.fetchone()
        return result[0]

    def print_users(self, status):
        """
        Prints all users in the database, with either showing or hiding their passwords,
        depending on the status of the user.

        Args:
            The status of the user, either "user" or "admin".
        """
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
        """
        Saves a score for the current user in the 'scores' table of the score database.

        Args:
            The score to save.
        """
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
        """
        Prints all scores in the database, ordered by score and timestamp (in case of ties).

        If there are no scores yet, prints a message to that effect.
        Otherwise, prints the scores in order, with the ranking number, username, and score.
        """
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
        """
        Returns the lowest score from the 'scores' table in the score database.

        Returns:
            The lowest score as an integer.
        """
        
        cursor = self.score_connection.cursor()
        cursor.execute("SELECT MIN(score) FROM scores")
        return cursor.fetchone()[0]

    def del_lowest_score(self):
        """
        Deletes the lowest score from the 'scores' table in the score database.
        """
        cursor = self.score_connection.cursor()
        cursor.execute("DELETE FROM scores WHERE score = (SELECT MIN(score) FROM scores)")
        self.score_connection.commit()

    def get_score_count(self):
        """
        Gets the total number of scores stored in the 'scores' table of the score database.

        Returns:
            The count of scores as an integer.
        """
        cursor = self.score_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM scores")
        return cursor.fetchone()[0]

    def get_username(self):
        """
        Gets the username of the currently logged in user.

        Returns:
            The username as a string.
        """
        return self.user

    def empty_database(self):
        """
        Empties the 'users' table in the database.

        Used with the tests.
        """
        cursor = self.data_connection.cursor()
        cursor.execute("DELETE FROM users")
        self.data_connection.commit()

    def empty_scorebase(self):
        """
        Empties the 'scores' table in the score database.

        Used with the tests.
        """
        cursor = self.score_connection.cursor()
        cursor.execute("DELETE FROM scores")
        self.score_connection.commit()

databas_connection = database_connection()
scoreboard_connection = highscore_connection()
game = Game(databas_connection, scoreboard_connection)
