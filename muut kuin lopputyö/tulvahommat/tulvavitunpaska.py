def tulvataytto(plan, alku_x, alku_y):
    """
    Merkitsee planeetalla olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """
    
    
    
    if plan[alku_y][alku_x] == " ":
        for _ in range(3):
            a_lista = [(alku_y, alku_x)]
            
            viim = len(a_lista) - 1
            y = a_lista[viim][0]
            x = a_lista[viim][1]
            a_lista.pop(viim)
            
            b_lista = []
            
            #listan käsittely
            
            
            
            
            #suunnat
            yla = y - 1
            ala = y + 1
            vasen = x - 1
            oikea = x + 1
            
            aa = (yla, vasen)
            ab = (yla, x)
            ac = (yla, oikea)
            
            ba = (y, vasen)
            bb = (y, oikea)
            
            ca = (ala, vasen)
            cb = (ala, x)
            cc = (ala, oikea)
            
            #viereisten ruutujen määrittely
            if y > 0:
                if x < len(plan[y]):

                    yl_o = plan[yla][oikea]
                    if yl_o == " ":
                        b_lista.append(ac)
                    
                if x > 0:
                    yl_v = plan[yla][vasen]
                    if yl_v == " ":
                        b_lista.append(aa)
                
                yl_k = plan[yla][x]
                if yl_k == " ":
                        b_lista.append(ab)
                        
            if x < len(plan[y]):
                ke_o = plan[y][oikea]
                if ke_o == " ":
                        b_lista.append(bb)
                        
            if x > 0:
                ke_v = plan[y][vasen]
                if ke_v == " ":
                        b_lista.append(ba)
                        
            if y < len(plan) - 1:
                if x < len(plan[y]):
                    al_o = plan[ala][oikea]
                    if al_o == " ":
                        b_lista.append(cc)
                        
                if x > 0:
                    al_v = plan[ala][vasen]
                    if al_v == " ":
                        b_lista.append(ca)
                        
                al_k = plan[ala][x]
                if al_k == " ":
                        b_lista.append(cb)
                
            
            for ind, i in enumerate(b_lista):
                a_lista.append(i)
                plan[i[0]][i[1]] = "0"
                print(a_lista)
                if ind == 7:
                    b_lista.clear()
            
                
        
        

        
        
        
        
    
            
planeetta = [[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "], 
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "], 
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "], 
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "], 
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "], 
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "], 
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "], 
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "], 
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "], 
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "], 
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "], 
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
]

tulvataytto(planeetta, 5, 2)
print(planeetta)
