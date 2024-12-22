import random
from database_connection import database_connection
from highscore_connection import highscore_connection

data_connection = database_connection()
score_connection = highscore_connection()


class MemoryGameLogic:
    def __init__(self, game, grid_size):
        self.game = game
        self.grid_size = grid_size
        self.cards = self.create_cards()
        self.grid = self.create_grid()
        self.revealed = [[False] * grid_size for _ in range(grid_size)]
        self.paired = []
        self.selected = []
        self.not_pair = False
        self.score = 1000

    def create_cards(self):
        """
        Creates the cards for the game. The number of cards is
        grid_size * grid_size. The cards are shuffled.

        Returns: a list of shuffled cards.
        """
        cards = list(range(1, (self.grid_size * self.grid_size // 2) + 1)) * 2
        random.shuffle(cards)
        return cards

    def create_grid(self):
        """
        Creates the game grid. The grid is a list of lists, where each inner
        list represents a row in the grid. The length of the grid is equal to
        the grid_size.

        Returns: a list of lists representing the game grid.
        """
        grid = []
        for i in range(self.grid_size):
            row = self.cards[i * self.grid_size:(i + 1) * self.grid_size]
            grid.append(row)
        return grid

    def reveal_card(self, row, col):
        """
        Reveals a card in the game grid at the given row and column.

        Args:
            row: The row of the card to reveal.
            col: The column of the card to reveal.

        Returns: True if the card was revealed, False if it was already revealed.
        """
        if not self.revealed[row][col]:
            self.revealed[row][col] = True
            return True
        return False

    def hide_card(self, row, col):
        """
        Hides a card in the game grid at the given row and column.

        Args:
            row: The row of the card to hide.
            col: The column of the card to hide.
        """
        if self.revealed[row][col]:
            self.revealed[row][col] = False


    def get_card(self, mouse_click, margin, card_size):    # minkä kortin kohalla klikataan
        """
        Determines the card position in the grid based on a mouse click.

        Args:
            mouse_click: A tuple containing the x and y coordinates of the mouse click.

        Returns:
            A tuple (row, col) representing the grid position of the clicked card,
            or None if the click is outside the grid boundaries.
        """
        x, y = mouse_click
        col, row = x // (card_size + margin), y // (card_size + margin)
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            return row, col
        return None

    def check_win(self):
        """
        Checks if the game is won by checking the length of paired list.

        Returns:
            True if the game is won, False otherwise.
        """
        return len(self.paired) == self.grid_size * self.grid_size

    def handling_the_click(self, position, margin, card_size):
        """
        Handles the click event on the game grid depending on the boolean value of not_pair.
        
        Args:
            position: A tuple containing the x and y coordinates of the click event.
        """
        if self.not_pair:    # jos todettu että ei pari ja nappia painettiin
            r1, c1 = self.selected[0]
            r2, c2 = self.selected[1]
            self.hide_card(r1, c1)
            self.hide_card(r2, c2)
            self.selected = []  # valittujen korttien tyhjennys
            self.not_pair = False  # muutetaan taas Falseksi
        else:
            # pelaaja kääntää uuden kortin
            card = self.get_card(position, margin, card_size)
            if card and not self.revealed[card[0]][card[1]]:  # tarkistus onko jo käännetty
                self.selected.append(card)
                self.reveal_card(card[0], card[1])

    def handling_the_selection(self):
         # tarkistetaan onko kaksi korttia valittu ja False
        """
        First checking if two cards are selected and not_pair is False.
        Then checking if the selected cards have the same value. If they do,
        they are added to the paired list. If they don't, not_pair is set to True.
        """
        if len(self.selected) == 2 and not self.not_pair:
            r1, c1 = self.selected[0]
            r2, c2 = self.selected[1]

            if self.grid[r1][c1] == self.grid[r2][c2]:  # jos käännetyissä korteissa on sama arvo
                self.paired.append(self.selected[0])     # lisätään valmis pari
                self.paired.append(self.selected[1])
                self.selected = []   # jos tuli pari nii selectin tyhjennys
            else:
                self.not_pair = True  # muutetaan Trueksi
                self.decrease_score()

    def decrease_score(self):
        """
        Decreases the score by 10 points if it is not already zero.
        """
        self.score = max(0, self.score - 10)

    def scoreboard(self, score):
        if self.game.get_score_count() >= 10:
            lowest_score = self.game.get_lowest_score()
            if score > lowest_score:
                self.game.del_lowest_score()
                self.game.save_score(score)
        else:
            self.game.save_score(score)

        print(f"Your score was: {score}")
