import unittest
import sqlite3
from game import Game

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(sqlite3.connect(":memory:"))
        self.game.empty_database()

    def test_register_user(self):
        self.game.save_user("username1", "password1")
        self.assertTrue(self.game.check_user_existence("username1"))
        self.assertEqual(self.game.check_user_password("username1"), "password1")
