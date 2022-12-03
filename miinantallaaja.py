import pyglet
import haravasto
import math
import random
import string
import time
from pyglet.window import key
from pyglet.window import mouse



#ikkunan muuttujat, joita muutetaan pelin aikana, kun siirrytään ruudusta toiseen.
#itse peli-ikkunan
tila = {
    "nakyva_kentta": [],
    "piilo_kentta": [],
    "peli": "paavalikko",
    "ikkunan_korkeus": 800,
    "ikkunan_leveys": 1000,
    "havitty": False,
    "voitettu": False,
}
#kentän ominaisuudet, johon päästään käsiksi käsittelijäfunktioissa.
kentan_ominaisuudet = {
    "leveys": 20,
    "korkeus": 10,
    "miinat": 10,
    "merkitsija": "",
    "vapaat": []
}

pelaaja = {
    "nimi": "",
    "pisteet": 0,
    "paivamaara": "",
    "top_kymmenen": [],
    "lopputulos": "",
    "kesto": "",
    "siirrot": 0
}

kello = {
    "alku": "",
    "loppu": ""
}

#Olioiden määrittely
class Nappi():
    """
    Luokka jolla voidaan luoda Nappi - olio. 
    Tarkoitettu lähinnä kollisioiden havaitsemiseen erikokoisilla spriteillä, 
    mikäli halutaan luoda yksinkertaisia käyttöliittymiä.
    
    Nappi-luokan oliot ovat muotoa
    
    Nappi(x, y, leveys, korkeus, sprite)
    
    Missä
    x ja y = spriten asettamiskoordinaatit
    leveys ja korkeus = spriten leveys ja korkeus
    sprite = spriten nimi.
    """
    def __init__(self,x,y,leveys,korkeus,sprite):
        self.x = x
        self.y = y
        self.leveys = leveys
        self.korkeus = korkeus
        self.sprite = sprite
        self.oikea_reuna = x + leveys
        self.yla_reuna = y + korkeus
        self.painettu = False
        
    def testaa_sijainti(self, koordx, koordy):
        """
        Tällä metodilla katsotaan, onko klikkaus tai sijainti napin päällä.
        Muuttaa napin "painettu" - ominaisuuden arvoon True(tosi), jos se on False(epätosi).
        
        Metodikutsu tulee olla muotoa testaa_sijainti(x, y), missä x ja y ovat tarkistettavan sijainnin koordinaatit.
        """
        if (self.x <= koordx <= self.oikea_reuna and
            self.y <= koordy <= self.yla_reuna):
            self.painettu = True
        else:
            self.painettu = False


#päävalikon napit
p_aloita        = Nappi(200, 300, 400, 100, "aloita")
p_lopeta        = Nappi(200, 150, 400, 100, "lopeta")
p_tilasto      = Nappi(600, 0, 200, 50, "tilasto")

#asetusruudun napit
a_valmis        = Nappi(500, 25, 200, 50, "valmis")
a_takaisin      = Nappi(100, 25, 200, 50, "takaisin")

a_ruud_leveys   = Nappi(400, 400, 500, 50, "input")
a_ruud_korkeus  = Nappi(400, 300, 500, 50, "input")
a_ruud_miinat   = Nappi(400, 200, 500, 50, "input")

#tilastoruudun napit
p_takaisin      = Nappi(100, 50, 200, 50, "takaisin")

#lista jonka avulla piirretään asetusruudun napit älykkäästi
a_napit = [a_valmis, a_takaisin, a_ruud_leveys, a_ruud_korkeus, a_ruud_miinat]

#lista joka sisältää kaikki numeeriset näppäimet. Käytetään näppäimistön kasittelijäfunkiossa.
numero_napit = [(key._0, "0"), (key._1, "1"), (key._2, "2"), (key._3, "3"), (key._4, "4"), 
                (key._5, "5"), (key._6, "6"), (key._7, "7"), (key._8, "8"), (key._9, "9")]

#Funktioiden määrittelyosio:

def miinoita(lista, vapaa, lukum):
    """
    Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin.
    """
    
    pituus = len(lista) - 1
    for _ in range(lukum):
        while True:
            sat_y   =   random.randint(0,   len(lista))
            sat_x   =   random.randint(0,   len(lista[pituus]))
            tupl    =   (sat_x, sat_y)
            if tupl not in vapaa:
                continue
            else:
                lista[sat_y][sat_x] = "x"
                vapaa.remove(tupl)
                break
        
def numeroi(lista):
    """
    tarkistaa miinakentän jokaisen alkion ja muuttaa alkion numeroruuduksi, jos sen vieressä on miina(tai useampi miina.)
    listan tulee olla kaksiulotteinen.
    Tulee kutsua miinoita - funktion jälkeen, sillä muuten listassa ei ole ainuttakaan miinaa, eikä funktio numeroi 
    ruutuja oikein.
    Funktio ei palauta mitään, vaan se muokkaa jo olemassa olevaa listaa.
    """
    miinat = 0
    for i, _ in enumerate(lista):
        for j, _ in enumerate(lista[i]):
            if i > 0:
                yla_rivi = lista[i - 1]
                for aa, _ in enumerate(yla_rivi):
                    if j - 1 <= aa <= j + 1 and yla_rivi[aa] == "x":
                        miinat += 1
        
            keski_rivi = lista[i]
            for bb, _ in enumerate(keski_rivi):
                if j - 1 <= bb <= j + 1 and keski_rivi[bb] == "x":
                        miinat += 1
        
            if i < len(lista)-1:
                for cc, _ in enumerate(lista[i + 1]):
                    if j - 1 <= cc <= j + 1 and lista[i + 1][cc] == "x":
                        miinat += 1
                        
            if lista[i][j] != "x":
                lista[i][j] = str(miinat)
                
            miinat = 0
    

def paljasta_tyhjat_ruudut(piilo_lista, nakyva_lista, ax, ay):
    """
    Muokattu tulvatäyttö-funktio. koska käsitellään listaa, jossa alkiot ovat tiedossa, eli on merkattu turvalliseksi,
    täytyy muokata vain pelaajalle näkyvää listaa.
    """
    
    lista = [(ay, ax)]
    
    while lista != []:
        #Otetaan listasta ulos yksi koordinaattipari käsiteltäväksi (huom. se poistetaan listasta) - tähän on olemassa oma listametodinsa.
        y = lista[len(lista) - 1][0]
        x = lista[len(lista) - 1][1]
        lista.pop(len(lista) - 1)
        #Merkitään se turvalliseksi, eli merkitään planeettaan siihen kohtaan "0"
        nakyva_lista[y][x] = "0"
        #Käydään vuorotellen läpi kaikki viereiset ruudut (8 kpl) (huomioiden planeetan reunat!) (ks. viime kerran ninja-tehtävä)
        
        if y > 0:
            yla_rivi = piilo_lista[y - 1]
            for aa, _ in enumerate(yla_rivi):
                if x - 1 <= aa <= x + 1 and yla_rivi[aa] == "0":
                    if (y - 1, aa) not in lista and nakyva_lista[y - 1][aa] == " ":
                        lista.append((y - 1, aa))
                
                if x - 1 <= aa <= x + 1 and yla_rivi[aa] != "x" and yla_rivi[aa] != "f":
                    nakyva_lista[y - 1][aa] = piilo_lista[y - 1][aa]
    
        keski_rivi = piilo_lista[y]
        for bb, _ in enumerate(keski_rivi):
            if x - 1 <= bb <= x + 1 and keski_rivi[bb] == "0":
                if (y, bb) not in lista and nakyva_lista[y][bb] == " ":
                        lista.append((y, bb))
                        
            #jos ei ole tyhjä ruutu
            if x - 1 <= bb <= x + 1 and keski_rivi[bb] != "x" and keski_rivi[bb] != "f":
                nakyva_lista[y][bb] = piilo_lista[y][bb]
        
        
        if y < len(piilo_lista)-1:
            for cc, _ in enumerate(piilo_lista[y + 1]):
                if x - 1 <= cc <= x + 1 and piilo_lista[y + 1][cc] == "0":
                    if (y + 1, cc) not in lista and nakyva_lista[y + 1][cc] == " ":
                        lista.append((y + 1, cc))
                        
                if x - 1 <= cc <= x + 1 and piilo_lista[y + 1][cc] != "x" and piilo_lista[y + 1][cc] != "f":
                    nakyva_lista[y + 1][cc] = piilo_lista[y + 1][cc]

def kirjoita_pistetaulukko(tiedosto):
    with open(tiedosto, "a") as tied:
        pelaaja["nimi"] = str(input("Anna nimesi: "))
        tied.write("{nimi}, {paivamaara}, {tulos}, {kesto}, {x} X {y}, {miinat}, {siirrot}".format(nimi=pelaaja["nimi"], 
        paivamaara=pelaaja["paivamaara"], tulos=pelaaja["lopputulos"], kesto=pelaaja["kesto"],
        x=kentan_ominaisuudet["leveys"], y=kentan_ominaisuudet["korkeus"], miinat=kentan_ominaisuudet["miinat"],
        siirrot=pelaaja["siirrot"]) + "\n")

      
def lue_pistetaulukko(tiedosto):
    def avainfunktio(lista):
        """palauttaa moniulotteisen listan ensimmäisen alkion."""
        return int(lista[0])
    try:    
        with open(tiedosto, "r") as tied:
            lista = tied.read().splitlines()
            for i, j in enumerate(lista):
                lista[i] = j.split(",")
        print("---------PELITILASTOT---------")
        
        for i in lista:
            print("Päivämäärä: {}".format(i[1]))
            print("Pelaaja {} pelasi pelin {} kokoisella kentällä. Miinoja: {}. Siirtojen määrä: {}".format(i[0], i[4], i[5], i[6]))
            print("Pelin kesto: {} minuuttia, lopputulos {}.".format(i[3], i[2])+ "\n")
    except FileNotFoundError:
        print("Tilastoa ei olla vielä luotu! Aloita peli päävalikosta!")
    
def piirra():
    
    """
    Piirtää ikkunaan sen mukaan, missä pelitilassa ollaan.
    Erilaisia tiloja ovat:
        - Päävalikko
        - asetukset, jossa määritellään pelikentän koko
        - peli, eli ollaan miinakentällä
        - pisteet eli katsotaan pelaajien huippupisteet.
    """
    
    haravasto.tyhjaa_ikkuna()
    if tila["peli"] == "paavalikko":
        #piirretään, kun ollaan päävalikossa.
        tila["ikkunan_korkeus"] = 600
        tila["ikkunan_leveys"] = 800
        haravasto.muuta_ikkunan_koko(tila["ikkunan_leveys"], tila["ikkunan_korkeus"])
        haravasto.piirra_tausta()
        haravasto.aloita_ruutujen_piirto()
        
        haravasto.piirra_tekstia("MIINANTALLAAJA", tila["ikkunan_leveys"] / 2 - 200, 
        tila["ikkunan_korkeus"] - 125 , vari=(0, 0, 0, 255), fontti="impact", koko=40)
        
        haravasto.lisaa_piirrettava_ruutu(p_aloita.sprite, p_aloita.x, p_aloita.y)
        haravasto.lisaa_piirrettava_ruutu(p_lopeta.sprite, p_lopeta.x, p_lopeta.y)
        haravasto.lisaa_piirrettava_ruutu(p_tilasto.sprite, p_tilasto.x, p_tilasto.y)
        haravasto.piirra_ruudut()

    elif tila["peli"] == "asetukset":
        tila["ikkunan_korkeus"] = 500
        tila["ikkunan_leveys"] = 800
        haravasto.muuta_ikkunan_koko(tila["ikkunan_leveys"], tila["ikkunan_korkeus"])
        haravasto.piirra_tausta()
        haravasto.aloita_ruutujen_piirto()
        for i in a_napit:
            haravasto.lisaa_piirrettava_ruutu(i.sprite, i.x, i.y)
        haravasto.piirra_ruudut()
        
        haravasto.piirra_tekstia("ANNA RUUDUKON LEVEYS: ", 50, 
        tila["ikkunan_korkeus"] - 100 , vari=(0, 0, 0, 255), fontti="impact", koko=20)
        
        haravasto.piirra_tekstia(str(kentan_ominaisuudet["leveys"]), 400, 
        tila["ikkunan_korkeus"] - 100 , vari=(0, 0, 0, 255), fontti="impact", koko=20)
        
        haravasto.piirra_tekstia("ANNA RUUDUKON KORKEUS: ", 50, 
        tila["ikkunan_korkeus"] - 200 , vari=(0, 0, 0, 255), fontti="impact", koko=20)
        
        haravasto.piirra_tekstia(str(kentan_ominaisuudet["korkeus"]), 400, 
        tila["ikkunan_korkeus"] - 200 , vari=(0, 0, 0, 255), fontti="impact", koko=20)
        
        haravasto.piirra_tekstia("ANNA MIINOJEN LKM: ", 50, 
        tila["ikkunan_korkeus"] - 300 , vari=(0, 0, 0, 255), fontti="impact", koko=20)
        
        haravasto.piirra_tekstia(str(kentan_ominaisuudet["miinat"]), 400, 
        tila["ikkunan_korkeus"] - 300 , vari=(0, 0, 0, 255), fontti="impact", koko=20)
        
        
        
    elif tila["peli"] == "peli":
        haravasto.muuta_ikkunan_koko(tila["ikkunan_leveys"], tila["ikkunan_korkeus"])
        haravasto.piirra_tausta()
        
        haravasto.aloita_ruutujen_piirto()
        
        for numero, _ in enumerate(tila["nakyva_kentta"]):
            for numero_m, _ in enumerate(tila["nakyva_kentta"][numero]):
                if tila["nakyva_kentta"][numero][numero_m] == "x":
                    haravasto.lisaa_piirrettava_ruutu("x", 40 * numero_m, 40 * numero)
                elif tila["nakyva_kentta"][numero][numero_m] == " ":
                    haravasto.lisaa_piirrettava_ruutu(" ", 40 * numero_m, 40 * numero)
                elif tila["nakyva_kentta"][numero][numero_m] == "f":
                    haravasto.lisaa_piirrettava_ruutu("f", 40 * numero_m, 40 * numero)
                for i in range(0, 9):
                    if tila["nakyva_kentta"][numero][numero_m] == "{}".format(i):
                        haravasto.lisaa_piirrettava_ruutu("{}".format(i), 40 * numero_m, 40 * numero)
        haravasto.piirra_ruudut()
        
        
        if tila["havitty"] == True:
            haravasto.piirra_tekstia("Voi ei! Astuit miinaan.", 50, 
            tila["ikkunan_korkeus"] / 2, vari=(0, 0, 0, 255), fontti="impact", koko=40)
            haravasto.piirra_tekstia("Paina \"Esc\" - näppäintä poistuaksesi asetusruutuun.", 50, 
            tila["ikkunan_korkeus"] / 2 - 50, vari=(0, 155, 0, 255), fontti="impact", koko=20)
            
            haravasto.piirra_tekstia("Paina \"Enter\" - näppäintä, jos haluat katsoa tilastoja.", 50, 
            tila["ikkunan_korkeus"] / 2 - 100, vari=(0, 75, 75, 255), fontti="impact", koko=20)
        
        if tila["voitettu"] == True:
            haravasto.piirra_tekstia("Onneksi olkoon! Kenttä on nyt turvallinen!", 50, 
            tila["ikkunan_korkeus"] / 2, vari=(0, 125, 0, 255), fontti="impact", koko=20)
            
            haravasto.piirra_tekstia("Paina \"Esc\" - näppäintä poistuaksesi asetusruutuun.", 50, 
            tila["ikkunan_korkeus"] / 2 - 50, vari=(0, 155, 0, 255), fontti="impact", koko=20)
            
            haravasto.piirra_tekstia("Paina \"Enter\" - näppäintä, jos haluat katsoa tilastoja.", 50, 
            tila["ikkunan_korkeus"] / 2 - 100, vari=(0, 75, 75, 255), fontti="impact", koko=20)
        
    elif tila["peli"] == "pisteet":
        tila["ikkunan_korkeus"] = 400
        tila["ikkunan_leveys"] = 600
        haravasto.muuta_ikkunan_koko(tila["ikkunan_leveys"], tila["ikkunan_korkeus"])
        haravasto.piirra_tausta()            
        haravasto.piirra_tekstia("Tilastot näkyvät konsolista.", 50, 
        tila["ikkunan_korkeus"] - 50 , vari=(0, 0, 0, 255), fontti="impact", koko=20)
        haravasto.piirra_tekstia("Palaa takaisin painamalla\"Esc\"-näppäintä.", 50, 
        tila["ikkunan_korkeus"] - 100 , vari=(0, 0, 0, 255), fontti="impact", koko=15)
        haravasto.piirra_tekstia("Vaihtoehtoisesti palaa takaisin painikkeella.", 50, 
        tila["ikkunan_korkeus"] - 250 , vari=(0, 0, 0, 255), fontti="impact", koko=15)
        haravasto.aloita_ruutujen_piirto()
        haravasto.lisaa_piirrettava_ruutu("takaisin", p_takaisin.x, p_takaisin.y)
        haravasto.piirra_ruudut()
        
#hiiren käsittelijä päävalikossa, pelissä ja pistetaulukossa

def kasittele_hiiri(x, y, nappi, muok):
    """
    päävalikon hiiren käsittelijäfunktio.
    """
    if tila["peli"] == "paavalikko":
        #jos painetaan nappia "aloita"
        p_aloita.testaa_sijainti(x, y)
        if p_aloita.painettu == True:
            tila["peli"] = "asetukset"
            p_aloita.painettu = False
        #jos painetaan nappia "lopeta"
        p_lopeta.testaa_sijainti(x, y)
        if p_lopeta.painettu == True:
            p_lopeta.painettu = False
            haravasto.lopeta()
        
        p_tilasto.testaa_sijainti(x, y)
        if p_tilasto.painettu == True:
            tila["peli"] = "pisteet"
            lue_pistetaulukko("pisteet.txt")
            p_tilasto.painettu = False
            
    
    elif tila["peli"] == "peli":
        """
        käsitellään hiiri silloin, kun ollaan pelitilassa eli miinakentällä.
        """
        #sovitetaan hiiren klikkaukset niin että ne voidaan sijoittaa listaan
        lattia_x = math.floor(x / 40)
        lattia_y = math.floor(y / 40)
        
        vapaat = (kentan_ominaisuudet["leveys"] * kentan_ominaisuudet["korkeus"]) - kentan_ominaisuudet["miinat"]
        
        if tila["havitty"] != True and tila["voitettu"] != True:
            if nappi == mouse.LEFT:
                if lattia_y < len(tila["nakyva_kentta"]):
                    if tila["nakyva_kentta"][lattia_y][lattia_x] != "f":
                              
                        tila["nakyva_kentta"][lattia_y][lattia_x] = tila["piilo_kentta"][lattia_y][lattia_x]
                        pelaaja["siirrot"] += 1
                        if tila["piilo_kentta"][lattia_y][lattia_x] == "0":
                            paljasta_tyhjat_ruudut(tila["piilo_kentta"], tila["nakyva_kentta"], lattia_x, lattia_y)
                            
                        for ind, _ in enumerate(tila["nakyva_kentta"]):
                            for ind_i, i in enumerate(tila["nakyva_kentta"][ind]):
                                if tila["nakyva_kentta"][ind][ind_i] != " " and tila["nakyva_kentta"][ind][ind_i] != "f" and tila["nakyva_kentta"][ind][ind_i] != "x":
                                    vapaat -= 1
                                    
                        
                        if vapaat == 0:
                            tila["voitettu"] = True
                            kello["loppu"] = time.monotonic()
                            pelaaja["kesto"] = round((kello["loppu"] - kello["alku"]) / 60)
                            pelaaja["lopputulos"] = "voitto"
                            
                            
                    if tila["nakyva_kentta"][lattia_y][lattia_x] == "x":
                        tila["havitty"] = True
                        kello["loppu"] = time.monotonic()
                        pelaaja["kesto"] = round((kello["loppu"] - kello["alku"]) / 60)
                        pelaaja["lopputulos"] = "häviö"
                
            if nappi == mouse.RIGHT:
                if tila["nakyva_kentta"][lattia_y][lattia_x] == " ":
                    tila["nakyva_kentta"][lattia_y][lattia_x] = "f"
                
                elif tila["nakyva_kentta"][lattia_y][lattia_x] == "f":
                    tila["nakyva_kentta"][lattia_y][lattia_x] = " "

    
    elif tila["peli"] == "asetukset":
        #silmukka jolla testataan kaikkien nappien kollisio
        for j in a_napit:
            j.testaa_sijainti(x, y)
        
        if a_ruud_leveys.painettu == True:
            kentan_ominaisuudet["leveys"] = str(kentan_ominaisuudet["leveys"])
            a_ruud_korkeus.painettu = False
            a_ruud_miinat.painettu = False
        else:
            if kentan_ominaisuudet["leveys"] != "" and kentan_ominaisuudet["leveys"] != "0":
                kentan_ominaisuudet["leveys"] = int(kentan_ominaisuudet["leveys"])
            else: kentan_ominaisuudet["leveys"] = 20
       
        if a_ruud_korkeus.painettu == True:
            kentan_ominaisuudet["korkeus"] = str(kentan_ominaisuudet["korkeus"])
            a_ruud_leveys.painettu = False
            a_ruud_miinat.painettu = False  
        else:
            if kentan_ominaisuudet["korkeus"] != "" and kentan_ominaisuudet["korkeus"] != "0":
                kentan_ominaisuudet["korkeus"] = int(kentan_ominaisuudet["korkeus"])
            else: 
                kentan_ominaisuudet["korkeus"] = 20
        

        if a_ruud_miinat.painettu == True:
            kentan_ominaisuudet["miinat"] = str(kentan_ominaisuudet["miinat"])
            a_ruud_leveys.painettu = False
            a_ruud_korkeus.painettu = False
        else:
            if kentan_ominaisuudet["miinat"] != "":
                kentan_ominaisuudet["miinat"] = int(kentan_ominaisuudet["miinat"])
            else:
                kentan_ominaisuudet["miinat"] = 10
                       
        if a_takaisin.painettu == True:
            tila["peli"] = "paavalikko"
            a_takaisin.painettu = False
              
        
        if a_valmis.painettu == True:
            a_valmis.painettu = False
            
            #jos painetaan nappia "valmis"
            for rivi in range(kentan_ominaisuudet["korkeus"]):
                tila["nakyva_kentta"].append([])
                tila["piilo_kentta"].append([])
                for sarake in range(kentan_ominaisuudet["leveys"]):
                    tila["nakyva_kentta"][-1].append(" ")
                    tila["piilo_kentta"][-1].append(" ")
            
            #luodaan vapaiden ruutujen lista miinoitusta varten
            for x in range(kentan_ominaisuudet["leveys"]):
                for y in range(kentan_ominaisuudet["korkeus"]):
                    kentan_ominaisuudet["vapaat"].append((x, y))
            
            miinoita(tila["piilo_kentta"], kentan_ominaisuudet["vapaat"], kentan_ominaisuudet["miinat"])
            numeroi(tila["piilo_kentta"])
            tila["ikkunan_korkeus"] = kentan_ominaisuudet["korkeus"] * 40
            tila["ikkunan_leveys"] = kentan_ominaisuudet["leveys"] * 40
            tila["peli"] = "peli"
            
            kello["alku"] = time.monotonic()
            
            tila["havitty"] = False
            tila["voitettu"] = False
    
    elif tila["peli"] == "pisteet":
        p_takaisin.testaa_sijainti(x,y)
        if p_takaisin.painettu == True:
            tila["peli"] = "paavalikko"
            p_takaisin.painettu = False
            pelaaja["top_kymmenen"].clear()
            
            
#käsittele näppäimistö
def kasittele_nappaimisto(symboli, muokkaus):
    if tila["peli"] == "asetukset":
        if a_ruud_leveys.painettu == True:
            for ind, i in enumerate(numero_napit):
                if symboli == numero_napit[ind][0]:
                    kentan_ominaisuudet["leveys"] += numero_napit[ind][1]
            
            if symboli == key.BACKSPACE:
                kentan_ominaisuudet["leveys"] = kentan_ominaisuudet["leveys"][:-1]
                
                
                
        elif a_ruud_korkeus.painettu == True:
            for ind, i in enumerate(numero_napit):
                if symboli == numero_napit[ind][0]:
                    kentan_ominaisuudet["korkeus"] += numero_napit[ind][1]
                
            if symboli == key.BACKSPACE:
                kentan_ominaisuudet["korkeus"] = kentan_ominaisuudet["korkeus"][:-1]
                
            
        elif a_ruud_miinat.painettu == True:
            for ind, i in enumerate(numero_napit):
                if symboli == numero_napit[ind][0]:
                    kentan_ominaisuudet["miinat"] += numero_napit[ind][1]
                
            if symboli == key.BACKSPACE:
                kentan_ominaisuudet["miinat"] = kentan_ominaisuudet["miinat"][:-1]
                
    elif tila["peli"] == "peli":
        if symboli == key.ESCAPE:
            tila["peli"] = "asetukset"
            tila["nakyva_kentta"].clear()
            tila["piilo_kentta"].clear()
        if tila["havitty"] == True or tila["voitettu"] == True:
            if symboli == key.ENTER:
                pelaaja["paivamaara"] = (time.strftime("%d.%m.%Y", time.localtime()) + "  klo  " + time.strftime("%H.%M", time.localtime()))
                tila["peli"] = "pisteet"
                kirjoita_pistetaulukko("pisteet.txt")
                tila["nakyva_kentta"].clear()
                tila["piilo_kentta"].clear()
                lue_pistetaulukko("pisteet.txt")
                
    elif tila["peli"] == "pisteet":
        if symboli == key.ESCAPE:
            tila["peli"] = "paavalikko"
            pelaaja["top_kymmenen"].clear()
    

def toistuva(aika):
    pass
#käynnistä peli

if __name__ ==  "__main__":
    haravasto.luo_ikkuna()
    haravasto.lataa_kuvat("spritet")
    haravasto.aseta_piirto_kasittelija(piirra)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aseta_nappain_kasittelija(kasittele_nappaimisto)
    haravasto.aseta_toistuva_kasittelija(toistuva, toistovali=1/30)
    haravasto.aloita()
    