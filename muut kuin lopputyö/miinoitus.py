import random
import haravasto

tila = {
"kentta": []
}


def miinoita(lista, vapaa, lukum):
    """
    Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin.
    funktiokutsu on muotoa
    
    miinoita(miinoitettava lista, vapaiden ruutujen lista, miinojen lukumäärä)
    """
    y_pituus = len(lista) - 1
        
    #tehdään silmukka, joka antaa satunnaiset luvut lukum kertaa ja 
    #tarkastaa että onko alkio vapaa - listassa
    for _ in range(lukum):
        while True:
            sat_y = random.randint(0, len(lista))
            sat_x = random.randint(0, len(lista[y_pituus]))
            tupl = (sat_x, sat_y)
            if tupl not in vapaa:
                continue
            else:
                lista[sat_y][sat_x] = "x"
                vapaa.remove(tupl)
                break
        



def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for numero, _ in enumerate(tila["kentta"]):
        for numero_m, _ in enumerate(tila["kentta"][numero]):
            if tila["kentta"][numero][numero_m] == "x":
                haravasto.lisaa_piirrettava_ruutu("x", 40 * numero_m, 40 * numero)
            elif tila["kentta"][numero][numero_m] == " ":
                haravasto.lisaa_piirrettava_ruutu(" ", 40 * numero_m, 40 * numero)
            elif tila["kentta"][numero][numero_m] == "0":
                haravasto.lisaa_piirrettava_ruutu("0", 40 * numero_m, 40 * numero)
    haravasto.piirra_ruudut()
    
def main():
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(600, 400)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aloita()

if __name__ == "__main__":
    
    kentta = []
    for rivi in range(10):
        kentta.append([])
        for sarake in range(15):
            kentta[-1].append(" ")

    tila["kentta"] = kentta
    
    jaljella = []
    for x in range(15):
        for y in range(10):
            jaljella.append((x, y))
    
    miinoita(kentta, jaljella, 35)
    main()