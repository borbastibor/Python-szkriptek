import sqlite3
import datetime

#############################
# Függvény a menü kiírására #
#############################
def printMenu():
    print("\n1 - Üres adatbázis létrehozása")
    print("2 - Adatbázis létrehozása üres táblákkal")
    print("3 - Adatbázis létrehozása tesztadatokkal")
    print("4 - A munkak tábla rekordjainak a kiíratása")
    print("5 - Egyéni SQL lekérdezések végrehajtása")
    print("q - Kilépés")

#######################################
# Függvény az adatbázis létrehozására #
#######################################
def createDataBase():
    print("\nAdatbázis létrehozása...", end="")
    con = sqlite3.connect(datetime.datetime.now().strftime("%Y%m%d_%Hh%Mm%Ss") + "_munkabeosztas.db")
    print("Ok")
    return con

################################
# Függvény a táblák eldobására #
################################
def dropTables(cursor):
    # munkak tábla eldobása
    print("munkak tábla eldobása...", end="")
    cursor.execute("DROP TABLE IF EXISTS munkak")
    print("Ok")
    # dolgozok tábla eldobása
    print("dolgozok tábla eldobása...", end="")
    cursor.execute("DROP TABLE IF EXISTS dolgozok")
    print("Ok")
    # kocsik tábla eldobása
    print("kocsik tábla eldobása...", end="")
    cursor.execute("DROP TABLE IF EXISTS kocsik")
    print("Ok")

#########################################
# Függvény az üres táblák létrehozására #
#########################################
def createTables(cursor):
    # kocsik tábla létrehozása
    print("kocsik tábla létrehozása...", end="")
    cursor.execute("CREATE TABLE IF NOT EXISTS kocsik (" + 
                   "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT," +
                   "tipus TEXT NOT NULL," +
                   "rendszam TEXT NOT NULL)")
    print("Ok")
    # dolgozok tábla létrehozása
    print("dolgozok tábla létrehozása...", end="")
    cursor.execute("CREATE TABLE IF NOT EXISTS dolgozok (" +
                   "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT," +
                   "csaladnev TEXT NOT NULL," +
                   "keresztnev TEXT NOT NULL)")
    print("Ok")
    # munkak tábla létrehozása
    print("munkak tábla létrehozása...", end="")
    cursor.execute("CREATE TABLE IF NOT EXISTS munkak (" +
                   "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT," +
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
    print("dolgozok tábla feltöltése...",end="")
    cursor.execute('INSERT INTO dolgozok(csaladnev,keresztnev) VALUES' +
                   '("Mekk","Elek"),("Mézga","Géza"),("Maci","Laci"),' +
                   '("Tapsi","Hapsi"),("Gyalog","Kakukk"),("Tell","Vilmos"),' +
                   '("Móka","Miki"),("Hunyadi","Mátyás"),("Mézga","Aladár"),' +
                   '("Rambo","John")')
    print("Ok")
    # kocsik tábla feltöltése
    print("kocsik tábla feltöltése...",end="")
    cursor.execute('INSERT INTO kocsik(tipus,rendszam) VALUES' +
                   '("Toyota Hilux","AAA-111"),("Opel Astra","ABC-123"),("Suzuki Swift","RET-342"),' +
                   '("Nissan Navara","DFG-456"),("Toyota Landcruiser","RTZ-789"),("VW Caddy","UZT-512"),' +
                   '("MB G-270","GHJ-555"),("Renault Cangoo","CVB-999"),("Suzuki Vitara","WSX-321"),' +
                   '("Dacia Logan","NMB-777")')
    print("Ok")
    # munkak tábla feltöltése
    print("munkak tábla feltöltése...",end="")
    cursor.execute('INSERT INTO munkak(datum,helyszin,leiras,utemezheto,dolgozoid,kocsiid) VALUES' +
                   '("2019-12-01","Paksi Atomerőmű","Felmérésitérkép készítés",0,1,1),' +
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
    utemezes = { "0":"Nem", "1":"Igen"}
    query = '''SELECT munkak.id,datum,helyszin,leiras,utemezheto,
    dolgozok.csaladnev,dolgozok.keresztnev,kocsik.tipus,kocsik.rendszam
    FROM munkak LEFT JOIN dolgozok ON munkak.dolgozoid = dolgozok.id
    LEFT JOIN kocsik ON munkak.kocsiid = kocsik.id'''
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

###################################################
# Függvény egyéni SQL lekérdezések végrehajtására #
###################################################
def customSQLQuery(cursor):
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

################################################
#-------------------- Main --------------------#
################################################
if __name__ == "__main__":
    conn = None
    cursor = None
    while True:
        printMenu()
        char = input("\nVálasszon: ")
        if char == 'q':
            break
        
        if char == '1':
            # üres adatbázis létrehozása
            conn = createDataBase()
            cursor = conn.cursor()
            dropTables(cursor)
            
        if char == '2':
            # adatbázis létrehozása üres táblákkal
            conn = createDataBase()
            cursor = conn.cursor()
            dropTables(cursor)
            createTables(cursor)
        
        if char == '3':
            # adatbázis létrehozása tesztadatokkal
            conn = createDataBase()
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
            # egyéni SQL lekérdezések végrehajtása
            if conn is None and cursor is None:
                print("\nNincs érvényes adatbázis!")
            else:
                customSQLQuery(cursor)

    conn.commit()
    conn.close()
########################################################
#-------------------- Program vége --------------------#
########################################################
