import googlemaps
import geocoder
import os


# A class that using the Google API python wrapper to get json request from Google APIs

class Location:
    def __init__(self):
        """
        Constructs a location object with a google API key and an ip
        """
        self.location = googlemaps.Client(key=os.environ.get('GOOGLE_API_KEY'))
        self.ip = os.environ.get('ip')

    def get_location(self, location):
        """
        :param location: a string of an address
        :return: a location JSON request
        """
        return self.location.geocode(location)

    def get_location_from_coordinates(self, location_tuple):
        """
        :param location_tuple: (Latitude, Longitude)
        :return: a location JSON request
        """
        return self.location.reverse_geocode(location_tuple)

    def get_timezone(self, location):
        """
        :param location: A JSON location request
        :return: a timezone JSON request
        """
        return self.location.timezone(location)

    def get_elevation(self, location):
        """
        :param location: A JSON location request
        :return: a elevation JSON request
        """
        return self.location.elevation(location)

    def get_current_location_from_ip(self):
        """
        :return: uses your ip to get the address as a string
        """
        return geocoder.ip(self.ip).address

    def parse_location_for_address(self, location_list):
        """
        :param location_list: A JSON location request
        :return: the address as a string
        """
        return location_list[1]['formatted_address']

    def parse_location_for_coordinates(self, location_list):
        """

        :param location_list: A JSON location request
        :return: a tuple (Latitude, Longitude)
        """
        coordinates = []
        for l in location_list:
            coordinates.append(l['geometry']['location']['lat'])  # Latitude
            coordinates.append(l['geometry']['location']['lng'])  # Longitude
        tuple_coordinates = tuple(float(c) for c in coordinates)
        return tuple_coordinates

    def parse_elevation(self, elevation_list):
        """
        :param elevation_list: an elevation JSON request
        :return: elevation as a float
        """
        elevation = 0.0
        for e in elevation_list:
            elevation = e['elevation']
        return elevation

    def parse_timezone(self, timezone_dict):
        """
        :parameter timezone JSON request
        :return timeZoneID as a String
        """
        return timezone_dict['timeZoneId']

    def parse_location_for_zip(self, location_list):
        """
        :parameter location JSON request
        :return the zipcode as a String
        """
        zip_code = ""
        for l in location_list:
            zip_code = l['address_components'][7]
        code = zip_code["long_name"]
        return code

    def current_elevation(self):
        """
        :return the elevation as a string for HAl to speak and display
        """
        elv = self.parse_elevation(self.get_elevation(
            self.parse_location_for_coordinates(self.get_location(self.get_current_location_from_ip()))))
        elv = int(round(elv, 2))
        return "You are at approximately " + str(elv) + " meters"

    def current_timezone(self):
        """
        :return: the timezone as astring for HAL to speak and display
        """
        tz = self.parse_timezone(self.get_timezone(self.parse_location_for_coordinates(
            self.get_location(self.get_current_location_from_ip()))))
        return "You are in the " + tz + " timezone"
