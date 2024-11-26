import unittest
import sys
sys.path.append('C:\\Users\\Fapacus\\Desktop\\Koulu_fileet\\ot-harjoitustyo')
from game import MemoryGame

class TestMemoryGame(unittest.TestCase):
    def setUp(self):
        self.game = MemoryGame.empty_database()

    def test_register_user(self):
        MemoryGame.save_user("username1", "password1")
        self.assertTrue(MemoryGame.check_user_existence("username1"))
        self.assertEqual(MemoryGame.check_user_password("username1", "password1"), "password1")
