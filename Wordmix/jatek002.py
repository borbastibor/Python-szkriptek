from random import *

szotomb = []
szamok = []
szavakfile = open('szavak.txt',encoding = 'utf-8')
while True:
    egysor = szavakfile.readline().strip('\n')
    if egysor == '':break
    szotomb.append(egysor)
szavakfile.close()
sorszam = randint(0,len(szotomb)-1)
kijeloltszo = szotomb[sorszam]
sumujszo = ''
for i in range(len(kijeloltszo)):
    while True:
        szam = randint(0,len(kijeloltszo)-1)
        if szam not in szamok:
            sumujszo = sumujszo + kijeloltszo[szam]
            szamok.append(szam)
            break
print(sumujszo)
szamlalo = 1
while True:
    bekeres = input('Kérem adja meg az eredeti szót: ')
    if bekeres == kijeloltszo:
        print('Ön eltalálata a szót {} próbálkozásból!'.format(str(szamlalo)))
        break
    else:print('Nem talált!')
    szamlalo += 1
