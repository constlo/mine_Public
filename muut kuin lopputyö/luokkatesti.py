class Nappi():

    def __init__(self,x,y,leveys,korkeus,sprite):
        self.x = x
        self.y = y
        self.leveys = leveys
        self.korkeus = korkeus
        self.sprite = sprite
        self.oikea_reuna = x + leveys
        self.yla_reuna = y + korkeus
        self.painettu = False
        
    def testaa_painike(self, koordx, koordy):
        """
        Tällä funktiolla katsotaan, onko klikkaus tai sijainti napin päällä.
        """
        if (self.x <= koordx <= self.oikea_reuna and
            self.y <= koordy <= self.yla_reuna):
            painettu = True
    
    

aloita = Nappi(200, 300, 50, 50, "tämä.png")

print(aloita.yla_reuna)
print(aloita.painettu)

aloita.testaa_painike(250, 200)