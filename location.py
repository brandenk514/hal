import googlemaps
import os
import formatter as f
import requests
import json

# A class that using the Google API python wrapper to get json request from Google APIs


class Location:
    def __init__(self):
        """
        Constructs a location object with a google API key and an ip
        """
        self.location = googlemaps.Client(key=os.environ.get('GOOGLE_API_KEY'))
        self.ip = os.environ.get('ip')
        self.f = f.Formatter()
        self.error_message = ""

    def get_location(self, location):
        """
        :param location: a string of an address
        :return: a location JSON request
        """
        try:
            return self.location.geocode(location)
        except googlemaps.exceptions.ApiError:
            self.error_message = "geocode API Error"
        except googlemaps.exceptions.HTTPError:
            self.error_message = "geocode HTTP Error"
        except googlemaps.exceptions.Timeout:
            self.error_message = "geocode Timeout Error"
        except googlemaps.exceptions.TransportError:
            self.error_message = "geocode Transport Error"

    def get_ip(self):
        """
        Gets the lat, lng for a give IP
        :return:
        """
        try:
            r = requests.post("https://www.googleapis.com/geolocation/v1/geolocate?key=" +
                              os.environ.get('GOOGLE_API_KEY')).text
            return json.loads(r)
        except googlemaps.exceptions.ApiError:
            self.error_message = "geocode API Error"
        except googlemaps.exceptions.HTTPError:
            self.error_message = "geocode HTTP Error"
        except googlemaps.exceptions.Timeout:
            self.error_message = "geocode Timeout Error"
        except googlemaps.exceptions.TransportError:
            self.error_message = "geocode Transport Error"

    def get_location_from_coordinates(self, location_tuple):
        """
        :param location_tuple: (Latitude, Longitude)
        :return: a location JSON request
        """
        try:
            return self.location.reverse_geocode(location_tuple)
        except googlemaps.exceptions.ApiError:
            self.error_message = "reverse_geocode API Error"
        except googlemaps.exceptions.HTTPError:
            self.error_message = "reverse_geocode HTTP Error"
        except googlemaps.exceptions.Timeout:
            self.error_message = "reverse_geocode Timeout Error"
        except googlemaps.exceptions.TransportError:
            self.error_message = "reverse_geocode Transport Error"

    def get_timezone(self, location):
        """
        :param location: A JSON location request
        :return: a timezone JSON request
        """
        try:
            return self.location.timezone(location)
        except googlemaps.exceptions.ApiError:
            self.error_message = "timezone API Error"
        except googlemaps.exceptions.HTTPError:
            self.error_message = "timezone HTTP Error"
        except googlemaps.exceptions.Timeout:
            self.error_message = "timezone Timeout Error"
        except googlemaps.exceptions.TransportError:
            self.error_message = "timezone Transport Error"

    def get_elevation(self, location):
        """
        :param location: A JSON location request
        :return: a elevation JSON request
        """
        try:
            return self.location.elevation(location)
        except googlemaps.exceptions.ApiError:
            self.error_message = "elevation API Error"
        except googlemaps.exceptions.HTTPError:
            self.error_message = "elevation HTTP Error"
        except googlemaps.exceptions.Timeout:
            self.error_message = "elevation Timeout Error"
        except googlemaps.exceptions.TransportError:
            self.error_message = "elevation Transport Error"

    def get_distance_matrix(self, origin, destination):
        """
        :param origin: A location String
        :param destination: A location String
        :return: A directions JSON request
        """
        try:
            return self.location.distance_matrix(origin, destination)
        except googlemaps.exceptions.ApiError:
            self.error_message = "distance_matrix API Error"
        except googlemaps.exceptions.HTTPError:
            self.error_message = "distance_matrix HTTP Error"
        except googlemaps.exceptions.Timeout:
            self.error_message = "distance_matrix Timeout Error"
        except googlemaps.exceptions.TransportError:
            self.error_message = "distance_matrix Transport Error"

    def parse_location_for_address(self, location_list):
        """
        :param location_list: A JSON location request
        :return: the address as a string
        """
        if location_list is not None:
            return location_list[1]['formatted_address']
        else:
            self.error_message = "I could not find the address you requested"

    def parse_location_for_coordinates(self, location_list):
        """
        :param location_list: A JSON location request
        :return: a tuple (Latitude, Longitude)
        """
        if location_list is not None:
            coordinates = []
            for location in location_list:
                coordinates.append(location['geometry']['location']['lat'])  # Latitude
                coordinates.append(location['geometry']['location']['lng'])  # Longitude
            tuple_coordinates = tuple(float(c) for c in coordinates)
            return tuple_coordinates
        else:
            self.error_message = "I could not find the coordinates you requested"

    def parse_location_from_ip(self, location_list):
        if location_list is not None:
            coordinates = []
            coordinates.append(location_list['location']['lat'])  # Latitude
            coordinates.append(location_list['location']['lng'])  # Longitude
            tuple_coordinates = tuple(float(c) for c in coordinates)
            return tuple_coordinates
        else:
            self.error_message = "I could not find the coordinates you requested"

    def parse_elevation(self, elevation_list):
        """
        :param elevation_list: an elevation JSON request
        :return: elevation as a float
        """
        elevation = 0.0
        if elevation_list is not None:
            for e in elevation_list:
                elevation = e['elevation']
            return elevation
        else:
            self.error_message = "I could not find the elevation for the location you requested"

    def parse_timezone(self, timezone_dict):
        """
        :parameter timezone_dict JSON request
        :return timeZoneID as a String
        """
        if timezone_dict is not None:
            return timezone_dict['timeZoneId']
        else:
            self.error_message = "I could not find the timezone for the location you requested"

    def parse_location_for_zip(self, location_list):
        """
        :parameter location_list JSON request
        :return the zipcode as a String
        """
        zip_code = ""
        if location_list is not None:
            for l in location_list:
                zip_code = l['address_components'][7]
            code = zip_code['long_name']
            return code
        else:
            self.error_message = "I could not find the zip code for the location you requested"

    def get_timezone_offset(self, location_tuple):
        if location_tuple is not None:
            tz = self.get_timezone(location_tuple)
            return tz['rawOffset']
        else:
            self.error_message = "I could not find the timezone offset for the location you requested"

    def get_dst_offset(self, location_tuple):
        if location_tuple is not None:
            tz = self.get_timezone(location_tuple)
            return tz['dstOffset']
        else:
            self.error_message = "I could not find the dst offset for the location you requested"


if __name__ == '__main__':
    loc = Location()
    print(loc.parse_location_from_ip(loc.get_ip()))
