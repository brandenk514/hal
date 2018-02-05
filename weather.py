import forecastio
import os
import formatter as f
import location
import datetime
from datetime import timedelta
from pytz import timezone
import pytz


# A class that gets the weather for Dark Sky's API and a the python-forecast.io package

class Weather:
    def __init__(self):
        """
        Constructs a weather object with the disclaimer from Dark Sky
        """
        self.disclaimer = "Powered by Dark Sky - https://darksky.net/poweredby/"
        self.location = location.Location()
        self.formatter = f.Formatter()

    def get_weather_data(self, lat_lng_tuple, **keyword_parameters):
        """
        :param lat_lng_tuple: (Latitude, Longitude)
        :return: A forcastioDataBlock with a location's weather
        """
        if 'date_offset' in keyword_parameters:
            date_offset = keyword_parameters['date_offset']
        else:
            date_offset = 0
        current_tz_id = self.location.parse_timezone(self.location.get_timezone(lat_lng_tuple))
        utc = pytz.utc
        utc_dt = utc.localize(datetime.datetime.utcnow())
        current_timezone = timezone(current_tz_id)
        current_dt = current_timezone.normalize(utc_dt.astimezone(current_timezone))

        requested_date = current_dt + timedelta(days=date_offset)
        forecast = forecastio.load_forecast(os.environ.get('DARK_SKY_API_KEY'), lat_lng_tuple[0], lat_lng_tuple[1],
                                            time=requested_date, units="us")
        return forecast

    def get_current_temperature(self, weather_data: forecastio):
        """
        :param weather_data:
        :return: the weather temperature for the current weather in a JSON request
        """
        return int(round(weather_data.currently().temperature, 0))

    def get_high_temperature(self, weather_data: forecastio):
        max_temp = 0
        for data in weather_data.daily().data:
            max_temp = data.d["temperatureMax"]
        return int(round(max_temp, 0))

    def get_low_temperature(self, weather_data: forecastio):
        min_temp = 0
        for data in weather_data.daily().data:
            min_temp = data.d["temperatureMin"]
        return int(round(min_temp, 0))

    def get_forecast(self, weather_data, **keyword_parameters):
        forecast_type = ""
        if 'type' in keyword_parameters:
            forecast_type = keyword_parameters['type']
        if forecast_type == 'minutely':
            return weather_data.minutely().summary
        elif forecast_type == 'hourly':
            return weather_data.hourly().summary
        elif forecast_type == 'daily':
            return weather_data.daily().summary
        elif forecast_type == 'currently':
            return weather_data.currently().summary
        else:
            return "Forecast not specified"


if __name__ == '__main__':
    loc = location.Location()
    l = loc.get_location("Laurel, MD")
    lat = loc.parse_location_for_coordinates(l)
    weather = Weather()
    w = weather.get_weather_data(lat)
    print(w.currently())
