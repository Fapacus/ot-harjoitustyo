import pygame
import random

def memory_game():
    # pygame asetukset
    pygame.init()
    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Muistipeli")
    font = pygame.font.Font(None, 48)
    fps = 30
    clock = pygame.time.Clock()

    # pelin asetukset
    grid_size = 4  # 4x4-ruudukko
    margin = 25
    card_size = (width - (margin * (grid_size))) // (grid_size)   # 125


    # korttien luonti
    cards = list(range(1, (grid_size * grid_size // 2) + 1)) * 2   # 1-8 kahteen kertaan
    print(cards)
    random.shuffle(cards)   # sekotetaan kortit
    grid = []  # pelitaulukko korteista
    for i in range(grid_size):
        row = cards[i * grid_size:(i + 1) * grid_size]   # 0-4, 4-8, 8-12, 12-16
        grid.append(row)

    revealed = [[False] * grid_size for _ in range(grid_size)]   # False, False, ...
    selected = []   # valitut kortit

    def draw_grid():  # korttien piirtäminen
        for row in range(grid_size):
            for col in range(grid_size):
                x = col * (card_size + margin) + margin   # margin, margin+card_size+margin, ...
                y = row * (card_size + margin) + margin
                rect = pygame.Rect(x, y, card_size - margin, card_size - margin)
                if revealed[row][col]:   # jos kortti True, piirretään kortin arvo näkyville
                    if (row, col) in paired:  # jos kortti on jo pari
                        pygame.draw.rect(screen, (100, 50, 50), rect) # punertava
                    else:
                        pygame.draw.rect(screen, (200, 200, 200), rect)
                    text = font.render(str(grid[row][col]), True, (0, 0, 0))
                    screen.blit(text, (x + card_size // 3, y + card_size // 4))
                else:   # piirretään kortin selkämys
                    pygame.draw.rect(screen, (50, 100, 50), rect)  # vihertävä

    def get_card(mouse_click):  # minkä kortin kohalla klikataan
        x, y = mouse_click
        print(mouse_click)
        col, row = x // (card_size + margin), y // (card_size + margin)
        print(col, "  ,   ", row)
        if 0 <= row <= grid_size and 0 <= col <= grid_size:  # jos klikkaus ikkunan sisällä
            return row, col
        return None
    def check_win():
        if len(paired) == grid_size * grid_size:
            return True
        return False

    # peli looppi alkaa
    running = True
    not_pair = False  # tarvitaanko klikkaus pelin jatkamiseksi
    paired = []   # valmiit parit

    while running:
        screen.fill((22, 22, 22))  # taustan väri
        draw_grid()  # piirrä korttiruudukko
        pygame.display.flip()  # päivitä tiedot

        if check_win(): # katotaan onko voitto
            pygame.time.delay(3000)
            running = False

        for event in pygame.event.get():  # tapahtuma kaikissa tapahtumissa
            if event.type == pygame.QUIT:   # ikkunan sulkeutuminen
                running = False             # peli loppuu

            if event.type == pygame.MOUSEBUTTONDOWN:    # jos klikkaus 
                position = pygame.mouse.get_pos()            # tallennetaan hiiren sijainti klikkauksen hetkellä

                if not_pair:    # jos todettu että ei pari ja nappia painettiin
                    r1, c1 = selected[0]
                    r2, c2 = selected[1]
                    revealed[r1][c1] = False
                    revealed[r2][c2] = False
                    selected = []  # valittujen korttien tyhjennys
                    not_pair = False  # muutetaan taas Falseksi
                else:
                    # pelaaja kääntää uuden kortin
                    card = get_card(position)
                    if card and not revealed[card[0]][card[1]]:  # tarkistus onko jo käännetty
                        selected.append(card)
                        revealed[card[0]][card[1]] = True

        # tarkistetaan onko kaksi korttia valittu ja False
        if len(selected) == 2 and not not_pair:
            r1, c1 = selected[0]
            r2, c2 = selected[1]

            if grid[r1][c1] == grid[r2][c2]:  # jos käännetyissä korteissa on sama arvo
                paired.append(selected[0])     # lisätään valmis pari
                paired.append(selected[1])
                selected = []   # jos tuli pari nii selectin tyhjennys
            else:
                not_pair = True  # muutetaan Trueksi

        clock.tick(fps)

    pygame.quit()
