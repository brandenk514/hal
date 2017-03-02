import forecastio
import os
import formatter


# A class that gets the weather for Dark Sky's API and a the python-forecast.io package

class Weather:
    def __init__(self):
        """
        Constructs a weather object with the disclaimer from Dark Sky
        """
        self.disclaimer = "Powered by Dark Sky - https://darksky.net/poweredby/"

    def get_weather_data(self, lat_lng_tuple):
        """
        :param lat_lng_tuple: (Latitude, Longitude)
        :return: A forcastioDataBlock with a location's weather
        """
        return forecastio.load_forecast(os.environ.get('DARK_SKY_API_KEY'), lat_lng_tuple[0], lat_lng_tuple[1])

    def get_current_temperature(self, weather_data: forecastio):
        """
        :param weather_data:
        :return: the weather temperature for the current weather in a JSON request
        """
        return weather_data.currently().temperature

    def get_current_conditions(self, weather_data: forecastio):
        """
        :param weather_data:
        :return: the weather summary for the current conditions in a JSON request
        """
        return weather_data.currently().summary

    def get_hourly_weather(self, weather_data: forecastio):
        """
        :param weather_data:
        :return: the weather summary for the hour in a JSON request
        """
        return weather_data.hourly().summary

    def get_minutely_weather(self, weather_data: forecastio):
        """
        :param weather_data:
        :return: the weather summary for the minute in a JSON request
        """
        return weather_data.minutely().summary

    def current_forecast(self, weather_data):
        """
        :param weather_data: a JSON weather request
        :return: string for HAL to speak and display for the current forecast
        """
        temp = self.get_current_temperature(weather_data)
        condition = formatter.Formatter().format_weather_conditions(self.get_current_conditions(weather_data))
        temp = int(round(temp, 0))
        return "It is currently " + condition + " with a temperature of " + str(temp) + " degrees"

    def minutely_forecast(self, weather_data):
        """
        :param weather_data: a JSON weather request
        :return: string for HAL to speak and display for the minutely forecast
        """
        temp = self.get_current_temperature(weather_data)
        condition = formatter.Formatter().format_weather_conditions(self.get_minutely_weather(weather_data))
        temp = int(round(temp, 0))
        return "It looks like it will be " + condition + " with a temperature of " + str(temp) + " degrees"

    def hourly_forecast(self, weather_data):
        """
        :param weather_data: a JSON weather request
        :return: string for HAL to speak and display for the hourly forecast
        """
        # temp = self.get_current_temperature(weather_data)
        condition = formatter.Formatter().format_weather_conditions(self.get_hourly_weather(weather_data))
        # temp = int(round(temp, 0))
        return "It looks like today will be " + condition
