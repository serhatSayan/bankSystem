
from asyncio.windows_events import NULL


class mudur():
    def __init__(self):
        pass

    def getGenelDurum(self):
        pass

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

    def deadlockAnalizi(self, islemler):
        
        for x in islemler:

            if islemler[x][2]==NULL:
                continue

            for y in range(x+1, islemler):
                if islemler[x][7]==islemler[y][7]:
                    if islemler[x][2] == islemler[y][3]:
                       if islemler[x][3] == islemler[y][2]:
                           eklenecek = [islemler[x][1], islemler[y][1]]
                           tekilDeadlocklar = tekilDeadlocklar.append(eklenecek)

        #ayrık deadlockları birleştirme
        for x in tekilDeadlocklar:
            pass

        pass
