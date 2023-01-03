from collections import namedtuple
import api
import file
import urllib.parse
import urllib.request
import time

Coordinate = namedtuple('Coordinate', ['lat', 'lon'])

class FileCenter:
    def __init__(self, path: str) -> None:
        '''Initializes variables'''
        self._path = path
    def get_coord(self) -> namedtuple:
        '''
        Given a filename to a file with data in JSON format from the Nominatim API,
        returns a namedtuple containing the latitude in degrees and the longitude in degrees
        '''
        data = file.data_from_file(self._path)
        return _lat_and_lon(data[0])

class ApiCenter:
    def __init__(self, path: str) -> None:
        '''Initializes variables'''
        self._path = path
    def get_coord(self) -> namedtuple:
        '''
        Given the search url of the Nominatim API with the correct parameters,
        returns a namedtuple containing the latitude in degrees and the longitude in degrees
        '''
        data = api.get_result(self._path)
        return _lat_and_lon(data[0])

class FileLocation:
    def __init__(self, coords: list[str]) -> None:
        '''Initializes variables'''
        self._coords = coords
    def get_locations(self) -> list:
        '''
        Given a list of file paths, each file containing the result of a previous call to Nominatim,
        returns a list of the location names
        '''
        return _locations_from_file(self._coords)

class ApiLocation:
    def __init__(self, coords: list[str]) -> None:
        '''Initializes variables'''
        self._coords = coords
    def get_locations(self) -> list:
        '''
        Given a list of coordinates in the form of namedtuples, 
        returns a list of the coordinates' location names
        '''
        return _locations_from_api(self._coords)
        
def _lat_and_lon(data: dict) -> namedtuple:
    '''
    Given data in JSON format from the Nominatim API,
    returns a namedtuple containing the latitude in degrees and the longitude in degrees
    '''
    coord = Coordinate(data['lat'], data['lon'])
    return coord

def _locations_from_file(paths: list[str]) -> list:
    '''
    Given a list of file paths, each file containing the result of a previous call to Nominatim,
    returns a list of the location names
    '''
    locations = []

    for path in paths:
        obj = file.data_from_file(path)
        locations.append(obj['display_name'])

    return locations

def _locations_from_api(coords: list[str]):
    '''
    Given a list of coordinates in the form of namedtuples, 
    returns a list of the coordinates' location names
    '''
    locations = []

    for coord in coords:
        url = _create_reverse_url(coord)
        time.sleep(1) # pause for one second in between subsequent requests to the Nominatim api
        obj = api.get_result(url)
        locations.append(obj['display_name'])

    return locations

def _create_reverse_url(coord: namedtuple) -> str:
    '''Creates the reverse Nominatim api url'''
    params = urllib.parse.urlencode([('lat', str(coord.lat)), ('lon', str(coord.lon)), ('format', 'json')])
    url = 'https://nominatim.openstreetmap.org/reverse?' + params
    return url

def create_search_url(location: str) -> str:
    '''Creates the search Nominatim api url'''
    params = urllib.parse.urlencode([('q', location), ('format', 'json')])
    url =  'https://nominatim.openstreetmap.org/search?' + params
    return url






