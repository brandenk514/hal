import googlemaps


class Map:
    def __init__(self):
        self.map = googlemaps.Client(key="AIzaSyDlXhJ5AMfqSqjUbNhjkRsIbCZZQPMTNx8")

    def get_location_from_address(self, address):
        return self.map.geocode(address)

    def get_location_from_coordinates(self, lat):
        return self.map.geocode(lat)

    def get_timezone(self, location):
        return self.map.timezone(location)

    def get_elevation(self, location):
        return self.map.elevation(location)

    def parse_location_for_address(self, location_list):
        address = ""
        for l in location_list:
            address = l['formatted_address']
        return address

    def parse_location_for_coordinates(self, location_list):
        coordinates = {}
        for l in location_list:
            coordinates = l['geometry']['location']
        return coordinates


if __name__ == '__main__':
    m = Map()
    print(m.parse_location_for_coordinates(m.get_location_from_coordinates('1021 Dulaney Valley Road, Baltimore, MD')))
    print(m.get_elevation((39.4105767, -76.5996434)))
