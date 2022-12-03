def tulvataytto(plan, x, y):
    #täyttää kentän aloittaen turvallisesta ruudusta,
    #eli tarkistetaan että vieressä olevat ruudut on turvallisia.
    #ei jatka tarkistusta, jos kaikki vieressä olevat on paljastettu tai 
    #vieressä on miina.
    
    #ei saa myöskään kutsua itseään eli ei ole rekursiivinen funktio

    
    #jos aloitusruudussa ei ole miinaa, se on turvallinen ja suoritus voi alkaa
    if not plan[y][x] == "x":
        plan[y][x] = "0"
        #jokainen ruutu tarkastaa viereisen ruudun ja sitä kautta funktio etenee
        while True:
            isdone = False
            for indeksi_i, _ in enumerate(plan):
                for indeksi_j, j in enumerate(plan[indeksi_i]):
                    if j == "0":
                        #ylöspäin ja tark. reunat
                        if indeksi_i != 0:
                            if plan[indeksi_i - 1][indeksi_j] == " ":
                                plan[indeksi_i - 1][indeksi_j] = "0"
                                
                        #alaspäin ja tark. reunat
                        if indeksi_i != len(plan) - 1:
                            if plan[indeksi_i + 1][indeksi_j] == " ":
                                plan[indeksi_i + 1][indeksi_j] = "0"
                                
                        #oikealle ja tark.reunat
                        if indeksi_j != len(plan[indeksi_i]) - 1:
                            if plan[indeksi_i][indeksi_j + 1] == " ":
                                plan[indeksi_i][indeksi_j + 1] = "0"
                                
                        #vasemmalle ja tark.reunat
                        if indeksi_j != 0:
                            if plan[indeksi_i][indeksi_j - 1] == " ":
                                plan[indeksi_i][indeksi_j - 1] = "0"
            if isdone:
                break



def main():
    pass
    




planeetta = [
    [" ", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", "x", " "], 
    [" ", " ", "x", "x", " ", " ", " ", "x", " ", " ", " ", "x", " "], 
    [" ", "x", "x", " ", " ", " ", " ", "x", " ", " ", "x", "x", " "], 
    ["x", "x", "x", "x", "x", " ", " ", "x", " ", "x", " ", " ", " "], 
    ["x", "x", "x", "x", " ", " ", " ", " ", "x", " ", "x", " ", " "], 
    [" ", " ", "x", " ", " ", " ", " ", " ", " ", "x", " ", " ", " "]
]

tulvataytto(planeetta, 5, 0)
print(planeetta)