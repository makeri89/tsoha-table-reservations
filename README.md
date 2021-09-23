# Pöytävaraussovellus

Tällä sovelluksella voi tehdä pöytävarauksia ravintoloihin.

## Käyttäjäroolit

Erilaisia käyttäjärooleja on kolme: ylläpitäjä, ravintola ja asiakas.

### Asiakaskäyttäjä voi

- luoda uuden peruskäyttäjätunnuksen sekä kirjautua sisään ja ulos
- nähdä listan ravintoloista, jotka ovat listautuneet sovellukseen
  - nähdä tietoja ravintoloista, kuten aukioloajat, ruokalistan ja pöytävarauskalenterin
- luoda arvioita ravintoloille
- etsiä ravintoloita hakusanalla ja kategorian mukaan

### Ravintolakäyttäjä voi

- lisätä oman ravintolansa tiedot sovellukseen
- säätää pöytävarauksien saatavuutta
- muokata ravintolan tietoja, kuten ruokalistaa
- poistaa oman ravintolansa palvelusta

### Ylläpitäjä voi

- luoda ravintolakäyttäjän tunnuksia
- poistaa ravintoloita palvelusta
- poistaa ravintola-arvioita
- tehdä kaikkea, mitä asiakas- ja ravintolakäyttäjätkin

## Sovelluksen käyttäminen paikallisesti

Lataa tai kloonaa tämä repositorio koneellesi ja siirry komentorivillä sen juurikansioon:

```bash
cd tsoha-table-reservations
```

Siirry virtuaaliympäristöön komennoilla

```bash
python3 -m venv venv
source venv/bin/activate
```

Asenna sitten riippuvuudet komennolla

```bash
pip install -r requirements.txt
```

Nyt voit käynnistää sovelluksen komennolla

```bash
flask run
```
