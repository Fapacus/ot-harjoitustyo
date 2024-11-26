import unittest

from game import MemoryGame


class TestMemoryGame(unittest.TestCase):
    def setUp(self):
        self.game = MemoryGame.empty_database()


    def test_register_user(self):
        self.game.save_user("username1", "password1")

        self.assertTrue(self.game.check_user_existence("username1"))
        self.assertEqual(self.game.check_user_password("username1", "password1"), "password1")