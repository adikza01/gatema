Aplikace je konzolová a pracuje s CNC souborem D327971_fc1.i. Aplikaci je možné spustit s parametry, jenž můžou nabývat dvou hodnot.

• Hodnota: -funkce1
Ke všem souřadnicím v bloku mezi (M47, Zacatek bloku vrtani) a (M47, Konec bloku vrtani) na ose Y, které mají hodnotu v X větší jak 50 přičte hodnotu 10. Výstupem je nový soubor: cnc.txt, který se vytvoří v místě spuštění scriptu. Spuštění se provede v CMD konzoli příkazem: python script.py -funkce1

• Hodnota: -funkce2
Funkce vytiskne maximální a minimální hodnotu v X a Y získanou ze všech souřadnic v bloku mezi (M47, Zacatek bloku vrtani) a (M47, Konec bloku vrtani). Výstupem jsou 4 řádky v konzoli:
o Min_X = <minimum v X>
o Max_X = <maximum v X>
o Min_Y = <minimum v Y>
o Max_Y = <maximum v Y>
Spuštění se provede v CMD konzoli příkazem: python script.py -funkce2

Obě funkce je možné spustit několikrát v jednom spuštění programu. Funkce se spouští v pořadí v jakém byly zadány do konzole. (např. při zadání příkazu: python script.py -funkce1 -funkce1 -funkce2 se provede jako první -funkce1, následně opět -funkce1 a nakonec se provede -funkce2.
