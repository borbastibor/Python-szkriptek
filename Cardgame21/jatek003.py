# 21 kártyajáték #
from random import *

adatok = [0,0]

kartyak = [['Makk alsó',4],['Makk felső',5],['Makk király',6],['Makk hetes',7],
           ['Makk nyolcas',8],['Makk kilences',9],['Makk tizes',10],['Makk ász',11],
           ['Zöld alsó',4],['Zöld felső',5],['Zöld király',6],['Zöld hetes',7],
           ['Zöld nyolcas',8],['Zöld kilences',9],['Zöld tizes',10],['Zöld ász',11],
           ['Tök alsó',4],['Tök felső',5],['Tök király',6],['Tök hetes',7],
           ['Tök nyolcas',8],['Tök kilences',9],['Tök tizes',10],['Tök ász',11],
           ['Piros alsó',4],['Piros felső',5],['Piros király',6],['Piros hetes',7],
           ['Piros nyolcas',8],['Piros kilences',9],['Piros tizes',10],['Piros ász',11]]

def keveres(pakli):
    shuffle(pakli)
    return pakli

def lapkeres(pszam,sszam):
    print(kartyak[sszam][0]+' ({})'.format(str(kartyak[sszam][1])))
    pszam = pszam + kartyak[sszam][1]
    if pszam > 21:
        print('Ön vesztett! pontszám: {}'.format(str(pszam)))
        pszam = 0
        sszam = 0
        keveres(kartyak)
        return sszam,pszam
        
    if pszam <= 21:
        print('Az ön pontszáma: {}'.format(str(pszam)))
        sszam += 1
        return sszam,pszam

keveres(kartyak)
while True:
    betu = input('Mit kíván tenni?: Kér lapot(l) Új kör(u) Kilép(q)')
    if betu == 'q':exit()
    if betu == 'l':
        adatok = lapkeres(adatok[1],adatok[0])
    if betu == 'u':
        adatok = [0,0]
        keveres(kartyak)
