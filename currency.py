class currency():
    def __init__(self, curIDcopy):
        self.curID = curIDcopy

    def getCurKur(self, connector):
        with connector.cursor() as cursor:
            getCurKuru = f"""SELECT curKur FROM currencies WHERE curID={self.curID}"""
            cursor.execute(getCurKuru)
            kaynakKurType = cursor.fetchone()
            return kaynakKurType[0]