def tulvataytto(plan, x, y):
    """
    Merkitsee planeetalla olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """
    
    
    u_lista = [(x, y)]
    
    
    if plan[y][x] != "x":
        for _ in range(1500):
            
            viim = len(u_lista) - 1
            curr_x = u_lista[viim][0]
            curr_y = u_lista[viim][1]
            u_lista.pop(viim)
            vasen = curr_x - 1
            keski = curr_x
            oikea = curr_x + 1
            yla = curr_y - 1
            ala = curr_y + 1
            
            plan[curr_y][curr_x] = "0"
            #apua: [].index(), leikkaus, esim. lista[5:8]
            #katsotaan viereiset ruudut ja lisätään tuntemattomat listaan
            #määritellään jokainen viereinen ruutu erikseen ja sitä kautta ehtorakenteella lisätään alkio listaan
            #pisteet:
            
            if curr_y > 0:
                if curr_x > 0:
                    yla_v = plan[yla][vasen]
                    if yla_v == " ":
                        plan[yla][vasen] = "0"
                        if (vasen, yla) not in u_lista:
                            u_lista.append((vasen, yla))
                    
                yla_k = plan[yla][keski]
                if yla_k == " ":
                    if (keski, yla) not in u_lista:
                        u_lista.append((keski, yla))
                
                
                if curr_x < len(plan[curr_y]) - 1:
                    yla_o = plan[yla][oikea]
                    if yla_o == " ":
                        plan[yla][oikea] = "0"
                        if (oikea, yla) not in u_lista:
                            u_lista.append((oikea,yla))
                    
            if curr_x > 0:
                k_riv_vas = plan[curr_y][vasen]
                if k_riv_vas == " ":
                    plan[curr_y][vasen] = "0"
                    if (vasen, curr_y) not in u_lista:
                        u_lista.append((vasen, curr_y))
            
            if curr_x < len(plan[curr_y]) - 1:
                k_riv_oik = plan[curr_y][oikea]
                if k_riv_oik == " ":
                    plan[curr_y][oikea] = "0"
                    if (oikea, curr_y) not in u_lista:
                        u_lista.append((oikea, curr_y))
            
            if curr_y < len(plan) - 1:
                if curr_x > 0:
                    alav = plan[ala][vasen]
                    if alav == " ":
                        plan[ala][vasen] = "0"
                        if (vasen, ala) not in u_lista:
                            u_lista.append((vasen, ala))
                    
                alak = plan[ala][keski]
                if alak == " ":
                    plan[ala][keski] = "0"
                    if (keski, ala) not in u_lista:
                        u_lista.append((keski, ala))
                
                if curr_x < len(plan[curr_y]) - 1:
                    alao = plan[ala][oikea]
                    if alao == " ":
                        plan[ala][oikea] = "0"
                        if (oikea, ala) not in u_lista:
                            u_lista.append((oikea, ala))
            print(u_lista)
            if u_lista == []:
                break
        
planeetta = [
    [" ", " ", " ", "x", " ", " ", " ", " ", " ", " ", " ", "x", " "], 
    [" ", " ", "x", "x", " ", " ", " ", "x", " ", " ", " ", "x", " "], 
    [" ", "x", "x", " ", " ", " ", " ", "x", " ", " ", "x", "x", " "], 
    ["x", "x", "x", "x", "x", " ", " ", "x", " ", "x", " ", " ", " "], 
    ["x", "x", "x", "x", " ", " ", " ", " ", "x", " ", "x", " ", " "], 
    [" ", " ", "x", " ", " ", " ", " ", " ", " ", "x", " ", " ", " "]
]

tulvataytto(planeetta, 5, 2)
print(planeetta)
