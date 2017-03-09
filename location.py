import googlemaps
import geocoder
import os
import formatter as f


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

    def get_distance_matrix(self, origin, destination):
        """
        :param location: A location String
        :return: A directions JSON request
        """
        return self.location.distance_matrix(origin, destination)

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
        for location in location_list:
            coordinates.append(location['geometry']['location']['lat'])  # Latitude
            coordinates.append(location['geometry']['location']['lng'])  # Longitude
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
        :parameter timezone_dict JSON request
        :return timeZoneID as a String
        """
        return timezone_dict['timeZoneId']

    def parse_location_for_zip(self, location_list):
        """
        :parameter location_list JSON request
        :return the zipcode as a String
        """
        zip_code = ""
        for l in location_list:
            zip_code = l['address_components'][7]
        code = zip_code["long_name"]
        return code

    def get_timezone_offset(self, location_tuple):
        tz = self.get_timezone(location_tuple)
        return tz['rawOffset']

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

    def current_location(self):
        """
        :return: the location from your IP address as a String
        """
        return "You are currently in or nearby " + self.get_current_location_from_ip()

    def return_map_coordinates(self, request, request_index):
        """
        :param request: An array of strings
        :param request_index: A selected word to get location data after
        :return: A string consisting of Lat and Long information
        """
        e_w = ""
        n_s = ""
        location_string = f.Formatter().join_array_with_spaces(
            f.Formatter().get_index_after(request, request_index + 1))
        location = self.parse_location_for_coordinates(self.get_location(location_string))
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
        return "{0} is located at {1}° {2} and {3}° {4}".format(location_string, str(lat), n_s, str(long),
                                                                e_w)

    def get_elevation_at_location(self, request, request_index):
        """
        :param request: An array of strings
        :param request_index: A selected word to get location data after
        :return:  A string consisting of an elevation at a location
        """
        location = f.Formatter().join_array_with_spaces((f.Formatter().get_index_after(request, request_index + 1)))
        location_obj = self.parse_location_for_coordinates(self.get_location(location))
        elevation = self.parse_elevation(self.get_elevation(location_obj))
        return "{0} is at approximately {1} meters".format(location, str(int(round(elevation))))

    def get_distance_between_to_locations(self, request, request_index):
        """
        :param request: An array of strings
        :param request_index: A selected word to get location data after
        :return:  A string consisting of distance and travel time between two locations in a given radius
        """
        print(f.Formatter().get_index_after(request, request_index + 1))
        locations = f.Formatter().split_locations(f.Formatter().get_index_after(request, request_index + 1))
        print(locations)
        distance_matrix = self.get_distance_matrix(locations[0], locations[1])
        dest = distance_matrix['destination_addresses'][0]
        ori = distance_matrix['origin_addresses'][0]
        rows = distance_matrix['rows'][0]
        distance = ""
        time = ""
        for e in rows['elements']:
            if e['status'] == "ZERO_RESULTS":
                return "The distance between {0} and {1} is too far to calculate".format(ori, dest)
            distance = e['distance']['text']
            time = e['duration']['text']
        return "The distance between {0} and {1} is approximately {2} and it will take about {3} in travel time by car"\
            .format(ori, dest, distance, time)

    def get_distance_from_current_location(self, request, request_index):
        """
        :param request: An array of strings
        :param request_index: A selected word to get location data after
        :return:  A string consisting of distance and travel time between a location and your current location
        """
        destination = f.Formatter().join_array_with_spaces(f.Formatter().get_index_after(request, request_index + 1))
        distance_matrix = self.get_distance_matrix(self.get_current_location_from_ip(), destination)
        dest = distance_matrix['destination_addresses'][0]
        rows = distance_matrix['rows'][0]
        distance = ""
        time = ""
        for e in rows['elements']:
            if e['status'] == "ZERO_RESULTS":
                return "The distance to {0} is too far to calculate".format(dest)
            distance = e['distance']['text']
            time = e['duration']['text']
        return "The distance to {0} from your current location is approximately {1} " \
               "and it will take about {2} in travel time by car".format(dest, distance, time)

    def location_request(self, request):
        """
        Handles a location request from the user
        :param request: An array of strings
        :return: Location information for the user
        """
        location_request = "I couldn't find your location or the location you requested"
        if 'I' in request:
            location_request = self.current_location()
        elif 'is' in request:
            location_request = self.return_map_coordinates(request, request.index('is'))
        return location_request

    def elevation_request(self, request):
        """
        Handles an elevation request from the user
        :param request: An array of strings
        :return: Elevation information for the user
        """
        elevation_request = "Distance request failed. No location given"
        if 'I' in request:
            elevation_request = self.current_elevation()
        elif 'of' in request:
            elevation_request = self.get_elevation_at_location(request, request.index('of'))
        elif 'at' in request:
            elevation_request = self.current_elevation()
        return elevation_request

    def distance_request(self, request):
        """
        Handles a distance request from the user
        :param request: An array of strings
        :return: Distance information for the user
        """
        distance_request = "Distance request failed. No location given"
        if 'between' in request:
            distance_request = self.get_distance_between_to_locations(request, request.index('between'))
        elif 'to' in request:
            distance_request = self.get_distance_from_current_location(request, request.index('to'))
        return distance_request

    def timezone_request(self, request):
        """
        Handles a timezone request from the user
        :param request: An array of strings
        :return: Timezone information for the user
        """
        # timezone_request = "Timezone request failed. No location given"
        timezone_request = self.current_timezone()
        return timezone_request

if __name__ == '__main__':
    l = Location()
    print(l.get_timezone_offset((52, 4)))
    print(type(l.get_timezone_offset((52, 4))))
