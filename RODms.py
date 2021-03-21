import fdb
from datetime import datetime
import configparser
import time

print("Generator miesięcznych zestawien naliczeń na ROD. Wersja 1.0")
print("Copyright (C) 2021 Filip Napierała")
print("Data kompilacji 18.03.2021")
print("--------------------------------------------------------------------------------------------------------")
print("Niniejszy program jest wolnym oprogramowaniem - możesz go rozpowszechniać dalej i/lub modyfikować na warunkach Powszechnej Licencji Publicznej GNU wydanej przez Fundację Wolnego Oprogramowania, według wersji 3 tej Licencji lub dowolnej z późniejszych wersji.")
print("Niniejszy program rozpowszechniany jest z nadzieją, iż będzie on użyteczny - jednak BEZ ŻADNEJ GWARANCJI, nawet domyślnej gwarancji PRZYDATNOŚCI HANDLOWEJ albo PRZYDATNOŚCI DO OKREŚLONYCH ZASTOSOWAŃ. Bliższe informacje na ten temat można uzyskać z Powszechnej Licencji Publicznej GNU.")
print("Powszechnej Licencji Publicznej GNU powinna zostać ci dostarczona razem z tym programem")
print("--------------------------------------------------------------------------------------------------------")
print("Program powinien być uruchamiany na serwerze")
print("Proszę sprawdzić plik config.txt pod kątem zgodności danych domyślnych z tymi na Państwa Ogrodzie")

config="config.txt"
parser = configparser.ConfigParser()
parser.read('config.txt')

filepath = parser['BASIC']['filepath']
database = parser['BASIC']['database']
user = parser['BASIC']['user']
password = parser['BASIC']['password']

print("Zapis do pliku '%s'. Upewnij się, że jest pusty!"%(filepath))

#connecting to database
con = fdb.connect(database=database, user=user, password=password)
cur = con.cursor()

#opening file
f = open(filepath, "a")

# Creating list in file
L = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0]

#start = input("Podaj datę początkową w formacie RRRR-MM-DD:")
#stop = input("Podaj datę końcową w formacie RRRR-MM-DD:")
start = '2018-01-01'
stop = '2019-01-01'
headers = input("Czy drukować nagłówki? [T/n]")

#accrual = cur.execute("SELECT IDNALICZENIA FROM \"@PZD_NALICZENIA\" WHERE DATANALICZENIA BETWEEN '%s' AND '%s' "%(start,stop))
cur.execute("SELECT IDNALICZENIA FROM \"@PZD_NALICZENIA\" WHERE DATANALICZENIA BETWEEN '2018-01-01' AND '2019-01-01'")
accrual = cur.fetchall()
print("Lista ID naliczeń to:")
print(accrual)

# Translating ID to accural name using dictionary
if headers == 'T' or headers == 't':
    cur.execute("SELECT NAZWAOPLATY FROM \"@PZD_SLOOPLATY\" ")
    names = cur.fetchall()
    print("Tytuły naliczeń:")
    print(names)
else:
    print("Tworzę plik bez tytułów opłat")

#Selecting values from database and writing to variables
for h in range(len(accrual)):
    singleaccrualraw = accrual[h]
    singleaccrual = singleaccrualraw[0]
    cur.execute("SELECT KWOTA FROM \"@PZD_NALICZENIAPOZ\" WHERE IDNALICZENIA='%s' "%(singleaccrual))
    kwota = cur.fetchall()
    kwotadwa = kwota[0]
    kwotatrzy = kwotadwa[0]
    #print(kwotatrzy)
    cur.execute("SELECT IDSLOOPLATY FROM \"@PZD_NALICZENIAPOZ\" WHERE IDNALICZENIA='%s' "%(singleaccrual))
    idslooplaty = cur.fetchall()
    idslooplatydwa = idslooplaty[0]
    idslooplatytrzy = idslooplatydwa[0]
    #print(idslooplatytrzy)


    #writing to list
    if kwotatrzy != 0:
        kwotazlisty = L[int(idslooplatytrzy)]
        L[idslooplatytrzy] = kwotazlisty + kwotatrzy

now = datetime.now()
print(L)
f.write("\n")
f.write("Zestawienie naliczeń wygenerowano od:")
f.write(start)
f.write(" do:")
f.write(stop)
f.write(". Raport wygenerowano dnia:")
f.write(str(now))
f.write("\n")

#Printing headers
if headers == 'T' or headers == 't':
    for b in range(len(names)):
        f.write(str(names[b]))
        f.write(";")
        b = b + 1
f.write("\n")
#Printing data
for g in range(len(L)):
    f.write(str(L[g]))
    f.write(";")
    g=g+1
#closing file and connection
f.close()
con.close()
print("Program zakończył pracę z sukcesem. Wyłączam za 3 sekundy")
time.sleep(3)