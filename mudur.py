
from asyncio.windows_events import NULL
from hesap import hesap


class mudur():
    def __init__(self):
        pass

    def getGenelDurum(self, connector):
        genelToGet = hesap(1)
        bakiye = genelToGet.getHesapBakiye(connector)
        gelirGider = genelToGet.getGelirGider(connector)

        return [bakiye, gelirGider[0], gelirGider[1]]


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

        # Deadlock analizini yapmak i??in islemlerin yapt?????? dairesel hareketleri bulmam??z gerekiyor. Bunun i??in
        # islemlerin hangi hesaplar aras??nda ger??ekle??ti??i bulunmal??d??r ve bu bulgular ili??kilendirilerek zincirler
        # olu??turulmal??d??r. Daha sonra olu??turulan zincirler incelenerek dairesel hareketler tespit edilmelidir.
        # Worst case olan en uzun zincir, (sistemdeki ??zg??n hesap say??s??-1) i??lem i??erece??i i??in bu i??lem hesap
        # say??s?? kadar tekrarlan??r. (uniqueHesaplar bu de??eri belirlemek i??in hesaplan??r)
        for x in islemler:
            if islemler[x][2]==NULL:
                continue
            elif islemler[x][3]==NULL:
                continue
            # islemler[x][2]!=NULL and islemler[x][3]!=NULL
            else:
                
                # islemleri tarihlerine g??re gruplamak i??in listeyi yeni bir tarihle kar????la????ld??????nda geni??letir
                if sonKars??las??lanTarih != islemler[x][7]:
                    sonKars??las??lanTarih = islemler[x][7]
                    tariheGoreUniqueHesaplar.append([])
                    tariheGoreIslemVektorler.append([])
                    tariheGoreDeadlocklar.append([])
                    tarihIndex = tarihIndex+1
                
                # ??slemin kaynak veya hedef hesab?? daha ??nce kar????la????lm???? m??? 
                # Kar????la????lmam????sa hesaplar?? tariheGoreUniqueHesaplar'a ekle
                if not tariheGoreUniqueHesaplar[tarihIndex].count(islemler[x][2]):
                    tariheGoreUniqueHesaplar[tarihIndex].append(islemler[x][2])
                if not tariheGoreUniqueHesaplar[tarihIndex].count(islemler[x][3]):
                    tariheGoreUniqueHesaplar[tarihIndex].append(islemler[x][3])

                
                atomicIslem = [islemler[x][2], islemler[x][3]]
                if not tariheGoreIslemVektorler[tarihIndex].count(atomicIslem):
                    tariheGoreIslemVektorler[tarihIndex].append(atomicIslem)


        tariheGoreZincirler = tariheGoreIslemVektorler

        # zincir olu??turma a??amas??
        for i in range((len(tariheGoreUniqueHesaplar))):
            tempZincirler = []

            # i indexindeki zincirleri bulur
            for _ in range(len(tariheGoreUniqueHesaplar[i])):
                for j in range(len(tariheGoreZincirler[i])):
                    for k in range((len(tariheGoreIslemVektorler[i]))):
                        
                        #e??er zincir dairesel hareket yapm????sa onu tarihine uygun deadlock listesine ekler
                        if tariheGoreZincirler[i][j][-1]==tariheGoreIslemVektorler[i][k][0]:
                            tempZincirler.append(tariheGoreZincirler[i][j]+(tariheGoreIslemVektorler[i][k][2]))
                            if tempZincirler[-1][0]==tempZincirler[-1][-1]:
                                tariheGoreDeadlocklar[i].append(tempZincirler.pop())

            tariheGoreZincirler[i] = tempZincirler
            
            # Dairesel hareketler incelenirken hangi zincirin hangi hesaptan ba??lad??????na g??re farkl?? zincirler ayn??
            # deadlocku temsil edebilir, deadlock say??s??n??n do??ru hesaplanabilmesi i??in her deadlock bir zincirle temsil
            # edilmelidir
            # Bunu sa??lamak i??in kopya zincirlerden kurtulmal??y??z

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
