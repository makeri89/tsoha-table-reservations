# Pöytävaraussovellus

Tällä sovelluksella voi tehdä pöytävarauksia ravintoloihin.

## Käyttäjäroolit

Erilaisia käyttäjärooleja on kolme: ylläpitäjä, ravintola ja asiakas.

### Asiakaskäyttäjä voi

- luoda uuden peruskäyttäjätunnuksen sekä kirjautua sisään ja ulos :heavy_check_mark:
- nähdä listan ravintoloista, jotka ovat listautuneet sovellukseen :heavy_check_mark:
  - nähdä tietoja ravintoloista, kuten aukioloajat, ruokalistan ja pöytävarauskalenterin
- luoda arvioita ravintoloille :heavy_check_mark:
- etsiä ravintoloita hakusanalla :heavy_check_mark:

### Ravintolakäyttäjä voi

- lisätä oman ravintolansa tiedot sovellukseen
- säätää pöytävarauksien saatavuutta
- muokata ravintolan tietoja, kuten ruokalistaa
- poistaa oman ravintolansa palvelusta

### Ylläpitäjä voi

- luoda ravintolakäyttäjän tunnuksia
- poistaa ravintoloita palvelusta
- poistaa ravintola-arvioita
- tehdä kaikkea, mitä asiakas- ja ravintolakäyttäjätkin :heavy_check_mark:

Tällä hetkellä toimivat toiminnallisuudet on merkitty yllä :heavy_check_mark: -emojilla.

#### Suurimmat puutteet sovelluksen toimintalogiikassa ovat tällä hetkellä

- pöytävarausten tekeminen
  - toteutus backendiin
  - kalenteri
- ravintolakäyttäjän hallintapaneeli
- ylläpitäjän hallintapaneeli

## Sovelluksen testaaminen Herokussa

Sovellus löytyy Herokussa osoitteesta [https://tsoha-table-reservations.herokuapp.com](https://tsoha-table-reservations.herokuapp.com/). Sovellukseen voi etusivulta luoda uudet tunnukset tai halutessaan kirjautua kehitysvaiheen tietokannassa olevalla ylläpitäjäkäyttäjällä, tunnuksilla admin:admin.

Kaikkiin toiminnallisuuksiin pääsee tällä hetkelä suoraan etusivulla olevista linkeistä.

Jos Herokussa oleva sovellus jostain syystä kaatuu sitä testatessasi eikä se enää aukea, voit luoda ongelmasta issuen tähän GitHub-repositorioon. Sovellus on vielä hyvin vahvasti kehitysvaiheessa, joten bugien löytyminen on enemmän kuin todennäköistä.

## Sovelluksen käyttäminen paikallisesti

Sovellus vaatii toimiakseen paikallisen PostgreSQL-tietokannan. Jos koneellasi ei ole PostgrSQL:ää, voit asentaa sen esimerkiksi [tällä](https://github.com/hy-tsoha/local-pg) skriptillä. Tietokannan tulee olla käynnissä sovellusta käytettäessä. Jos käytit asentamiseen edellä mainittua skriptiä, saat tietokannan käyntiin komennolla `start-pg.sh`.

Lataa tai kloonaa tämä repositorio koneellesi ja siirry komentorivillä sen juurikansioon:

```bash
cd tsoha-table-reservations
```

Luo kansioon `.env`-tiedosto ja aseta sinne seuraavat ympäristömuuttujat:

```
DATABASE_URL=tietokannan paikallinen osoite
SECRET_KEY=salainen avain
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

Halutessasi voit luoda tietokantaan testidataa suorittamalla `resetdb.sh` skriptin.

Nyt voit käynnistää sovelluksen komennolla

```bash
flask run
```
