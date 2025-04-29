# Kotitalouden Kauppalista

## Sovelluksen toiminnot
*  Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
*  Käyttäjä pystyy luomaan salasanalla toimivan kauppalistan.
*  Käyttäjä pystyy etsimään ja liittymään toisen käyttäjän kauppalistaan, jos tietää kauppalistan nimen ja salasanan.
*  Käyttäjä voi lisätä kauppalistaan tuotteita ja niiden tarvittavan määrän sekä muokata ja poistaa lisäämiään tuotteita.
*  Käyttäjä pystyy valitsemaan tuotteelle tuoteryhmän (elintarvikkeet, käyttötavarat, muut).
*  Käyttäjä näkee kauppalistaan lisätyt tuotteet. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät tuotteet.
*  Käyttäjä pystyy luokittelemaan tuotteen ostajaksi kenet tahansa listan jäsenistä. Luokittelun perusteella tuote siirtyy maksajan käyttäjäsivulle.
*  Käyttäjäsivulla näkyy ostotiedot:
    - Käyttäjän maksaman tuotteen hinta, määrä ja ostoaika.
    - Jos listalla on useita jäseniä, profiiliin lasketaan automaattisesti käyttäjän osuus prosentteina kaikkien käyttäjien ostoksista.
*  Eri listoilla on omat käyttäjäsivut eli ostetut tuotteet eivät mene eri listojen kesken sekaisin.
*  Kun listan viimeinen käyttäjä päättää poistua listasta, poistuu tietokannasta kaikki listaan liittyvät tiedot. Ohessa ohjelma varmistaa käyttäjältä haluaako tämä varmasti tehdä tämän.
*  Listan pystyy järjestämään tuoteryhmien perusteella.

## Sovelluksen asennus

Asenna "flask"-kirjasto:

'''
pip install flask
'''

Luo tietokanna taulut ja lisää alkutiedot:


'''
sqlite3 database.db < scgema.sql
sqlite3 database.db < init.sql
'''

Voit käynnistää sovelluksen näin:

'''
flask run
'''