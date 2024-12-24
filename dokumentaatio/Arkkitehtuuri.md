# SOVELLUKSEN ARKKITEHTUURI
- Sovelluksen arkkitehtuuri noudattaa seuraavaa rakennetta:

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

```mermaid
sequenceDiagram
    participant game.py
    participant database_connection.py
    participant highscore_connection.py
    participant user_data.db
    participant scoreboard.db

    game.py<<->>database_connection.py: molemminpuoleinen yhteys
    game.py<<->>highscore_connection.py: molemminpuoleinen yhteys
    database_connection.py<<->>user_data.db: molemminpuoleinen yhteys
    highscore_connection.py<<->>scoreboard.db: molemminpuoleinen yhteys
```