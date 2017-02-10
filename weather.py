from noaaweather import weather


class Weather:
    def __init__(self):
        self.noaa = weather.noaa()
