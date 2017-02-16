import forecastio
import os
import location

class Weather:
    def __init__(self):
        self.disclaimer = "Powered by Dark Sky - https://darksky.net/poweredby/"

    def get_weather_data(self, lat_lng_tuple):
        return forecastio.load_forecast(os.environ.get('DARK_SKY_API_KEY'), lat_lng_tuple[0], lat_lng_tuple[1])

    def get_current_temperature(self, weather_data: forecastio):
        return weather_data.currently().temperature

    def get_current_conditions(self, weather_data: forecastio):
        return weather_data.currently().summary

    def get_hourly_weather(self, weather_data: forecastio):
        return weather_data.hourly().summary

    def get_minutely_weather(self, weather_data: forecastio):
        return weather_data.minutely().summary
