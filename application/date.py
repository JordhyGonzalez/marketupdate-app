from datetime import *

class dt():
    def __init__(self,month,day,year):
        self.day = day
        self.month = month
        self.year = year

    def getToday(self):
        return datetime.today()
    
    def getProperDate(self):
        return datetime(self.year,self.month,self.day)



