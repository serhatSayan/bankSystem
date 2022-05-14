
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
            cursor = connector.cursor()
            cursor.execute(bakiyeGoster)
            bakiye = cursor.fetchone()

            yeniBakiye = bakiye[0]+miktar
            bakiyeArt = f"UPDATE hesaplar SET bakiye = {yeniBakiye} WHERE hesapID = {hesapID}"
            cursor = connector.cursor()
            cursor.execute(bakiyeArt)

            tarihCek = "SELECT tarih FROM bankValues ORDER BY tarih LIMIT 1"
            cursor = connector.cursor()
            cursor.execute(tarihCek)
            tarih = cursor.fetchone()
            tarih = tarih[0]

            islemOlustur = f"""INSERT INTO islemler (islemTYPE, hedefID, tutar, hedefBAKIYE, tarih)
                            VALUES ("Para Yatırma", {hesapID}, {miktar}, {bakiye[0]}, {tarih})"""
            cursor = connector.cursor()
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
            talepOlustur = f"""INSERT INTO talepler (musID, talepTYPE, hedefID) 
                        VALUES ({self.kendiID}, "Hesap Silme", {hedefID})"""
            
            cursor.execute(talepOlustur)

        connector.commit()
        return "Hesap silme talebi olusturuldu."

    def transfer(self, connector, kaynakID, hedefID, miktar):

        
        with connector.cursor() as cursor:

            #gönderenin bakiyesinin transfer için yeterli olup olmadığını kontrol eder
            bakiyeGoster = f"SELECT bakiye FROM hesaplar WHERE hesapID={kaynakID}"
            cursor.execute(bakiyeGoster)
            bakiye = cursor.fetchone()
        
            if miktar>bakiye[0]:
                return "Bakiyeniz yetersiz"
        
            #gönderilecek miktarın alıcının hesabına etkisini hesaplar
            transferCarpani = self.kurDonustur(connector, kaynakID, hedefID)
            alıcıMiktarı = miktar*transferCarpani

            #gönderen ve alıcının bakiyelerini günceller
            gonderenYeniBakiye = bakiye[0]-miktar

            bakiyeArt = f"UPDATE hesaplar SET bakiye = {gonderenYeniBakiye} WHERE hesapID = {kaynakID}"
            cursor.execute(bakiyeArt)

          #---
            bakiyeGoster = f"SELECT bakiye FROM hesaplar WHERE hesapID={hedefID}"
            cursor.execute(bakiyeGoster)
            alıcıbakiye = cursor.fetchone()
            alıcıYeniBakiye = alıcıbakiye[0]+alıcıMiktarı

            bakiyeArt = f"UPDATE hesaplar SET bakiye = {alıcıYeniBakiye} WHERE hesapID = {hedefID}"
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

            talepOlustur = f"""INSERT INTO krediTalepleri (musID, krediMiktarı, krediVade)
                         VALUES ({self.kendiID}, {miktar}, {vade})"""
            cursor.execute(talepOlustur)

        connector.commit()
        return "Kredi talebi olusturma işlemi basarili."

    def getAylıkOzet(self, connector):
        with connector.cursor() as cursor:
            getIslemler = f"""SELECT * FROM islemler 
                            WHERE kaynakID = {self.kendiID} OR hedefID = {self.kendiID}"""
            cursor.execute(getIslemler)
            islemler = cursor.fetchall()

        #islemler is a list of tuples    
        return islemler



#--------methods which only used inside instance--------

    #gönderilen para miktarının, alıcının kurundaki miktarını bulmak için gereken değeri döndürür
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