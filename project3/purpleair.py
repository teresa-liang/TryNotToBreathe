import nominatim
import api
import file
from calculations import calc_distance, calc_aqi
from collections import namedtuple

class FileData:
    def __init__(self, path: str, center: namedtuple, range: int, threshold: int, max: int):
        '''Initializes variables'''
        self._path = path
        self._center = center
        self._range = range
        self._threshold = threshold
        self._max = max
    def filter_locations(self):
        '''
        Given data in JSON format from the PurpleAir API,
        returns a tuple containing the max number of location coordinates and their corresponding AQI values
        '''
        data = file.data_from_file(self._path)
        locations = _get_locations_in_range(self._center, data, self._range, self._threshold)
        return _get_max_locations_coords(self._max, locations)

class ApiData:
    def __init__(self, path: str, center: namedtuple, range: int, threshold: int, max: int):
        '''Initializes variables'''
        self._path = path
        self._center = center
        self._range = range
        self._threshold = threshold
        self._max = max
    def filter_locations(self):
        '''
        Calls the PurpleAir api and return a tuple containing the max number 
        of location coordinates and their corresponding AQI values
        '''
        data = api.get_result(self._path)
        locations = _get_locations_in_range(self._center, data, self._range, self._threshold)
        return _get_max_locations_coords(self._max, locations)
        

def _get_locations_in_range(center: namedtuple, obj: list, range: int, threshold: int) -> list:
    '''
    Given a list of dictionaries containing data about PurpleAir's sensors,
    filters out the locations that fulfill the set conditions
    '''
    filtered_locations = []
    data = obj['data']
    fields = obj['fields']
    
    for location in data:
        location = dict(zip(fields, location))
        if location['pm'] != None and location['pm'] != None and location['age'] != None and location['Type'] != None and location['Lat'] != None and location['Lon'] != None:
            if location['age'] <= 3600: # check if the sensor has reported a value in the last hour
                if location['Type'] == 0: # check if the sensor is outdoors
                    coord = nominatim.Coordinate(float(location['Lat']), float(location['Lon']))
                    if calc_distance(center, coord) <= range: # check if the location is in range
                        if calc_aqi(float(location['pm'])) >= threshold: # check if the location's aqi value is above the threshold
                            filtered_locations.append(location)

    return filtered_locations

def _get_max_locations_coords(max: int, data: list):
    '''
    Given a list of locations, sort the locations by pm value in descending order
    and returns the max number of locations in the form of a list of coordinates
    and returns the locations' corresponding AQI values 
    '''
    data = sorted(data, key=lambda k: k['pm'], reverse=True)
    data_max = data[:max]

    coord_list = []
    pm_list = []
    for location in data_max:
        coord = nominatim.Coordinate(float(location['Lat']), float(location['Lon']))
        coord_list.append(coord)
        pm_list.append(calc_aqi(location['pm']))

    return coord_list, pm_list
