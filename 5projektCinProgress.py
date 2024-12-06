import random
import time
import copy

class Hrac:
    def __init__(hrac, meno, start_x, start_y):
        hrac.meno = meno
        hrac.x = start_x
        hrac.y = start_y
        hrac.pred_x = start_x
        hrac.pred_y = start_y
        hrac.pocet = 0
        hrac.vyhral = False  

def hracie_pole(n): #funkcia ktora vytvori hracie pole velkosti n x n
    hracie_pole = []  
    for riadok in range(n + 1): #pre kazdy riadok v rozsahu od 0 do n
        hracie_pole.append([]) #pridame novy prazdny zoznam (riadok)
        for stlpec in range(n + 1): #pre kazdy stlpec v rozsahu od 0 do n
            if riadok == 0 and stlpec == 0: #ak je to pozicia [0,0]
                hracie_pole[riadok].append(' ') #prida ' '
            elif riadok == 0: #ak sme v prvom riadku (nultom) 
                hracie_pole[riadok].append(stlpec - 1) #pridame cisla od 0 az po n - 1
            elif stlpec == 0: #ak sme v prvom stlpci (nultom)
                hracie_pole[riadok].append(riadok - 1) #pridame cisla od o az po n - 1
            else:
                hracie_pole[riadok].append('.') #pre vsetky ostatne pozicia prida bodku

    return hracie_pole #funkcia vrati hracie pole ako dvojrozmerny zoznam


def pozitivny_teleport(n,pole): #funkcia pre vytvorenie pozitivnych teleportov
    pocet_pozitivnych = n//2  #pocet pozitivnych teleportov je polovica velkosti pola zaokruhlena nadol
    pismena = ["A","B","C","D","E"] #zoznam pismen ktore oznacuju pozitivne teleporty
    pozitivny_start = []
    pozitivny_koniec = []
    
    for i in range(pocet_pozitivnych): #pre kazdy pozitivny teleport nahodne generuje zaciatocnu suradnicu 
        riadok_start = random.randint(1, n-1) #nahodna generacia ziaciatocneho teleportu
        stlpec_start = random.randint(1, n)
        while pole[riadok_start][stlpec_start] != '.': #ak je na tomto mieste pole obsadene generuje znova suradnicu pokial nebude obsadena
            riadok_start = random.randint(1, n-1)
            stlpec_start = random.randint(1, n) 
        pole[riadok_start][stlpec_start] = pismena[i] #na suradnicu pridame prislusne pismeno  
        pozitivny_start.append((riadok_start,stlpec_start))

        riadok_koniec = random.randint(riadok_start+1, n) #nahodna generacia konecneho teleportu ktory musi byt o riadok vyssie 
        stlpec_koniec = random.randint(1, n)
        while pole[riadok_koniec][stlpec_koniec] != '.': #to iste co predtym 
            riadok_koniec = random.randint(1, n-1)
            stlpec_koniec = random.randint(1, n)
        pole[riadok_koniec][stlpec_koniec] = pismena[i]
        pozitivny_koniec.append((riadok_koniec,stlpec_koniec))  
    
    return pole, pozitivny_start, pozitivny_koniec


def negativne_teleporty(n, pole): #funkcia pre vytvorenie negativnych teleportov
    pocet_negativnych = n//2 #je to vlastne to iste co pozitivne teleporty
    pismena = ["a","b","c","d","e"]
    negativny_start = []
    negativny_koniec = []
    for i in range(pocet_negativnych):
        riadok_start = random.randint(2, n)
        stlpec_start = random.randint(1, n)
        while pole[riadok_start][stlpec_start] != '.':
            riadok_start = random.randint(2, n)
            stlpec_start = random.randint(1, n) 
        pole[riadok_start][stlpec_start] = pismena[i] 
        negativny_start.append((riadok_start,stlpec_start))
        
        riadok_koniec = random.randint(1, riadok_start-1) #iba konecny negativny teleport musi byt nizsie ako zaciatocny teleport
        stlpec_koniec = random.randint(1, n)
        while pole[riadok_koniec][stlpec_koniec] != '.':
            riadok_koniec = random.randint(1, riadok_start-1)
            stlpec_koniec = random.randint(1, n)
        pole[riadok_koniec][stlpec_koniec] = pismena[i]         
        negativny_koniec.append((riadok_koniec,stlpec_koniec)) 
    
    return pole, negativny_start, negativny_koniec


def kocka(hrac): #funkcia na vytvorenie hracej kocky
    hod = random.randint(1, 6)
    sucet_hodov = hod

    while hod == 6:
        hod = random.randint(1, 6)
        sucet_hodov += hod

    hrac.pocet = sucet_hodov

def koniec(n,pole): #funkcia na vytvorenie ciela hracieho pola
    if n % 2 != 0: #ak n je neparne, cize riadky budu neparne ciel bude v dolnom pravom rohu
        pole[n][n] = '*'
        koniec = "vpravo" #v premennej koniec bude umiestena informacia kde sa nachadza ciel
    
    elif n % 2 == 0: #ak n bude parne, cize aj riadky budu tak ciel bude vlavom dolnom rohu
        pole[n][1] = '*'
        koniec = "vlavo"
    
    return koniec


def generacia_pola(n,pole): #funkcia vygeneruje hracie pole
    pole[1][1] = '+' #prida start hry
    pole, pozitivny_start, pozitivny_koniec = pozitivny_teleport(n,pole) #volame funkcie na teleporty
    pole, negativny_start, negativny_koniec = negativne_teleporty(n,pole)
    
    return pole, pozitivny_start, pozitivny_koniec, negativny_start, negativny_koniec #funkcia vrati upravene pole, ktore obsahuje teleporty a zaciatok hry


def vypis(pole,n,hraci,k): #funkcia vypise hracie pole
    print("Hracie pole:")
    for i in pole: #prechadza kazdy riadok a kazdy stlpec
        for j in i:
            print(j, end=" ") #vypise znak ktory je na tej pozicii a da medzeru medzi znakmi
        print() #po vypise vsetkych stlpcov v riadku sa posunie na novy riadok
    print("="*((n+1)*2)) #po vypise pola oddeli pole "=" ktore ma rovnaku dlzku ako pole

def lokacia(pole,hraci,k): #lokacia jedneho (zatial) hraca [x,y] ASI NAM NETRREBA FUNCKIA
    print("Pozicie hracov:")
    for j in range(k):
        print(f"Hrac c.{j+1} [{hraci[j].y - 1}, {hraci[j].x - 1}]")
    print("---")   


def pohyb(hrac, pole, n, pozitivny_start, pozitivny_koniec, negativny_start, negativny_koniec, k, pozicie):
    # Starting position of the player
    x = hrac.x
    y = hrac.y

    #VYPOCET KOLKO NAM TREBA DO KONCA
    if y % 2 != 0: #pRE NEPARNE
        dokonca = (n - x) * n + (n - y)
    else: #pre parne
        dokonca = (n - x) * n + (y - 1)
    # Loop for each dice roll
    if hrac.pocet > dokonca:
        print("Hráč hodil viac bodov, než je vzdialenosť do cieľa!")
        return pole
    for i in range(hrac.pocet):
        if x % 2 != 0:  
            y += 1
            if y > n:  
                x += 1
                y = n
        else:  
            y -= 1
            if y < 1:  
                x += 1
                y = 1

       
        if n % 2 != 0:  # Cieľ je v pravom dolnom rohu
            if x == n and y == n:
                hrac.vyhral = True
                break
        else:  # Cieľ je v ľavom dolnom rohu
            if x == n and y == 1:
                hrac.vyhral = True
                break          
    
    hrac_teleport = (x, y)
    print(f"Hrac c. {hrac.meno} sa posuva na policko: [{y - 1}, {x - 1}]")
    if pole[x][y] != "." and pole[x][y] != "*" and pole[x][y] != "+":
        # Positive teleport
        if pole[x][y].isupper():
            if hrac_teleport in pozitivny_start:
                index = pozitivny_start.index(hrac_teleport)  
                hrac_teleport = pozitivny_koniec[index]  
                x = hrac_teleport[0]
                y = hrac_teleport[1]
                print(f"Hrac c. {hrac.meno} sa cez pozitivny teleport posuva na policko: [{y - 1}, {x - 1}]")
        # Negative teleport
        elif pole[x][y].islower():
            if hrac_teleport in negativny_start:
                index = negativny_start.index(hrac_teleport) 
                hrac_teleport = negativny_koniec[index]  
                x = hrac_teleport[0]
                y = hrac_teleport[1]
                print(f"Hrac c. {hrac.meno} sa cez negativny teleport posuva na policko: [{y - 1}, {x - 1}]")
    """
    PO TYCHTO POCTOCH MAME NASLEDOVNE :
        hrac.x a hrac.y == stare pozicie hraca za ktoreho hrame
        x a y == novo vypocitane pozicie kde budeme stat vratane teleportovania

        pole - pole ktore budeme vykreslovat, max jeden hrac na policku
        pozicie - kopia pola, bude sluzit na ukladanie ak na policku bude viac hracov 
    """

    if hrac.meno in pozicie[hrac.x][hrac.y]: #ak sa nachadza hrac na mieste kde ma byt -> malo by byt vzdy true
        pozicie[hrac.x][hrac.y] = pozicie[hrac.x][hrac.y].replace(hrac.meno, "", 1) ##prvy vyskyt mena hraca v retazci vymaz - ak stoja dvaja hraci na bodke -> ".12"
        ##print(pozicie[x])

    #ACH JAJ
    najvacsie_cislo = None #ideme hladat najvacsieho hraca ktory stoji na danom policku, aby sme ho mohli vyprintovat na danom mieste
    if (len(pozicie[hrac.x][hrac.y])) > 1: ##AK JE NA DANEJ POZICII V POLI POLIZICE VIAC NEZ POVODNY ZNAK A HRAC -> SU TAM VIACERI HRACI
        for t in pozicie[hrac.x][hrac.y]:
            if t.isdigit():  # Ak je hodnota číslo
                if najvacsie_cislo is None or int(t) > int(najvacsie_cislo): #ak v premennej neni nic alebo plati podmienka 
                    najvacsie_cislo = t #NAJDEM  NAJVACSIU HODNOTU Z TYCH CO TAM SU 
        pole[hrac.x][hrac.y]  = najvacsie_cislo #Do realneho pola nastavim nech ukazuje najvacsieho hraca na predchadzaujcom policku hraca na tahu

        ##print("debug print", najvacsie_cislo)
        pole[x][y] = hrac.meno #Na novu poziciu nastavim meno hraca na tahu 
        pozicie[x][y] += hrac.meno ##DO VIRTUALNEHO POLA NA NOVEJ POZICII VOPCHAM HRACA


    else : #AK JE NA POLICKU LEN JEDEN HRAC -> VO VIRTUALNOM POLICKU BUDE POVODNY ZNAK A HRAC
        pole[hrac.x][hrac.y]  = pozicie[hrac.x][hrac.y] #Na starej pozicii v realnom poli nastav povodny znak
        pole[x][y] = hrac.meno #Na novu poziciu nastavim meno hraca na tahu 
        pozicie[x][y] += hrac.meno ##DO VIRTUALNEHO POLA NA NOVEJ POZICII VOPCHAM HRACA
        ####print("tu vkladam",pozicie[x][y])   
                                  
    hrac.x = x
    hrac.y = y  
    #print("tu som",pozicie[x][y])

    return pole
def hra():
    n = int(input(f"Zadaj parameter n (veľkosť hracieho pola): "))
    if n < 5 or n > 10:
        print("Chyba")
        return None
    k = int(input(f"Zadaj parameter k (počet hračov): "))
    if k < 1 or k > 4:
        print("Chyba")
        return None
    
    #INIT POLA CLASSOV
    end = 0
    hraci = []
    mena = ["1","2","3","4"]
    start_x = 1
    start_y = 1
    pomocne_k = mena[k-1] #k ale "k"
    for i in range(k):
        hraci.append(Hrac(mena[i], start_x, start_y))
        if (i != (k-1)): #vsetkym nastav do predch. hodnotu k, poslednemu tam nechaj hodnotu "+"
            hraci[i].pred_znak = pomocne_k
        
    #KONIEC INIT 

    pole = hracie_pole(n)  # vygeneruje maticu
    ciel = koniec(n, pole)  # vráti mi pozíciu cieľa
    pole, pozitivny_start, pozitivny_koniec, negativny_start, negativny_koniec  = generacia_pola(n, pole)  # vygeneruje teleporty a začiatok

    pozicie = copy.deepcopy(pole) #vytvorim presnu kopiu pola  
    vypis(pole, n, hraci, k)  # 1. výpis poľa
    lokacia(pole,hraci,k) # 1. vypis lokacii 


    
    # Pohyb hráča na začiatok
    #lokacia_hraca_x, lokacia_hraca_y, pole, predchadzajuci = pohyb(pole, lokacia_hraca_x, lokacia_hraca_y, n, 0, predchadzajuci, pozitivny_start, pozitivny_koniec, negativny_start, negativny_koniec)
    
    while end == 0:
        for i in range(k):
            kocka(hraci[i])  # vygeneruje náhodný výsledok kocky
            print("Hráč c.",hraci[i].meno," hodil spolu na kocke:", hraci[i].pocet, "bodov")

            # Kontrola, či hráč môže prejsť (zabezpečenie, že sa nezastaví pred cieľom)
            if ciel == "vpravo" and hraci[i].x == n and hraci[i].y + hraci[i].pocet > n:
                print(f"Hráč c. {hraci[i].meno} hodil viac bodov nez je vzdialenost do ciela!")
                vypis(pole, n, hraci,k)
                continue  # Hráč hádže znovu, ak hodil viac, než je potrebné

            if ciel == "vlavo" and hraci[i].x == n and hraci[i].y - hraci[i].pocet < 1:
                print(f"Hráč c. {hraci[i].meno} hodil viac bodov nez je vzdialenost do ciela!")
                vypis(pole, n, hraci,k)
                continue  # Hráč hádže znovu, ak hodil viac, než je potrebné

            #funckia, ktora vymaze hraca zo starej suradnice a da ho do novej 
            pole = pohyb(hraci[i], pole, n, 
            pozitivny_start, pozitivny_koniec, negativny_start, negativny_koniec, 
            k, pozicie)
            
            # Výpis hracieho poľa
            vypis(pole, n, hraci,k)
            #time.sleep(5)  

            if ciel == "vlavo" and hraci[i].x == n and hraci[i].y == 1:
                print(f"Hráč c {hraci[i].meno} VYHRAL !")
                end = 1
                break
            if ciel == "vpravo" and hraci[i].x == n and hraci[i].y == n:
                print(f"Hráč c {hraci[i].meno} VYHRAL !")
                end = 1
                break
            lokacia(pole,hraci,k)
hra()