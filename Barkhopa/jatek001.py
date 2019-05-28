from random import *

szam = randint(0,100)
szamlalo = 1
while True:
    bekertszam = input('Kérem tippeljen: ')
    if bekertszam == 'q':break
    if int(bekertszam)==szam:
        print('Ön eltalálta a számot {} próbálkozásból'.format(str(szamlalo)))
        break
    if int(bekertszam)>szam:print('A tipp nagyobb')
    if int(bekertszam)<szam:print('A tipp kisebb')
    szamlalo += 1
