def tulvataytto(plan, x, y):
    """
    Merkitsee planeetalla olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """
    
    
    u_lista = [(x, y)]
    
    
    if plan[y][x] != "x":
        #while u_lista != []:
        for _ in range(10):
            viim = len(u_lista) - 1
            curr_x = u_lista[viim][0]
            curr_y = u_lista[viim][1]
            u_lista.pop(viim)
            
            plan[curr_y][curr_x] = "0"
            #apua: [].index(), leikkaus, esim. lista[5:8]
            #katsotaan viereiset ruudut ja lisätään tuntemattomat listaan
            if curr_y > 0:
                yla_rivi = plan[curr_y - 1]
                #koodi on liian hidas, koska jokaisella kierroksella se joutuu käymään läpi 100 alkiota jokaisella rivillä.
                for aa, _ in enumerate(yla_rivi):
                    if curr_x - 1 <= aa <= curr_x + 1 and yla_rivi[aa] == " ":
                        if (aa, curr_y - 1) not in(u_lista):
                            u_lista.append((aa, curr_y - 1))
                        
            keski_rivi = plan[curr_y]
            for bb, _ in enumerate(keski_rivi):
                if curr_x - 1 <= bb <= curr_x + 1 and keski_rivi[bb] == " ":
                    if (bb, curr_y) not in(u_lista):
                        u_lista.append((bb, curr_y))
                    
            if curr_y < len(plan) - 1:
                for cc, _ in enumerate(plan[curr_y + 1]):
                    if curr_x - 1 <= cc <= curr_x + 1 and plan[curr_y + 1][cc] == " ":
                        if (cc, curr_y + 1) not in(u_lista):
                            u_lista.append((cc, curr_y + 1))
                        
            print(u_lista)
            
            
planeetta = [
    [" ", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", "x", " "], 
    [" ", " ", "x", "x", " ", " ", " ", "x", " ", " ", " ", "x", " "], 
    [" ", "x", "x", " ", " ", " ", " ", "x", " ", " ", "x", "x", " "], 
    ["x", "x", "x", "x", "x", " ", " ", "x", " ", "x", " ", " ", " "], 
    ["x", "x", "x", "x", " ", " ", " ", " ", "x", " ", "x", " ", " "], 
    [" ", " ", "x", " ", " ", " ", " ", " ", " ", "x", " ", " ", " "]
]

tulvataytto(planeetta, 5, 1)
print(planeetta)