from datetime import datetime

print('[ LOG ] : Importing date-time serializer...')

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
        self.refresh()
        return str(self.raw_y)

    def getMonth(self):
        self.refresh()
        return months[self.raw_m]

    def getDay(self):
        self.refresh()
        return str(self.raw_d)

    def getHour(self):
        self.refresh()
        return str(self.raw_h)

    def getMin(self):
        self.refresh()
        if self.raw_mn < 10:
            buffer = '0' + str(self.raw_mn)
            return buffer
        else:
            return str(self.raw_mn)

    def getSec(self):
        self.refresh()
        if self.raw_s < 10:
            buffer = '0' + str(self.raw_s)
            return buffer
        else:
            return str(self.raw_s)

    def getComplete(self):
        self.refresh()
        string = self.getHour() + ':' + self.getMin() + ':' + self.getSec()
        return string
