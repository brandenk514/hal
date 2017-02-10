import googlemaps
import geocoder
import os


class Map:
    def __init__(self):
        key = os.environ.get('GOOGLE_API_KEY')
        self.map = googlemaps.Client(key=key)

    def get_location(self, location):
        return self.map.geocode(location)

    def get_timezone(self, location):
        return self.map.timezone(location)

    def get_elevation(self, location):
        return self.map.elevation(location)

    """
    Returns the address in a formatted string, relative to US address system
    """

    def parse_location_for_address(self, location_list):
        address = ""
        for l in location_list:
            address = l['formatted_address']
        return address

    """
    Returns the latitude and longitude of a location given a location list from get_location_from_address()
    @:return (Latitude, Longitude)
    """

    def parse_location_for_coordinates(self, location_list):
        coordinates = []
        for l in location_list:
            coordinates.append(l['geometry']['location']['lat'])  # Latitude
            coordinates.append(l['geometry']['location']['lng'])  # Longitude
        tuple_coordinates = tuple(float(c) for c in coordinates)
        return tuple_coordinates

    def parse_elevation(self, elevation_list):
        elevation = 0.0
        for e in elevation_list:
            elevation = e['elevation']
        return elevation

    def parse_timezone(self, timezone_dict):
        return timezone_dict['timeZoneId']

    def get_current_location_from_ip(self, ip):
        return geocoder.ip(ip).address


if __name__ == '__main__':
    m = Map()

