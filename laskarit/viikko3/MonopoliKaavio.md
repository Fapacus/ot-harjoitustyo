```mermaid
 classDiagram
    Monopolipeli "1" -- "2" Noppa
    Monopolipeli "1" -- "1" Pelilauta
    Pelilauta "1" -- "40" Ruutu
    Ruutu "1" -- "1" Ruutu : seuraava
    Ruutu "1" -- "0..8" Pelinappula
    Pelinappula "1" -- "1" Pelaaja
    Pelaaja "2..8" -- "1" Monopolipeli
    Ruutu <-- Aloitusruutu
    Ruutu <-- Vankila
    Ruutu <-- Sattuma_ja_yhteismaa
    Ruutu <-- Asemat_ja_laitokset
    Ruutu <-- Normaalit_kadut
    Monopolipeli -- Aloitusruutu
    Monopolipeli -- Vankila
    Aloitusruutu <-- Toiminto1
    Vankila <-- Toiminto2
    Sattuma_ja_yhteismaa <-- Toiminto3
    Asemat_ja_laitokset <-- Toiminto4
    Normaalit_kadut <-- Toiminto5
    Sattuma_ja_yhteismaa <-- Kortti1
    Sattuma_ja_yhteismaa <-- Kortti2
    Sattuma_ja_yhteismaa <-- Kortti3
    Kortti1 <-- Toiminto6
    Kortti2 <-- Toiminto7
    Kortti3 <-- Toiminto8
    Normaalit_kadut "1" -- "0..4" Talo
    Normaalit_kadut "1" -- "0..1" Hotelli 
```
