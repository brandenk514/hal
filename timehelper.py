import datetime


# A Class to aid in time related decision by HAL

class TimeHelper:
    def __init__(self):
        """
        Constructs a timehelper object with the current time and date
        """
        self.currentTime = datetime.datetime.now().time()
        self.today = datetime.datetime.now().date()

    def get_today(self):
        """
        Returns the date
        :return:
        """
        return self.today

    def get_time(self):
        """
        Return the time
        :return:
        """
        return self.currentTime

    def is_morning(self):
        """
        Tests to see if it is morning
        :return:
        """
        am = datetime.time(6)
        noon = datetime.time(12)
        if am < self.currentTime < noon:
            return True
        else:
            return False

    def is_afternoon(self):
        """
        Tests to see if it is afternoon
        :return:
        """
        noon = datetime.time(12)
        pm = datetime.time(18)
        if noon < self.currentTime < pm:
            return True
        else:
            return False

    def is_evening(self):
        """
        Tests to see if it is evening
        :return:
        """
        pm = datetime.time(18)
        if pm < self.currentTime and not self.is_late_night():
            return True
        else:
            return False

    def is_late_night(self):
        """
        Tests to see if it is night
        :return:
        """
        midnight = datetime.time(0)
        am = datetime.time(6)
        if midnight < self.currentTime < am:
            return True
        else:
            return False
