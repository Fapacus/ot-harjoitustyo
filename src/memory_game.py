import time
import pygame
from memory_game_logic import MemoryGameLogic

def memory_game(game):  # pygame settings
    """
    Has both pygame and game settings for the game. 
    """
    pygame.init()
    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Muistipeli")
    font = pygame.font.Font(None, 48)
    score_font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()

    # game settings
    game_logic = MemoryGameLogic(game, grid_size=4)
    grid_size = game_logic.grid_size  # 4x4-grid
    margin = 25
    card_size = (width - (margin * (grid_size))) // (grid_size)   # 125

    def draw_grid():  # drawing cards
        """
        Draw the grid of cards, either revealing the card values or keeping them hidden
        depending on the game and card state.
        """
        for row in range(grid_size):
            for col in range(grid_size):
                x = col * (card_size + margin) + margin   # margin, margin+card_size+margin, ...
                y = row * (card_size + margin) + margin
                rect = pygame.Rect(x, y, card_size - margin, card_size - margin)
                if game_logic.revealed[row][col]:# if the card is True
                    if (row, col) in game_logic.paired:  # if it's a pair
                        pygame.draw.rect(screen, (100, 50, 50), rect) # reddish
                    else:
                        pygame.draw.rect(screen, (200, 200, 200), rect)
                    text = font.render(str(game_logic.grid[row][col]), True, (0, 0, 0))
                    screen.blit(text, (x + card_size // 3, y + card_size // 4))
                else:   # drawing the hidden cards
                    pygame.draw.rect(screen, (50, 100, 50), rect)  # greenish

    # game loop starts right here
    running = True
    start_time = None
    while running:
        screen.fill((22, 22, 22))   # background color
        draw_grid()   # drawing the grid
        score_text = score_font.render(f"Score: {game_logic.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()   # refresh
        if game_logic.check_win(): # checking if winning the game
            end_time = time.time()
            total_time = end_time - start_time
            game_logic.score -= int(total_time)
            game_logic.scoreboard(game_logic.score)
            pygame.time.delay(3000)
            running = False

        for event in pygame.event.get():  # one event in all the events
            if event.type == pygame.QUIT:   # closing the window
                running = False             # game over

            if event.type == pygame.MOUSEBUTTONDOWN:    # if click
                if start_time is None:
                    start_time = time.time()
                position = pygame.mouse.get_pos() # save mouse position
                game_logic.handling_the_click(position, margin, card_size)
                game_logic.handling_the_selection()

        clock.tick(30)

    pygame.quit()
