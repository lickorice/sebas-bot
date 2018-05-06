from datetime import datetime

months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
          6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October',
          11: 'November', 12: 'December'}


class DateSerializer:
    # gets raw rawteger data of dates
    def __init__(self):
        self.raw_y = (datetime.now().year)
        self.raw_m = (datetime.now().month)
        self.raw_d = (datetime.now().day)
        self.raw_h = (datetime.now().hour)
        self.raw_mn = (datetime.now().minute)
        self.raw_s = (datetime.now().second)

    def refresh(self):
        self.raw_y = (datetime.now().year)
        self.raw_m = (datetime.now().month)
        self.raw_d = (datetime.now().day)
        self.raw_h = (datetime.now().hour)
        self.raw_mn = (datetime.now().minute)
        self.raw_s = (datetime.now().second)

    def getYear(self):
        return str(self.raw_y)

    def getMonth(self):
        return months[self.raw_m]

    def getDay(self):
        return str(self.raw_d)

    def getHour(self):
        return str(self.raw_h)

    def getMin(self):
        return str(self.raw_mn)
