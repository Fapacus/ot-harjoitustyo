import unittest
import sqlite3
from unittest.mock import patch
from game import Game
from database_connection import database_connection
from highscore_connection import highscore_connection
data_connection = database_connection()
score_connection = highscore_connection()

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(data_connection, score_connection)
        self.game.empty_database()
        self.game.empty_scorebase()
        

    def test_save_user(self):
        self.game.save_user("username", "password")
        self.assertTrue(self.game.check_user_existence("username"))
        self.assertEqual(self.game.check_user_password("username"), "password")
        self.game.empty_database()

    def test_login_user_success(self):
        self.game.save_user("username", "password")
        inputs = iter(["username", "password"])
        self.game.user_input = lambda _: next(inputs)
        self.game.login_user()
        self.assertEqual(self.game.get_username(), "username")
        self.game.empty_database()

    @patch("builtins.print")
    def test_login_user_fail(self, mock_print):
        self.game.save_user("username", "password")
        inputs = iter(["wrongname", "username", "wrongword", "username", "password"])
        self.game.user_input = lambda _: next(inputs)
        self.game.login_user()
        mock_print.assert_any_call("There is no such user. Please try again!")
        mock_print.assert_any_call("Password lacking. Please try again!")
        self.assertEqual(self.game.get_username(), "username")
        self.game.empty_database()

    def test_load_users(self):
        users = self.game.load_users()
        self.assertEqual(users, {})
        self.cursor = data_connection.cursor()
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("username", "password"))
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("username2", "password2"))
        data_connection.commit()
        users = self.game.load_users()
        self.assertEqual(users, {"username": "password", "username2": "password2"})
        self.game.empty_database()

    @patch("builtins.print")
    def test_register_user(self, mock_print):
        inputs = iter(["username", "password", "username", "username2", "password2"])
        self.game.user_input = lambda _: next(inputs)
        self.game.register_user()
        mock_print.assert_called_with("User registered successfully!")
        self.game.register_user()
        mock_print.assert_any_call("Copycat. Please try again!")
        mock_print.assert_called_with("User registered successfully!")

        self.assertEqual(self.game.check_user_existence("username"), True)
        self.assertEqual(self.game.check_user_password("username"), "password")
        self.assertEqual(self.game.check_user_existence("username2"), True)
        self.assertEqual(self.game.check_user_password("username2"), "password2")
        users = self.game.load_users()
        self.assertEqual(users, {"username": "password", "username2": "password2"})
        self.game.empty_database()

    @patch("builtins.print")
    def test_print_users(self, mock_print):
        self.game.print_users("user")
        mock_print.assert_called_with("There is no user data yet.")
        self.game.print_users("admin")
        mock_print.assert_called_with("There is no user data yet.")
        self.game.save_user("username", "password")
        self.game.print_users("user")
        mock_print.assert_called_with("Username: username, Password: SECRET")
        self.game.print_users("admin")
        mock_print.assert_called_with("Username: username, Password: password")
        self.game.empty_database()

    def test_save_score(self):
        self.game.save_score(10)
        self.assertEqual(self.game.get_lowest_score(), 10)
        self.game.save_score(100)
        self.assertEqual(self.game.get_lowest_score(), 10)
        self.assertEqual(self.game.get_score_count(), 2)
        self.game.save_score(5)
        self.assertEqual(self.game.get_lowest_score(), 5)
        self.assertEqual(self.game.get_score_count(), 3)
        self.game.empty_scorebase()

    @patch("builtins.print")
    def test_print_scores(self, mock_print):
        self.game.print_scores()
        mock_print.assert_called_with("There are no scores yet.")
        self.game.save_score(10)
        self.game.save_score(100)
        self.game.save_score(5)
        self.assertEqual(self.game.get_score_count(), 3)
        self.game.print_scores()
        mock_print.assert_any_call("SCOREBOARD")
        mock_print.assert_any_call("--------------------------")
        mock_print.assert_any_call("1: Username: , Score: 100")
        mock_print.assert_any_call("2: Username: , Score: 10")
        mock_print.assert_any_call("3: Username: , Score: 5")
        self.game.empty_scorebase()

    def test_del_lowest_score(self):
        self.game.save_score(10)
        self.game.save_score(100)
        self.game.save_score(5)
        self.assertEqual(self.game.get_lowest_score(), 5)
        self.assertEqual(self.game.get_score_count(), 3)
        self.game.del_lowest_score()
        self.assertEqual(self.game.get_lowest_score(), 10)
        self.assertEqual(self.game.get_score_count(), 2)
        self.game.empty_scorebase()