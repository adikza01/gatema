import sys

#check if there is either -funkce1 or -funkce2 argument, otherwise close the app
args=sys.argv
if ("-funkce1" not in args) and ("-funkce2" not in args):
    sys.exit("Platné parametry jsou -funkce1 nebo -funkce2. Ani jeden z nich nebyl při spouštění zadán.")
#loading every row in a file into the list pole_radku
pole_radku=[]
try:
    with open("D327971_fc1.i", "r", encoding="utf-8") as f:
        for radek in f.readlines():
            pole_radku.append(radek.strip())
except:
    print("Nastal problém při načítání souboru")
    sys.exit()

#extracting the rows of file between the first and last row in block from (M47, Zacatek bloku vrtani) to (M47, Konec bloku vrtani) into pole_radku, header of file into hlavicka and footer into zapati
zacatek=pole_radku.index("(M47, Zacatek bloku vrtani)")
konec=pole_radku.index("(M47, Konec bloku vrtani)")
hlavicka=pole_radku[0:zacatek]
zapati=pole_radku[konec:len(pole_radku)]
pole_radku=pole_radku[zacatek:konec]

#extracting rows that starts with X
temp=[]
zbyle_radky=[]
for radek in pole_radku:
    if radek.startswith("X"):
        temp.append(radek)
    else:
        zbyle_radky.append(radek)

#Adding the rest of header and footer from block (M47, Zacatek bloku vrtani) to (M47, Konec bloku vrtani) into hlavicka and zapati
zacatek=pole_radku.index(temp[0])
dodatek_hlavicka=zbyle_radky[0:zacatek]
dodatek_zapati=zbyle_radky[zacatek:len(zbyle_radky)]
for radek in dodatek_hlavicka:
    hlavicka.append(radek)
for radek in dodatek_zapati:
    zapati.insert(0,radek)
pole_radku=temp

#creating a dictionary with key=ID of tool(number that follows after T) and value o(list of list f X and Y dimensions)
instrukce_stroju= dict()
instrukce_stroje=[]
for radek in pole_radku:
    #if there is a set of instructions for new machine, add a list of instructions of the previous machine to the dictionary
    if "T" in radek:
        #exception for the first iteration
        if(len(instrukce_stroje)!=0):
            instrukce_stroju[id_stroje]=instrukce_stroje
            instrukce_stroje = []
        id_stroje = radek.split("T")[1]
    x=radek.split("Y")[0].replace("X","")
    y=radek.split("Y")[1].split("T")[0]
    instrukce_stroje.append([x,y])
instrukce_stroju[id_stroje]=instrukce_stroje

#getting min_x,max_x,min_y,max_y
def ziskejExtremniHodnotyXY():
    prvni_pruchod = True
    for instrukce_stroje in instrukce_stroju:
        for instrukce in instrukce_stroju[instrukce_stroje]:
            x = float(instrukce[0])
            y = float(instrukce[1])
            if prvni_pruchod:
                min_x = x
                max_x = x
                min_y = y
                max_y = y
                prvni_pruchod = False
            if (x < min_x):
                min_x = x
            elif (x > max_x):
                max_x = x
            if (y < min_y):
                min_y = y
            elif (y > max_y):
                max_y = y
    print(f"MIN_X={min_x}\nMAX_X={max_x}\nMIN_Y={min_y}\nMAX_Y={max_y}")
def pridej10():
    # Adding 10 to Y when x>50
    for instrukce_stroje in instrukce_stroju:
        for instrukce in instrukce_stroju[instrukce_stroje]:
            x = float(instrukce[0])
            y = float(instrukce[1])

            if x > 50:
                y += 10
            instrukce[1] = y

def zapisDoSouboru():
    # insert the result (ordered by tool ID) into new file cnc.txt
    serazene_klice = list(instrukce_stroju.keys())
    serazene_klice.sort()
    with open("cnc.txt", "w", encoding="utf-8") as soubor:
        for radek in hlavicka:
            soubor.write(f"{radek}\n")
        for klic in serazene_klice:
            for poradi_instrukce, instrukce in enumerate(instrukce_stroju[klic]):
                instrukce[0] = format(float(instrukce[0]), ".3f")
                instrukce[1] = format(float(instrukce[1]), ".3f")
                radek = f"X{instrukce[0]}Y{instrukce[1]}"
                if (poradi_instrukce == 0):
                    radek += f"T{klic}"
                radek += "\n"
                soubor.write(radek)
        for radek in zapati:
            soubor.write(f"{radek}\n")

#doing the stuff according to arguments
for parametr in args[1:len(args)]:
    if parametr=="-funkce1":
        ziskejExtremniHodnotyXY()
    elif parametr=="-funkce2":
        pridej10()
    else:
        print(f"{parametr} je neplatný parametr")
if "-funkce2" in args:
    zapisDoSouboru()