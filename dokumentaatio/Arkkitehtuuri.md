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

- Sovelluksen tekstikäyttöliittymä "main.py" noudattaa seuraavaa rakennetta:

```mermaid
sequenceDiagram
    participant User
    participant Main
    participant Game
    participant Database
    participant Scorebase

    User->>Main: Käynnistä ohjelma
    loop Valikkotoiminnot
        User->>Main: Valitse toiminto
        alt Pelaa peliä
            Main->>memory_game: Käynnistä peli
        else Rekisteröi käyttäjä
            Main->>Game: register_user()
            Game->>Database: Tallenna tiedot
        else Kirjaudu sisään
            Main->>Game: login_user()
            Game->>Database: Hae kirjautumistiedot verrattaviksi
        else Tulosta Pistetaulukko
            Main->>Game: print_scores()
            Game->>Scorebase: Hae pistetaulukko
        else Tulosta käyttäjät "Userina"
            Main->>Game: print_users("user")
            Game->>Database: Hae käyttäjät
        else Tulosta käyttäjät "Adminina"
            Main->>Game: print_users("admin")
            Game->>Database: Hae käyttäjät
        else Poistu
            Main->>Game: Sulje yhteys
            Main->>User: Ohjelma kiinni, moikka!
        end
    end
```

## SOVELLUKSEN ARKKITEHTUURI SANALLISESTI KUVATTUNA
- Tiedosto main.py käynnistää sovelluksen ja toimii käyttäjälle samalla tekstikäyttöliittymänä.
- Vaihtoehtoina tekstikäyttöliittymässä on käyttäjällä pelata, rekisteröityä, kirjautua sisään, tulostaa pistetaulukko, tulostaa käyttäjät ilman salasanan näkyvyyttä, tulostaa käyttäjät salasana näkyvillä, ja lopettaa sovelluksen käyttö.

- Tiedosto game.py sisältää käytännössä kaikki "käytännön asiat", jotka eivät liity niinkään suoranaisesti pelaamiseen, vaan ennemmin tietojen tarkistamiseen, tuomiseen ja tallentamiseen. Sekä main.py että memory_game_logic käyttävät game.py -tiedostoa toiminnoissaan.

- Tiedosto memory_game.py sisältää itse muistipelin pyörittämiseen tarvittavat asiat kuten graafisen käyttöliittymän. Memory_game.py kommunikoi runsaasti memory_game_logic.py -tiedoston kanssa.

- Tiedosto memory_game_logic sisältää käytännössä kaikki muistipelissä tarvittavat toiminnallisuudet ja se hyödyntää toiminnoissaan game.py -tiedostoa.

- Tiedostot database_connection.py ja highcore_connection.py kommunikoivat tiedoston game.py kanssa ja toimivat näin ollen yhteyksien luojina tietokantataluihin user_data.db ja scoreboard.db.