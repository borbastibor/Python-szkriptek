#######################################################################
# MunkaBeosztasDbCreator.py                                           #
#                                                                     #
# Segédprogram a munkabeosztás weblaphoz.                             #
# Célja a weblap háttéradatbázisának a létrehozása és adatokkal       #
# történő feltöltése, kiegészítve néhány funkcióval.                  #
#                                                                     #
# Funkciók:                                                           #
#   - Üres adatbázis létrehozása                                      #
#   - Adatbázis létrehozása üres táblákkal (munkak, dolgozok, kocsik) #
#   - Adatbázis létrehozása tesztadatokkal                            #
#   - A táblák rekordjainak a kiíratása                               #
#   - Egyéni SQL lekérdezések összeállítása és futtatása              #
#   - Dump fájl készítése az adatbázisból                             #
#                                                                     #
# FONTOS!!!                                                           #
# 1. A program nem létező adatbázisokat nyit meg, hanem újat hoz      #
# létre. Adatbázis létrehozáskor a következőképpen generálódik az     #
# adatbázis fájl neve:                                                #
#   létrehozási dátum_idő(mp pontosan)_munkabeosztas.db               #
#                                                                     #
# 2. Az adatbázis autocommit beállítással működik!                    #
#                                                                     #
# 3. Adatbázis dump-nál a fájl neve a következőképpen generálódik:    #
#   létrehozási dátum_idő(mp pontosan)_dump.sql - itt a dátum és idő  #
# ugyanaz lesz, mint az adatbázisnál                                  #
#                                                                     #
# 4. Ez a program nem egy általános célú adatbázis kezelő.            #
# Kifejezetten csak a MunkaBeosztas projekthez készült, illetve       #
# k...vára ráértem munkaidőben és nem tudtam mást találni.            # 
#                                                                     #
# Borbás Tibor                                                        #
# Szolnok                                                             #
# 2019. december 16.                                                  #
#######################################################################

import sqlite3
import datetime

#############################
# Függvény a menü kiírására #
#############################
def printMenu():
    print("\n1 - Üres adatbázis létrehozása")
    print("2 - Adatbázis létrehozása üres táblákkal")
    print("3 - Adatbázis létrehozása tesztadatokkal")
    print("4 - A 'munkak' tábla rekordjainak a kiíratása")
    print("5 - A 'dolgozok' tábla rekordjainak a kiíratása")
    print("6 - A 'kocsik' tábla rekordjainak a kiíratása")
    print("7 - Egyéni SQL lekérdezések végrehajtása (fejlesztés alatt)")
    print("8 - Dump fájl készítése az adatbázisból")
    print("q - Kilépés")

#######################################################
# Függvény a megadott tábla létezésének ellenőrzésére #
#######################################################
def tableExists(cursor,tname):
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name='" + tname + "'"
    cursor.execute(query)
    if len(cursor.fetchall()) == 0:
        return False
    else:
        return True

#######################################
# Függvény az adatbázis létrehozására #
#######################################
def createDataBase():
    print("\nAdatbázis létrehozása...", end="")
    fname = datetime.datetime.now().strftime("%Y%m%d_%Hh%Mm%Ss")
    con = sqlite3.connect(fname + "_munkabeosztas.db")
    con.isolation_level = None
    print("Ok")
    return fname, con

################################
# Függvény a táblák eldobására #
################################
def dropTables(cursor):
    # munkak tábla eldobása
    print("'munkak' tábla eldobása...", end="")
    cursor.execute("DROP TABLE IF EXISTS munkak")
    print("Ok")
    # dolgozok tábla eldobása
    print("'dolgozok' tábla eldobása...", end="")
    cursor.execute("DROP TABLE IF EXISTS dolgozok")
    print("Ok")
    # kocsik tábla eldobása
    print("'kocsik' tábla eldobása...", end="")
    cursor.execute("DROP TABLE IF EXISTS kocsik")
    print("Ok")

#########################################
# Függvény az üres táblák létrehozására #
#########################################
def createTables(cursor):
    # kocsik tábla létrehozása
    print("'kocsik' tábla létrehozása...", end="")
    cursor.execute("CREATE TABLE IF NOT EXISTS kocsik (" + 
                   "kocsiid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT," +
                   "tipus TEXT NOT NULL," +
                   "rendszam TEXT NOT NULL)")
    print("Ok")
    # dolgozok tábla létrehozása
    print("'dolgozok' tábla létrehozása...", end="")
    cursor.execute("CREATE TABLE IF NOT EXISTS dolgozok (" +
                   "dolgozoid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT," +
                   "csaladnev TEXT NOT NULL," +
                   "keresztnev TEXT NOT NULL)")
    print("Ok")
    # munkak tábla létrehozása
    print("'munkak' tábla létrehozása...", end="")
    cursor.execute("CREATE TABLE IF NOT EXISTS munkak (" +
                   "munkaid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT," +
                   "datum TEXT NOT NULL," +
                   "helyszin TEXT NOT NULL," +
                   "leiras TEXT NOT NULL," +
                   "utemezheto INTEGER NOT NULL DEFAULT 1," +
                   "dolgozoid INTEGER," +
                   "kocsiid INTEGER," +
                   "FOREIGN KEY (dolgozoid) REFERENCES dolgozok(id)," +
                   "FOREIGN KEY (kocsiid) REFERENCES kocsik(id))")
    print("Ok")

#######################################################
# Függvény a táblák tesztadattal történő feltöltésére #
#######################################################
def loadTestData(cursor):
    # dolgozok tábla feltöltése
    print("'dolgozok' tábla feltöltése...",end="")
    cursor.execute('INSERT INTO dolgozok(csaladnev,keresztnev) VALUES' +
                   '("Mekk","Elek"),("Mézga","Géza"),("Maci","Laci"),' +
                   '("Tapsi","Hapsi"),("Gyalog","Kakukk"),("Tell","Vilmos"),' +
                   '("Móka","Miki"),("Hunyadi","Mátyás"),("Mézga","Aladár"),' +
                   '("Rambo","John")')
    print("Ok")
    # kocsik tábla feltöltése
    print("'kocsik' tábla feltöltése...",end="")
    cursor.execute('INSERT INTO kocsik(tipus,rendszam) VALUES' +
                   '("Toyota Hilux","AAA-111"),("Opel Astra","ABC-123"),("Suzuki Swift","RET-342"),' +
                   '("Nissan Navara","DFG-456"),("Toyota Landcruiser","RTZ-789"),("VW Caddy","UZT-512"),' +
                   '("MB G-270","GHJ-555"),("Renault Cangoo","CVB-999"),("Suzuki Vitara","WSX-321"),' +
                   '("Dacia Logan","NMB-777")')
    print("Ok")
    # munkak tábla feltöltése
    print("'munkak' tábla feltöltése...",end="")
    cursor.execute('INSERT INTO munkak(datum,helyszin,leiras,utemezheto,dolgozoid,kocsiid) VALUES' +
                   '("2019-12-01","Paksi Atomerőmű","Felmérési térkép készítés",0,1,1),' +
                   '("2019-12-23","Szakály","Elektromos hálózat felmérése",1,2,2),' +
                   '("2019-12-18","Szekszárd","Gázhálózat felmérés",1,3,3),' +
                   '("2019-12-28","Pécs","Munkaterület kitűzés",0,4,4),' +
                   '("2019-12-28","Baja","Lángos evés :)",0,5,5),' +
                   '("2019-12-19","Dunaújváros","Hankook üzem felmérése",1,6,6),' +
                   '("2019-12-27","Kukutyin","Akárminek a felmérése",1,7,7),' +
                   '("2019-12-27","Pornóapáti","Még valaminek a felmérése",0,8,8),' +
                   '("2019-12-30","Szibéria","Jegesmedve vadászat műszerlábbal",1,9,9),' +
                   '("2019-12-29","Valahol","Valamilyen felmérés sörözéssel",0,10,10)')
    print("Ok")

######################################################
# Függvény a munkak tábla rekordjainak a kiíratására #
######################################################
def printMunkak(cursor):
    if tableExists(cursor,"munkak"):
        utemezes = { "0":"Nem", "1":"Igen"}
        query = '''SELECT munkaid,datum,helyszin,leiras,utemezheto,
        csaladnev,keresztnev,tipus,rendszam
        FROM munkak LEFT JOIN dolgozok ON munkak.dolgozoid = dolgozok.dolgozoid
        LEFT JOIN kocsik ON munkak.kocsiid = kocsik.kocsiid'''
        cursor.execute(query)
        count = 0
        while True:
            r = cursor.fetchone()
            if r is None:
                break
            print("--------------------")
            print("Munka id: " + str(r[0]))
            print("Dátum: " + r[1])
            print("Helyszin: " + r[2])
            print("Leírás: " + r[3])
            print("Brigádvezető: " + r[5] + " " + r[6])
            print("Gépjármű: " + r[7] + " (" + r[8] + ")")
            print("Átütemezhető: " + utemezes[str(r[4])])
            count += 1
        print("\n" + str(count) + " db rekord")
    else:
        print("\nNem létezik 'munkak' nevű tábla az adatbázisban!")

########################################################
# Függvény a dolgozok tábla rekordjainak a kiíratására #
########################################################
def printDolgozok(cursor):
    if tableExists(cursor,"dolgozok"):
        query = '''SELECT * FROM dolgozok'''
        cursor.execute(query)
        count = 0
        while True:
            r = cursor.fetchone()
            if r is None:
                break
            print("--------------------")
            print("Dolgozó id: " + str(r[0]))
            print("Családnév: " + r[1])
            print("Keresztnév: " + r[2])
            count += 1
        print("\n" + str(count) + " db rekord")
    else:
        print("\nNem létezik 'dolgozok' nevű tábla az adatbázisban!")

########################################################
# Függvény a kocsik tábla rekordjainak a kiíratására #
########################################################
def printKocsik(cursor):
    if tableExists(cursor,"kocsik"):
        query = '''SELECT * FROM kocsik'''
        cursor.execute(query)
        count = 0
        while True:
            r = cursor.fetchone()
            if r is None:
                break
            print("--------------------")
            print("Kocsi id: " + str(r[0]))
            print("Típus: " + r[1])
            print("Rendszám: " + r[2])
            count += 1
        print("\n" + str(count) + " db rekord")
    else:
        print("\nNem létezik 'kocsik' nevű tábla az adatbázisban!")

###################################################
# Függvény egyéni SQL lekérdezések végrehajtására #
###################################################
def customSQLQuery(cursor):
    buffer = ""
    while True:
        line = input("\nSQL mondat: ")
        if line == "":
            break
        buffer += line
        if sqlite3.complete_statement(buffer):
            try:
                buffer = buffer.strip()
                cursor.execute(buffer)
                if buffer.lstrip().upper().startswith("SELECT"):
                    print(cursor.fetchall())
            except sqlite3.Error as e:
                print("\nHiba: ", e.args[0])
            buffer = ""

###########################################
# Függvény adatbázis dump fájl készítésre #
###########################################
def dumpDataBase(con,fname):
    print("\nAdatbázis dump fájl létrehozása...",end="")
    with open(fname + "dump.sql", "w", encoding="utf8") as f:
        for line in con.iterdump():
            f.write("%s\n" % line)
    print("Ok")

################################################
#-------------------- Main --------------------#
################################################
if __name__ == "__main__":
    conn = None
    cursor = None
    fname = None
    while True:
        printMenu()
        char = input("\nVálasszon: ")
        if char == 'q':
            break
        
        if char == '1':
            # üres adatbázis létrehozása
            fname, conn = createDataBase()
            cursor = conn.cursor()
            dropTables(cursor)
            
        if char == '2':
            # adatbázis létrehozása üres táblákkal
            fname, conn = createDataBase()
            cursor = conn.cursor()
            dropTables(cursor)
            createTables(cursor)
        
        if char == '3':
            # adatbázis létrehozása tesztadatokkal
            fname, conn = createDataBase()
            cursor = conn.cursor()
            dropTables(cursor)
            createTables(cursor)
            loadTestData(cursor)

        if char == '4':
            # a munkak tábla rekordjainak a kiíratása
            if conn is None and cursor is None:
                print("\nNincs érvényes adatbázis!")
            else:
                printMunkak(cursor)

        if char == '5':
            # a dolgozok tábla rekordjainak a kiíratása
            if conn is None and cursor is None:
                print("\nNincs érvényes adatbázis!")
            else:
                printDolgozok(cursor)

        if char == '6':
            # a kocsik tábla rekordjainak a kiíratása
            if conn is None and cursor is None:
                print("\nNincs érvényes adatbázis!")
            else:
                printKocsik(cursor)

        if char == '7':
            # egyéni SQL lekérdezések végrehajtása
            if conn is None and cursor is None:
                print("\nNincs érvényes adatbázis!")
            else:
                customSQLQuery(cursor)

        if char == '8':
            # adatbázis dump készítése
            if conn is None and cursor is None:
                print("\nNincs érvényes adatbázis!")
            else:
                dumpDataBase(conn,fname)

    conn.close()
########################################################
#-------------------- Program vége --------------------#
########################################################
