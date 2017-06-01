import googlemaps
import geocoder
import os
import formatter as f
import datetime
from datetime import timedelta

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

    def get_current_location_from_ip(self):
        """
        :return: uses your ip to get the address as a string
        """
        try:
            return geocoder.ip(self.ip).address
        except None:
            return None

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
            code = zip_code["long_name"]
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
        :return: the timezone as a string for HAL to speak and display
        """
        tz = self.parse_timezone(self.get_timezone(self.parse_location_for_coordinates(
            self.get_location(self.get_current_location_from_ip()))))
        return "You are in the " + tz + " timezone"

    def get_time(self, requested_location):
        if requested_location is not None:
            current_tz = self.parse_location_for_coordinates(self.get_location(requested_location))
        else:
            current_tz = self.parse_location_for_coordinates(self.get_location(self.get_current_location_from_ip()))
        time_offset = self.get_timezone_offset(current_tz)
        time_dst = self.get_dst_offset(current_tz)
        time = datetime.datetime.utcnow() + timedelta(seconds=time_offset) + timedelta(seconds=time_dst)
        return "{:d}:{:02d}".format(time.hour, time.minute)

    def current_location(self):
        """
        :return: the location from your IP address as a String
        """
        return "You are currently in or nearby " + self.get_current_location_from_ip()

    def return_map_coordinates(self, location_requested):
        """
        :param location_requested: An array of strings
        :return: A string consisting of Lat and Long information
        """
        location = self.parse_location_for_coordinates(self.get_location(location_requested))
        lat = int(round(location[0], 0))
        long = int(round(location[1], 0))
        if location[0] < 0:
            n_s = "South"
            lat *= -1
        else:
            n_s = "North"
        if location[1] < 0:
            e_w = "West"
            long *= -1
        else:
            e_w = "East"
        return "{0} is located at {1}° {2} and {3}° {4}".format(location_requested, str(lat), n_s, str(long), e_w)

    def get_elevation_at_location(self, location_requested):
        """
        :param location_requested: An array of strings
        :return:  A string consisting of an elevation at a location
        """
        location_obj = self.parse_location_for_coordinates(self.get_location(location_requested))
        elevation = self.parse_elevation(self.get_elevation(location_obj))
        return "{0} is at approximately {1} meters".format(location_requested, str(int(round(elevation))))

    def get_distance_between_to_locations(self, distance_request):
        """
        :param distance_request: A string 
        :return:  A string consisting of distance and travel time between two locations in a given radius
        """
        locations = self.f.split_locations(self.f.split_sentence(distance_request))
        distance_matrix = self.get_distance_matrix(locations[0], locations[1])
        destination = distance_matrix['destination_addresses'][0]
        ori = distance_matrix['origin_addresses'][0]
        rows = distance_matrix['rows'][0]
        distance = ""
        time = ""
        for e in rows['elements']:
            if e['status'] == "ZERO_RESULTS":
                return "The distance between {0} and {1} is too far to calculate".format(ori, destination)
            distance = e['distance']['text']
            time = e['duration']['text']
        return "The distance between {0} and {1} is approximately {2} and it will take about {3} in travel time by car"\
            .format(ori, destination, distance, time)

    def get_distance_from_current_location(self, location_requested):
        """
        :param location_requested: A location as a string
        :return:  A string consisting of distance and travel time between a location and your current location
        """
        distance_matrix = self.get_distance_matrix(self.get_current_location_from_ip(), location_requested)
        destination = distance_matrix['destination_addresses'][0]
        rows = distance_matrix['rows'][0]
        distance = ""
        time = ""
        for e in rows['elements']:
            if e['status'] == "ZERO_RESULTS":
                return "The distance to {0} is too far to calculate".format(destination)
            distance = e['distance']['text']
            time = e['duration']['text']
        return "The distance to {0} from your current location is approximately {1} " \
               "and it will take about {2} in travel time by car".format(destination, distance, time)

    def location_request(self, location_requested):
        """
        Handles a location request from the user
        :param location_requested: An array of strings
        :return: Location information for the user
        """
        if location_requested == "":
            location_request = self.current_location()
        else:
            location_request = self.return_map_coordinates(location_requested)
        return location_request

    def elevation_request(self, location_requested):
        """
        Handles an elevation request from the user
        :param location_requested: An array of strings
        :return: Elevation information for the user
        """
        if location_requested == "":
            elevation_request = self.current_elevation()
        else:
            elevation_request = self.get_elevation_at_location(location_requested)
        return elevation_request

    def distance_request(self, locations_requested, classification):
        """
        Handles a distance request from the user
        :param locations_requested: An array of strings
        :param classification: A string that is a NaiveBayes Classification
        :return: Distance information for the user
        """
        distance_request = "Distance locations_requested failed. No location given"
        if classification == "distance":
            distance_request = self.get_distance_between_to_locations(locations_requested)
        elif classification == "distance from current loc":
            distance_request = self.get_distance_from_current_location(locations_requested)
        return distance_request

    def timezone_request(self, location_requested):
        """
        Handles a timezone request from the user
        :param location_requested: An location as a string
        :return: Timezone information for the user
        """
        if location_requested == "":
            timezone_request = "You are currently in " + self.current_timezone() + " time zone and it is currently "\
                               + self.get_time(None)
        else:
            timezone_request = location_requested + " is in the " + self.parse_timezone(self.get_timezone(
                self.parse_location_for_coordinates(self.get_location(location_requested)))) \
                               + " time zone and it is currently " + self.get_time(location_requested)
        return timezone_request
