from currency import currency
from hesap import hesap

class musteri():
    def __init__(self, musID) -> None:
        self.kendiID = musID
        pass

    def returnGenel():
        pass

    def paraCek(self, connector, miktar, hesapID):

        with connector.cursor() as cursor:
            bakiyeGoster = f"SELECT bakiye FROM hesaplar WHERE hesapID={hesapID}"
            cursor = connector.cursor()
            cursor.execute(bakiyeGoster)
            bakiye = cursor.fetchone()
        
            if miktar>bakiye[0]:
                return "Bakiyeniz yetersiz"

        
            yeniBakiye = bakiye[0]-miktar
            bakiyeDus = f"UPDATE hesaplar SET bakiye = {yeniBakiye} WHERE hesapID = {hesapID}"
            cursor = connector.cursor()
            cursor.execute(bakiyeDus)

        
            tarihCek = "SELECT tarih FROM bankValues ORDER BY tarih LIMIT 1"
            cursor = connector.cursor()
            cursor.execute(tarihCek)
            tarih = cursor.fetchone()
            tarih = tarih[0]

        
            islemOlustur = f"""INSERT INTO islemler (islemTYPE, kaynakID, tutar, kaynakBAKIYE, tarih) VALUES 
                        ("Para Cekme", {hesapID}, {miktar}, {bakiye[0]}, {tarih})"""
            cursor = connector.cursor()
            cursor.execute(islemOlustur)
            

        connector.commit()    
        return "Para cekme islemi basarili."

    def paraYatir(self, connector, miktar, hesapID):

        with connector.cursor() as cursor:

            bakiyeGoster = f"SELECT bakiye FROM hesaplar WHERE hesapID={hesapID}"
            cursor.execute(bakiyeGoster)
            bakiye = cursor.fetchone()

            yeniBakiye = bakiye[0]+miktar
            bakiyeArt = f"UPDATE hesaplar SET bakiye = {yeniBakiye} WHERE hesapID = {hesapID}"
            cursor.execute(bakiyeArt)

            tarihCek = "SELECT tarih FROM bankValues ORDER BY tarih DESC LIMIT 1"
            cursor.execute(tarihCek)
            tarih = cursor.fetchone()
            tarih = tarih[0]

            islemOlustur = f"""INSERT INTO islemler (islemTYPE, hedefID, tutar, hedefBAKIYE, tarih)
                            VALUES ("Para Yat??rma", {hesapID}, {miktar}, {bakiye[0]}, {tarih})"""
            cursor.execute(islemOlustur)

        connector.commit()    
        return "Para yatirma islemi basarili."

    #incomplete
    def krediBorcuOde(self, connector):
        
        with connector.cursor() as cursor:
            pass
        pass

    def hesapAcTalep(self, connector):

        with connector.cursor() as cursor:
            talepOlustur = f"""INSERT INTO talepler (musID, talepTYPE) 
                        VALUES ({self.kendiID}, "Hesap Acma")"""
            
            cursor = connector.cursor()
            cursor.execute(talepOlustur)

        connector.commit()
        return "Hesap acma talebi olusturuldu."

    def hesapSilTalep(self, connector, hedefID):
        
        with connector.cursor() as cursor:

            bakiyeGoster = f"SELECT bakiye FROM hesaplar WHERE hesapID={hedefID}"
            cursor.execute(bakiyeGoster)
            bakiye = cursor.fetchone()

            if bakiye != 0.0:
                return "Bu islemi gerceklestirebilmek icin bakiyenizin s??f??r(0) olmas?? gerek."

            talepOlustur = f"""INSERT INTO talepler (musID, talepTYPE, hedefID) 
                        VALUES ({self.kendiID}, "Hesap Silme", {hedefID})"""
            
            cursor.execute(talepOlustur)

        connector.commit()
        return "Hesap silme talebi olusturuldu."

    def transfer(self, connector, kaynakID, hedefID, miktar):

        
        with connector.cursor() as cursor:

            #g??nderenin bakiyesinin transfer i??in yeterli olup olmad??????n?? kontrol eder
            bakiyeGoster = f"SELECT bakiye FROM hesaplar WHERE hesapID={kaynakID}"
            cursor.execute(bakiyeGoster)
            bakiye = cursor.fetchone()
        
            if miktar>bakiye[0]:
                return "Bakiyeniz yetersiz"
        
            #g??nderilecek miktar??n al??c??n??n hesab??na etkisini hesaplar
            transferCarpani = self.kurDonustur(connector, kaynakID, hedefID)
            al??c??Miktar?? = miktar*transferCarpani

            #g??nderen ve al??c??n??n bakiyelerini g??nceller
            gonderenYeniBakiye = bakiye[0]-miktar

            bakiyeArt = f"UPDATE hesaplar SET bakiye = {gonderenYeniBakiye} WHERE hesapID = {kaynakID}"
            cursor.execute(bakiyeArt)

          #---
            bakiyeGoster = f"SELECT bakiye FROM hesaplar WHERE hesapID={hedefID}"
            cursor.execute(bakiyeGoster)
            al??c??bakiye = cursor.fetchone()
            al??c??YeniBakiye = al??c??bakiye[0]+al??c??Miktar??

            bakiyeArt = f"UPDATE hesaplar SET bakiye = {al??c??YeniBakiye} WHERE hesapID = {hedefID}"
            cursor.execute(bakiyeArt)

        connector.commit()    
        return "Transfer islemi basarili."
    
    def bilgiUpdate(self, connector, adSoyad="", tel="", tc="", adres="", mail=""):
        with connector.cursor() as cursor:

            if adSoyad != "":
                nameSurUpdate = f"UPDATE musteriler SET musADSOYAD = {adSoyad} WHERE musID = {self.kendiID}"
                cursor.execute(nameSurUpdate)
            if tel != "":
                telUpdate = f"UPDATE musteriler SET musTEL = {tel} WHERE musID = {self.kendiID}"
                cursor.execute(telUpdate)
            if tc != "":
                tcUpdate = f"UPDATE musteriler SET musTC = {tc} WHERE musID = {self.kendiID}"
                cursor.execute(tcUpdate)
            if adres != "":
                adresUpdate = f"""UPDATE musteriler SET musADRES = "{adres}" WHERE musID = {self.kendiID}"""
                cursor.execute(adresUpdate)
            if mail != "":
                mailUpdate = f"""UPDATE musteriler SET musMAIL = "{mail}" WHERE musID = {self.kendiID}"""
                cursor.execute(mailUpdate)
        
        connector.commit()    
        return "Bilgi guncelleme islemi basarili."

    def krediTalep(self, connector, miktar, vade):
        with connector.cursor() as cursor:

            talepOlustur = f"""INSERT INTO krediTalepleri (musID, krediMiktar??, krediVade)
                         VALUES ({self.kendiID}, {miktar}, {vade})"""
            cursor.execute(talepOlustur)

        connector.commit()
        return "Kredi talebi olusturma i??lemi basarili."

    def getAyl??kOzet(self, connector):
        with connector.cursor() as cursor:
            getIslemler = f"""SELECT * FROM islemler 
                            WHERE kaynakID = {self.kendiID} OR hedefID = {self.kendiID}"""
            cursor.execute(getIslemler)
            islemler = cursor.fetchall()

        #islemler is a list of tuples    
        return islemler



#--------method(s) which only used inside instance of this class--------

    #g??nderilen para miktar??n??n, al??c??n??n kurundaki miktar??n?? bulmak i??in gereken de??eri (FLOAT) d??nd??r??r
    def kurDonustur(self, connector, kaynakID, hedefID):
        with connector.cursor() as cursor:
            kaynakKurType = f"""SELECT curTYPE FROM hesaplar WHERE hesapID={kaynakID}"""
            cursor.execute(kaynakKurType)
            kaynakKurType = cursor.fetchone()
            kaynakKurType = kaynakKurType[0]
            
            kaynakKur = f"""SELECT curKUR FROM currencies WHERE curID={kaynakKurType}"""
            cursor.execute(kaynakKur)
            kaynakKur = cursor.fetchone()
            kaynakKur = kaynakKur[0]

            hedefKurType = f"""SELECT curTYPE FROM hesaplar WHERE hesapID={hedefID}"""
            cursor.execute(hedefKurType)
            hedefKurType = cursor.fetchone()
            hedefKurType = hedefKurType[0]
            
            hedefKur = f"""SELECT curKUR FROM currencies WHERE curID={hedefKurType}"""
            cursor.execute(hedefKur)
            hedefKur = cursor.fetchone()
            hedefKur = hedefKur[0]

        return kaynakKur/hedefKur

    def gelirGiderGenel(self, connector):
        gelir = 0
        gider = 0
        genel = self.getMusBakiye(connector)

        with connector.cursor() as cursor:
            tarihCek = "SELECT tarih FROM bankValues ORDER BY tarih LIMIT 1"
            cursor = connector.cursor()
            cursor.execute(tarihCek)
            tarih = cursor.fetchone()
            tarih = tarih[0]

            islemler = self.getAyl??kOzet()

            for i in islemler:
                if i[1] == "Para Yat??rma":
                    gelir = gelir + i[4]
                elif i[1] == "Para Cekme":
                    gider = gider + i[4]

        

        return  [gelir, gider, genel]

    def getMusBakiye(self, connector):
        toplamBakiye = 0
        hesaplar = self.getHesaplar(connector)
        
        for x in hesaplar:
            hesapToGet = hesap(x[0])
            curToGet = currency(hesapToGet.getHesapCur(connector))
            curCarpani = 1 / curToGet.getCurKur(connector)
            bakiye = hesapToGet.getHesapBakiye(connector)
            miktar = bakiye * curCarpani

            toplamBakiye = toplamBakiye + miktar

        return toplamBakiye

    def getHesaplar(self, connector):
        with connector.cursor() as cursor:
            getHesaplar = f"""SELECT hesapID FROM hesaplar 
                            WHERE musID = {self.kendiID}"""
            cursor.execute(getHesaplar)

            #hesaplar is a list of tuples 
            return cursor.fetchall()
   