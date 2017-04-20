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
        print(date_offset)
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

    def set_current_forecast(self, weather_data, **keyword_parameters):
        temp = self.get_current_temperature(weather_data)
        forecast_type = ""
        if 'type' in keyword_parameters:
            forecast_type = keyword_parameters['type']
        if forecast_type == 'minutely':
            condition = self.formatter.format_weather_conditions(self.get_forecast(weather_data, type=forecast_type))
            return "It looks like it will be " + condition + " with a temperature of " + str(temp)
        elif forecast_type == 'hourly':
            condition = self.formatter.format_weather_conditions(self.get_forecast(weather_data, type=forecast_type))
            return "It looks like today will be " + condition
        elif forecast_type == 'daily':
            conditions = self.formatter.format_weather_conditions(self.get_forecast(weather_data, type=forecast_type))
            return conditions
        elif forecast_type == 'currently':
            condition = self.formatter.format_weather_conditions(self.get_forecast(weather_data, type=forecast_type))
            return "It is currently " + condition + " with a temperature of " + str(temp)
        else:
            return "Forecast not specified"

    def set_future_forecast(self, weather_data, **keyword_parameters):
        temp = self.get_current_temperature(weather_data)
        time_frame = ""
        condition = self.formatter.format_weather_conditions(self.get_forecast(weather_data, type="currently"))
        if 'time_frame' in keyword_parameters:
            time_frame = keyword_parameters['time_frame']
        if time_frame == "tomorrow":
            return "It will be " + condition + " with a temperature of " + str(temp)
        else:
            time_frame = "The future is cloudy"
        return time_frame

    def get_weather_at_location(self, location_requested, **keyword_parameters):
        """
        Gets the weather for a specific location
        :param location_requested: A location as a string
        :return: The forecast as a string
        """
        if 'date_offset' in keyword_parameters:
            date = keyword_parameters['date_offset']
        else:
            date = 0
        if location_requested != "":
            location_obj = self.location.parse_location_for_coordinates(self.location.get_location(location_requested))
            weather_obj = self.get_weather_data(location_obj, date_offset=date)
            print(weather_obj.currently())
            if date == 1:
                return "Tomorrow in " + location_requested.capitalize() + ", " + self.set_future_forecast(
                    weather_obj, time_frame="tomorrow").lower() + "°F"
            if location_obj is None:
                self.set_future_forecast(weather_obj)
            else:
                return "In " + location_requested.capitalize() + ", " + self.set_current_forecast(
                    weather_obj, type="currently").lower() + "°F"
        else:
            cur_loc_obj = self.location.parse_location_for_coordinates(self.location.get_location(
                self.location.get_current_location_from_ip()))
            weather_obj = self.get_weather_data(cur_loc_obj, date_offset=date)
            if date == 1:
                return "Tomorrow, " + self.set_future_forecast(weather_obj, time_frame="tomorrow") \
                    .lower() + "°F"
            else:
                return self.set_current_forecast(weather_obj, type="currently") + "°F"

    def weather_request(self, location_requested, classification):
        """
        Handles all weather request from user
        :param location_requested: An array of strings
        :param classification: A string from a NaiveBayesClassifier
        :return: A string of the forecast
        """
        forecast = ""
        if classification == "weather tomorrow":
            forecast = self.get_weather_at_location(location_requested, date_offset=1)
        elif classification == "weather":
            forecast = self.get_weather_at_location(location_requested)
        return forecast

if __name__ == '__main__':
    w = Weather()
    loc = location.Location()
    print(w.get_weather_at_location("San Antonio", date_offset=1))
