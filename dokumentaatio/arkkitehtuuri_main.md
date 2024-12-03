```mermaid
sequenceDiagram
    participant User
    participant Main
    participant Game
    participant Database

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
        else Tulosta käyttäjät
            Main->>Game: print_users()
            Game->>Database: Hae käyttäjät
        else Poistu
            Main->>Game: Sulje yhteys
            Main->>User: Ohjelma kiinni, moikka!
        end
    end
```
