import fdb
import time
import configparser
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


con = fdb.connect(database=database, user=user, password=password)
cur = con.cursor()

start = input("Podaj datę początkową:")
stop = input("Podaj datę końcową:")

accrual = cur.execute("SELECT IDNALICZENIA FROM \"@PZD_NALICZENIA\" WHERE DATANALICZENIA BETWEEN '%s' AND '%s' "%(start,stop))
print(accrual)

con.close()