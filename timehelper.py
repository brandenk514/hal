import datetime


# A Class to aid in time related decision by HAL

class TimeHelper:
    def __init__(self):
        self.currentTime = datetime.datetime.now().time()
        self.today = datetime.datetime.now().date()

    def get_today(self):
        return self.today

    def get_time(self):
        return self.currentTime

    def is_morning(self):
        am = datetime.time(6)
        noon = datetime.time(12)
        if am < self.currentTime < noon:
            return True
        else:
            return False

    def is_afternoon(self):
        noon = datetime.time(12)
        pm = datetime.time(18)
        if noon < self.currentTime < pm:
            return True
        else:
            return False

    def is_evening(self):
        pm = datetime.time(18)
        if pm < self.currentTime and not self.is_late_night():
            return True
        else:
            return False

    def is_late_night(self):
        midnight = datetime.time(0)
        am = datetime.time(6)
        if midnight < self.currentTime < am:
            return True
        else:
            return False
