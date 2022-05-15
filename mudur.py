
from asyncio.windows_events import NULL
from hesap import hesap


class mudur():
    def __init__(self):
        pass

    def getGenelDurum(self):
        genelToGet = hesap(1)
        genelToGet


    def curEkle(self, connector, curAd, curKur):
        with connector.cursor() as cursor:
            addCur = f"""INSERT INTO currencies (curID, curKUR)
                        VALUES ("{curAd}", {curKur})"""
            cursor.execute(addCur)

        connector.commit()
        return "Para birimi ekleme islemi basarili."

    def curGuncelle(self, connector, curAd, curKur):
        with connector.cursor() as cursor:
            addCur = f"""UPDATE currencies SET curKUR = {curKur}
                        WHERE curID = "{curAd}" """
            cursor.execute(addCur)

        connector.commit()
        return "Kur guncelleme islemi basarili."

    def faizBelirle(self, connector, krediFaiz=-1, gecikmeFaiz=-1):

        with connector.cursor() as cursor:

            getLastRecord = """SELECT tarih FROM bankValues ORDER BY tarih DESC LIMIT 1"""
            cursor.execute(getLastRecord)
            getLastRecord = cursor.fetchone()

            if krediFaiz !=-1:
                updateKFaiz = f"""UPDATE bankValues SET krediFAIZ = {krediFaiz} WHERE tarih={getLastRecord[0]}"""
                cursor.execute(updateKFaiz)

            if gecikmeFaiz !=-1:
                updateGFaiz = f"""UPDATE bankValues SET gecikmeFAIZ = {gecikmeFaiz} WHERE tarih={getLastRecord[0]}"""
                cursor.execute(updateGFaiz)

        connector.commit()
        return "Faiz belirleme basarili."

    def addMusteri(self, connector, musAdSoyad, musTel, musTc, musAdres, musMail):

        with connector.cursor() as cursor:
            addMusteri = f"""INSERT INTO musteriler (musADSOYAD, musTEL, musTC, musADRES, musMAIL)
                        VALUES ("{musAdSoyad}","{musTel}","{musTc}","{musAdres}","{musMail}")"""
            cursor.execute(addMusteri)

        connector.commit()
        return "Musteri ekleme basarili."

    #incomplete
    def sistemiIlerler(self, connector):
        pass

    def islemListele(self, connector, limit=-1):
        with connector.cursor() as cursor:
            if limit==-1:
                islemCek = """SELECT * FROM islemler ORDER BY islemID DESC"""
                cursor.execute(islemCek)
                islemler = cursor.fethall()
            else:
                islemCek = f"""SELECT * FROM islemler ORDER BY islemID DESC LIMIT {limit}"""
                cursor.execute(islemCek)
                islemler = cursor.fethall()

        return islemler

    #untested
    def deadlockAnalizi(self, islemler):

        tariheGoreUniqueHesaplar = []
        tariheGoreZincirler = []
        tariheGoreIslemVektorler = []
        tarihIndex = -1
        tariheGoreDeadlocklar = []

        # Deadlock analizini yapmak için islemlerin yaptığı dairesel hareketleri bulmamız gerekiyor. Bunun için
        # islemlerin hangi hesaplar arasında gerçekleştiği bulunmalıdır ve bu bulgular ilişkilendirilerek zincirler
        # oluşturulmalıdır. Daha sonra oluşturulan zincirler incelenerek dairesel hareketler tespit edilmelidir.
        # Worst case olan en uzun zincir, (sistemdeki özgün hesap sayısı-1) işlem içereceği için bu işlem hesap
        # sayısı kadar tekrarlanır. (uniqueHesaplar bu değeri belirlemek için hesaplanır)
        for x in islemler:
            if islemler[x][2]==NULL:
                continue
            elif islemler[x][3]==NULL:
                continue
            # islemler[x][2]!=NULL and islemler[x][3]!=NULL
            else:
                
                # islemleri tarihlerine göre gruplamak için listeyi yeni bir tarihle karşılaşıldığında genişletir
                if sonKarsılasılanTarih != islemler[x][7]:
                    sonKarsılasılanTarih = islemler[x][7]
                    tariheGoreUniqueHesaplar.append([])
                    tariheGoreIslemVektorler.append([])
                    tariheGoreDeadlocklar.append([])
                    tarihIndex = tarihIndex+1
                
                # İslemin kaynak veya hedef hesabı daha önce karşılaşılmış mı? 
                # Karşılaşılmamışsa hesapları tariheGoreUniqueHesaplar'a ekle
                if not tariheGoreUniqueHesaplar[tarihIndex].count(islemler[x][2]):
                    tariheGoreUniqueHesaplar[tarihIndex].append(islemler[x][2])
                if not tariheGoreUniqueHesaplar[tarihIndex].count(islemler[x][3]):
                    tariheGoreUniqueHesaplar[tarihIndex].append(islemler[x][3])

                
                atomicIslem = [islemler[x][2], islemler[x][3]]
                if not tariheGoreIslemVektorler[tarihIndex].count(atomicIslem):
                    tariheGoreIslemVektorler[tarihIndex].append(atomicIslem)


        tariheGoreZincirler = tariheGoreIslemVektorler

        # zincir oluşturma aşaması
        for i in range((len(tariheGoreUniqueHesaplar))):
            tempZincirler = []

            # i indexindeki zincirleri bulur
            for _ in range(len(tariheGoreUniqueHesaplar[i])):
                for j in range(len(tariheGoreZincirler[i])):
                    for k in range((len(tariheGoreIslemVektorler[i]))):
                        
                        #eğer zincir dairesel hareket yapmışsa onu tarihine uygun deadlock listesine ekler
                        if tariheGoreZincirler[i][j][-1]==tariheGoreIslemVektorler[i][k][0]:
                            tempZincirler.append(tariheGoreZincirler[i][j]+(tariheGoreIslemVektorler[i][k][2]))
                            if tempZincirler[-1][0]==tempZincirler[-1][-1]:
                                tariheGoreDeadlocklar[i].append(tempZincirler.pop())

            tariheGoreZincirler[i] = tempZincirler
            
            # Dairesel hareketler incelenirken hangi zincirin hangi hesaptan başladığına göre farklı zincirler aynı
            # deadlocku temsil edebilir, deadlock sayısının doğru hesaplanabilmesi için her deadlock bir zincirle temsil
            # edilmelidir
            # Bunu sağlamak için kopya zincirlerden kurtulmalıyız

            for t in range(len(tariheGoreDeadlocklar)):
                z = 0
                while z < len(tariheGoreDeadlocklar[t])-1:
                    
                    f = z+1
                    while f < len(tariheGoreDeadlocklar[t]):
                    
                        if len(tariheGoreDeadlocklar[t][y])==len(tariheGoreDeadlocklar[t][y+1]):
                            if sorted(set(tariheGoreDeadlocklar[t][z])) == sorted(set(tariheGoreDeadlocklar[t+1][f])):
                                del tariheGoreDeadlocklar[t+1][y+1]
                        f += 1
                        
                            

        # tariheGoreDeadlocklar is a list of list
        return tariheGoreDeadlocklar
