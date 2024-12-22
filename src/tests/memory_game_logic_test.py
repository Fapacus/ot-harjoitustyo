import unittest
from memory_game_logic import MemoryGameLogic
from game import Game
#from memory_game import memory_game
from database_connection import database_connection
from highscore_connection import highscore_connection

data_connection = database_connection()
score_connection = highscore_connection()

class TestMemoryGameLogic(unittest.TestCase):
    def setUp(self,grid_size=4):
        self.game = Game(data_connection, score_connection)
        #self.memory_game = memory_game(self.game)
        self.game_logic = MemoryGameLogic(self.game, grid_size=4)
        self.revealed = self.game_logic.revealed
        self.width = 600
        self.margin = 25
        self.card_size = (self.width - (self.margin * (self.game_logic.grid_size))) // (self.game_logic.grid_size)

    def test_start_score(self):
        self.assertEqual(self.game_logic.score, 1000)

    def test_decrease_score(self):
        self.game_logic.decrease_score()
        self.assertEqual(self.game_logic.score, 990)

    def test_check_win(self):
        self.assertEqual(self.game_logic.check_win(), False)

        self.game_logic.paired = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 2), (2, 3), (3, 2), (3, 3)]
        self.assertEqual(self.game_logic.check_win(), True)

    def test_reveal_and_hide_card(self):
        check_true = self.game_logic.reveal_card(0, 0)
        self.assertTrue(check_true)

        check_false = self.game_logic.reveal_card(0, 0)
        self.assertEqual((False), check_false)
     
    def test_hide_card(self):
        self.assertFalse(self.revealed[1][1])
        self.revealed[1][1] = True
        self.assertTrue(self.revealed[1][1])
        self.game_logic.hide_card(1, 1)
        check_false = self.revealed[1][1]
        self.assertEqual((False), check_false)

    def test_get_card(self):
        spoton = self.game_logic.get_card((5, 5), self.margin, self.card_size)
        self.assertEqual((spoton), (0, 0))
        spotout = self.game_logic.get_card((-5, 999), self.margin, self.card_size)
        self.assertEqual((spotout), None)

    def test_handling_the_click(self):
        self.game_logic.not_pair = False
        self.game_logic.selected = []
        self.game_logic.handling_the_click((0, 0), self.margin, self.card_size)
        self.assertEqual(self.game_logic.selected, [(0, 0)])
        self.game_logic.handling_the_click((200, 200), self.margin, self.card_size)
        self.assertEqual(self.game_logic.selected, [(0, 0), (1, 1)])

        self.game_logic.not_pair = True
        self.game_logic.handling_the_click((2, 2), self.margin, self.card_size)
        self.assertEqual(self.game_logic.selected, [])
        self.assertEqual(self.game_logic.not_pair, False)

    def test_handling_the_selection(self):
        
        self.game_logic.handling_the_click((0, 0), self.margin, self.card_size)
        self.assertEqual(self.game_logic.selected, [(0, 0)])
        self.game_logic.handling_the_click((200, 200), self.margin, self.card_size)
        self.assertEqual(self.game_logic.selected, [(0, 0), (1, 1)])
        self.game_logic.not_pair = False
        self.assertEqual(self.game_logic.paired, [])
        self.game_logic.grid = [[1, 0], [0, 1]]
        self.game_logic.handling_the_selection()
        self.assertEqual(self.game_logic.paired, [(0, 0), (1, 1)])
        self.game_logic.handling_the_click((200, 2), self.margin, self.card_size)
        self.assertEqual(self.game_logic.selected, [(0, 1)])
        self.game_logic.handling_the_click((2, 200), self.margin, self.card_size)
        self.assertEqual(self.game_logic.selected, [(0, 1), (1, 0)])
        self.game_logic.grid = [[0, 0], [1, 1]]
        self.game_logic.handling_the_selection()
        self.assertTrue(self.game_logic.not_pair)

    def test_scoreboard(self):
        self.game.empty_scorebase()
        self.assertEqual(self.game.get_score_count(), 0)
        for score in range(1, 11):
            self.game_logic.scoreboard(score)
        self.assertEqual(self.game.get_score_count(), 10)
        self.assertEqual(self.game.get_lowest_score(), 1)
        self.game_logic.scoreboard(15)
        self.assertEqual(self.game.get_lowest_score(), 2)
        self.assertEqual(self.game.get_score_count(), 10)
        self.game.empty_scorebase()
