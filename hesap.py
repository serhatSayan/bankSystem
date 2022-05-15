class hesap():
    def __init__(self, hesapIDcopy):
        self.hesapID = hesapIDcopy

    
    def hesabıSil(self, connector):
        with connector.cursor() as cursor:
            deleteHesap = f"""DELETE FROM hesaplar WHERE hesapID = {self.hesapID}"""
            cursor.execute(deleteHesap)

        connector.commit()
        return
        
    def getHesapBakiye(self, connector):
        with connector.cursor() as cursor:

            bakiyeGoster = f"SELECT bakiye FROM hesaplar WHERE hesapID={self.hesapID}"
            cursor = connector.cursor()
            cursor.execute(bakiyeGoster)
            bakiye = cursor.fetchone()
            
        return bakiye[0]

    def getHesapCur(self, connector):
        with connector.cursor() as cursor:

            curGoster = f"SELECT curTYPE FROM hesaplar WHERE hesapID={self.hesapID}"
            cursor.execute(curGoster)
            cur = cursor.fetchone()
            
        return cur[0]

    def getGelirGider(self, connector):
        islemler = self.getIslemler(connector)
        gelir = 0
        gider = 0

        for x in islemler:
            if x[1]=="Para Yatırma":
                gelir = gelir + x[4]
            elif x[1]=="Para Cekme":
                gider = gider + x[4]
            elif x[1] == "Transfer":
                if x[2] == self.hesapID:
                    gider = gider + x[4]
                else:
                    gelir = gelir + x[4]
            elif x[1]=="Kredi Borcu":
                gider = gider + x[4]

        return [gelir, gider]
    
    def getIslemler(self, connector):
        with connector.cursor() as cursor:

            islemGoster = f"SELECT * FROM islemler WHERE kaynakID={self.hesapID} OR hedefID={self.hesapID}"
            cursor.execute(islemGoster)
            return cursor.fetchall()