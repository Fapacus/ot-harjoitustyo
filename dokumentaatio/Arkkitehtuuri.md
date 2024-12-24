# SOVELLUKSEN ARKKITEHTUURI
- Sovelluksen arkkitehtuuri noudattaa käyttöliittymien ja logiikan osalta seuraavaa rakennetta:

```mermaid
sequenceDiagram
    participant main.py
    participant game.py
    participant memory_game.py
    participant memory_game_logic.py

    main.py->>game.py: kutsuu sovelluslogiikkaa
    main.py->>memory_game.py: käynnistää muistipelin
    memory_game.py->>memory_game_logic.py: kutsuu pelilogiikkaa
    memory_game_logic.py->>game.py: kutsuu sovelluslogiikkaa
```

- Sovelluksen arkkitehtuuri noudattaa tiedon tallentamisen ja haun osalta seuraavaa rakennetta:

```mermaid
sequenceDiagram
    participant game.py
    participant database_connection.py
    participant highscore_connection.py
    participant user_data.db
    participant scoreboard.db

    game.py<<->>database_connection.py: yhteys käyttäjien tietoihin
    game.py<<->>highscore_connection.py: yhteys pistetaulukkoon
    database_connection.py<<->>user_data.db: yhteys käyttäjien tiedot sisältävään tietokantaan
    highscore_connection.py<<->>scoreboard.db: yhteys pistetaulukon tiedot sisältävään tietokantaan
```