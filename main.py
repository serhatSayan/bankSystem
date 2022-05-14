from mysql.connector import connect, Error
from musteri import musteri
from mudur import mudur

try:
    #with connect(
    #    host="localhost",
    #    user="root",
    #    password="Veri123-Havanı456",
    #    database="bankaSistemi"
    #) as connection:
    #    create_database = "CREATE DATABASE bankaSistemi"
    #    with connection.cursor() as cursor:
            #cursor.execute(create_database)
    #        pass
    #    print("Bağlandı")
    connection = connect(
        host="localhost",
        user="root",
        password="Veri123-Havanı456",
        database="bankaSistemi"
    )
except Error as e:
    print(e)

musteribir = musteri(1)
#print(musteribir.paraCek(connection, 30, 1))
#print(musteribir.paraYatir(connection, 50, 1))
#print(musteribir.hesapAcTalep(connection))
#print(musteribir.hesapSilTalep(connection,6))
#print(musteribir.bilgiUpdate(connection, tel="345", tc="4567", adres="fikirtepe", mail="banka@bankmail.com"))
#print(musteribir.krediTalep(connection, 50000, 24))

mudurbir = mudur()
#print(mudurbir.curEkle(connection, "STERLIN", 18.99))
#print(mudurbir.curGuncelle(connection, "STERLIN", 19.29))
#print(mudurbir.faizBelirle(connection, krediFaiz=2.4, gecikmeFaiz=1.7))
#print(mudurbir.addMusteri(connection, "Kıraç Uzun", "4567765", "12413536", "Mersin", "kirac@gmail.com"))






def musteriOlustur():
    pass