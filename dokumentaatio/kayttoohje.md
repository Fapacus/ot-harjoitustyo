# Käyttöohje
Lataa projekti githubista.

## Ohjelman käynnistäminen
Aivan aluksi on suositeltavaa asentaa projektin riippuvuudet käyttäen komentoa:
```bash
poetry install
```
Tämän jälkeen voit käynnistää ohjelman käyttäen komentoa:
```
poetry run invoke start
```
Mikäli edellä mainittu ei toimi, käynnistyy peli suorittamalla src-kansiosta löytyvän "main.py"-tiedoston.


## Ohjelman käyttäminen
Ohjelman avauduttua tulostuu konsoliin numeroidut vaihtoehdot, jotka voit suorittaa syöttämällä toimenpidettä vastaavan numeron konsoliin.

Jos haluat siirtyä samantien pelaamaan, syötä numero "1". Tällöin avautuu peli-ikkuna ja voit aloittaa pelaamisen.
Jos haluat kirjautua sisään etkä ole aiemmin luonut käyttäjätunnusta, syötä numero "2", jonka seurauksena pääset rekisteröitymään pelaajaksi.
Jos olet jo rekisteröitynyt käyttäjäksi, syötä numero "3", jolloin voit kirjautua sisään käyttäjätunnuksillasi.
Jos haluat tarkastella Top 10 -pisteitä, syötä numero "4".
Jos haluat tarkastella käyttäjien listaa, syötä numero "5".
Jos olet admin ja haluat nähdä käyttäjien tiedot, syötä numero "6".
Jos haluat poistua ohjelmasta, syötä numero "7".

## Pelin säännöt/toiminta
Peliä pelataan klikkaamalla hiiren vasemmalla painikkeella peli-ikkunassa näkyviä kortteja ja yritetään näin avata samanaikaisesti kaksi samaa numeroa. 
Jos kaksi samaa numeroa löytyy, muodostuu pari eikä kyseisissä korteissa näkyvät numerot poistu enää näkyvistä.
Pelin alkaessa pisteitä on 1000, mutta jokainen korttiparin kääntäminen pienentää pisteitä kymmenellä, mikäli korteissa on toisistaan poikkeavat numerot.
Jos käännetyissä kahdessa kortissa on sama numero, muuttuvat kortit punaisiksi ja seuraava klikkaus kääntää uuden kortin (mikäli klikkaus kohdistuu pois-kääntyneenä olevaan korttiin).
Jos käännetyissä kahdessa kortissa on eri numerot, seuraava klikkaus kääntää avoinna olevat kaksi korttia takaisin selkäpuoli ylöspäin.
Oikeaan korttipariin johtamattomien kääntöjen lisäksi pisteitä vähentää aika, joka alkaa kulumaan heti kun pelaaja on klikannut peli-ikkunaa ensimmäisen kerran.
Peli loppuu, kun kaikki korttiparit ovat löytyneet, minkä jälkeen tulos tallennetaan pistetaulukkoon, mikäli tuloksesi yltää Top 10 -pisteiden joukkoon.
Jos saat samat pisteet kuin joku aiempi pelaaja, on aiemmilla pisteillä etulyöntiasema pistetaulukon suhteen. Toisin sanoen, jos pistetaulukossa on jo kymmenen tulosta, pitää uusien pisteiden olla korkeammat kuin jotkin pistetaulukossa jo olevat pisteet, jotta nämä uudet pisteet tallentuisivat pistetaulukkoon.
Kun peli päättyy, tulostuu pistemääräsi konsoliin ja peli-ikkuna sulkeutuu, jolloin palaat takaisin alkunäkymään.