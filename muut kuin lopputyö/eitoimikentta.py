import haravasto
import miinoitus

tila = {
    "kentta": []
}

def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    
    tyhjaa_ikkuna (pyyhkii edellisen kierroksen grafiikat pois)
    piirra_tausta (asettaa ikkunan taustavärin)
    piirra_tekstia (kirjoittaa ruudulle tekstiä)
    aloita_ruutujen_piirto (kutsutaan ennen varsinaisen ruudukon piirtoa)
    lisaa_piirrettava_ruutu (lisää piirrettävän ruudun)
    piirra_ruudut (piirtää kaikki aloituksen jälkeen lisätyt ruudut)
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
    

def tulvataytto(plan, ax, ay):
    #luo lista joka sisältää alkiot jotka tarkistetaan.
    
    lista = [(ay, ax)]
    if plan[ay][ax] == " ":
        while lista != []:
            #Otetaan listasta ulos yksi koordinaattipari käsiteltäväksi (huom. se poistetaan listasta) - tähän on olemassa oma listametodinsa.
            y = lista[len(lista) - 1][0]
            x = lista[len(lista) - 1][1]
            lista.pop(len(lista) - 1)
            #Merkitään se turvalliseksi, eli merkitään planeettaan siihen kohtaan "0"
            plan[y][x] = "0"
            #Käydään vuorotellen läpi kaikki viereiset ruudut (8 kpl) (huomioiden planeetan reunat!) (ks. viime kerran ninja-tehtävä)
            
            if y > 0:
                yla_rivi = plan[y - 1]
                for aa, _ in enumerate(yla_rivi):
                    if x - 1 <= aa <= x + 1 and yla_rivi[aa] == " ":
                        if (y - 1, aa) not in lista:
                            lista.append((y - 1, aa))
        
            keski_rivi = plan[y]
            for bb, _ in enumerate(keski_rivi):
                if x - 1 <= bb <= x + 1 and keski_rivi[bb] == " ":
                    if (y, bb) not in lista:
                            lista.append((y, bb))
        
            if y < len(plan)-1:
                for cc, _ in enumerate(plan[y + 1]):
                    if x - 1 <= cc <= x + 1 and plan[y + 1][cc] == " ":
                        if not (y + 1, cc) in lista:
                            lista.append((y + 1, cc))
        
       

def main():
    """
    Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän.
    """

    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(520, 240)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aloita()

planeetta = [
    [" ", " ", " ", "x", " ", " ", "x", "x", " ", " ", " ", "x", " "], 
    [" ", " ", "x", "x", " ", " ", " ", "x", " ", " ", " ", "x", " "], 
    [" ", "x", "x", " ", " ", " ", " ", "x", " ", " ", "x", "x", " "], 
    ["x", "x", " ", "x", "x", " ", " ", "x", " ", "x", " ", " ", " "], 
    ["x", "x", "x", "x", " ", " ", " ", "x", "x", " ", "x", " ", " "], 
    [" ", " ", "x", " ", " ", " ", " ", " ", "x", "x", " ", " ", " "]
]

if __name__ == "__main__":
    k_plan = planeetta.reverse()
    tila["kentta"] = k_plan
    tulvataytto(planeetta, 5, 0)
    main()
