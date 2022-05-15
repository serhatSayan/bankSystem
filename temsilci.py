from musteri import musteri
from hesap import hesap

class temsilci():
    def __init__(self, temIDcopy):
        self.temID = temIDcopy

    

    # actions of temsilci

    def musEkle(self, connector, adSoyad="", tel="", tc="", adres="", mail=""):
        with connector.cursor() as cursor:
            addMusteriBody = f"""INSERT INTO musteriler (temID"""
            addMusteriValues = f"""VALUES ({self.temID}"""
            if adSoyad!="":
                addMusteriBody = addMusteriBody + """, musADSOYAD"""
                addMusteriValues = addMusteriValues + f""",'{adSoyad}'"""

            if tel!="":
                addMusteriBody = addMusteriBody + """, musTEL"""
                addMusteriValues = addMusteriValues + f""",'{tel}'"""

            if tc!="":
                addMusteriBody = addMusteriBody + """, musTC"""
                addMusteriValues = addMusteriValues + f""",'{tc}'"""

            if adres!="":
                addMusteriBody = addMusteriBody + """, musADRES"""
                addMusteriValues = addMusteriValues + f""",'{adres}'"""

            if mail!="":
                addMusteriBody = addMusteriBody + """, musMAIL"""
                addMusteriValues = addMusteriValues + f""",'{mail}'"""

            addMusteriBody = addMusteriBody + """) """
            addMusteriValues = addMusteriValues + """)"""

            addMusteri = addMusteriBody + addMusteriValues
            
            
            
            cursor.execute(addMusteri)
        connector.commit()
        return "Musteri ekleme islemi basarili."

    def musSil(self, connector, musID):

        with connector.cursor() as cursor:

            getHesapBakiye = f"SELECT hesapID, bakiye FROM hesaplar WHERE musID={musID}"
            cursor.execute(getHesapBakiye)
            bakiyeler = cursor.fetchall()

            for i in bakiyeler:
                if i[1] != 0.0:
                    return f"Musterinin {i[0]} IDli hesabında hala bakiye bulunmaktadır."


            deleteMusteri = f"""DELETE FROM musteriler WHERE musID = {musID}"""
            cursor.execute(deleteMusteri)

            for y in bakiyeler:
                hesapToDelete = hesap(y[0])
                hesapToDelete.hesabıSil()

        connector.commit()
        return "Musteri silme basarili."

    def musEdit(self, connector, musID, adSoyad="", tel="", tc="", adres="", mail=""):
        with connector.cursor() as cursor:
            
            musteriToEdit = musteri(musID)
            return musteriToEdit.bilgiUpdate(connector, adSoyad, tel, tc, adres, mail)

    def musGenel(self, connector, musID):
        pass

    def seeTalep(self, connector):
        pass

    def talepOnayla(self, connector, talepID):
        pass

    def musIslemleri(self, connector):
        pass


    # ------ method(s) which only used in inside instenses of this class -----
    def hesapSil(self, connector, hesapID):
        
        hesapToDelete = hesap(hesapID)
        return hesapToDelete.hesabıSil(connector)