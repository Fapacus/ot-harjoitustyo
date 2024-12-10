import unittest
from memory_game_logic import MemoryGameLogic

class TestMemoryGameLogic(unittest.TestCase):
    def setUp(self):
        self.game_logic = MemoryGameLogic(grid_size=4)

    def test_start_score(self):
        self.assertEqual(self.game_logic.score, 1000)

    def test_decrease_score(self):
        self.game_logic.decrease_score()
        self.assertEqual(self.game_logic.score, 990)

    def test_check_win(self):
        self.assertEqual(self.game_logic.check_win(), False)

        self.game_logic.paired = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 2), (2, 3), (3, 2), (3, 3)]
        self.assertEqual(self.game_logic.check_win(), True)
