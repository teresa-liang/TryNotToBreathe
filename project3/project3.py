import nominatim
import purpleair
from collections import namedtuple

def get_location() -> str:
    '''
    Asks the user for the first line of input,
    determining how the center coordinate will be fetched
    and returns the coordinate
    '''
    input1 = input()

    return _get_location_from_input(input1)

def _get_location_from_input(input1: str) -> str:
    '''Determines how the center coordinate will be fetched and returns the coordinate'''
    if 'CENTER NOMINATIM' in input1:
        location = input1[17:]
        url = nominatim.create_search_url(location)
        data = nominatim.ApiCenter(url)
    elif 'CENTER FILE' in input1:
        path = input1[12:]
        data = nominatim.FileCenter(path)
    
    return data.get_coord()

def get_range() -> int:
    '''Asks the user for the range and returns the range'''
    input2 = input()

    return _get_range_from_input(input2)

def _get_range_from_input(input2: str) -> int:
    '''Determines the range from an input and returns the range'''
    if 'RANGE' in input2:
        range = input2[6:]
        return int(range)

def get_threshold() -> int:
    '''Asks the user for the threshold and returns the threshold'''
    input3 = input()

    return _get_threshold_from_input(input3)


def _get_threshold_from_input(input3: str) -> int:
    '''Determines the threshold from an input and returns the threshold'''
    if 'THRESHOLD' in input3:
        aqi = input3[10:]
        return int(aqi)

def get_max() -> int:
    '''Asks the user for the max number and returns the max number'''
    input4 = input()

    return _get_max_from_input(input4)

def _get_max_from_input(input4: str) -> int:
    '''Determines the max from an input and returns the max'''
    if 'MAX' in input4:
        max = input4[4:]
        return int(max)

def get_air_data(center: namedtuple, range: int, threshold: int, max: int) -> str:
    '''
    Asks the user for the fifth line of input,
    determining how the air quality information from PurplerAir's api will be obtained,
    and returns a tuple containing the filtered list of coords and a list of corresponding aqi values'''
    input5 = input()

    return _get_air_data_from_input(input5, center, range, threshold, max)

def _get_air_data_from_input(input5: str, center: namedtuple, range: int, threshold: int, max: int) -> str:
    '''Determines how the air quality information from PurplerAir's api will be obtained,
    and returns a tuple containing the filtered list of coords and a list of corresponding aqi values'''
    if input5 == 'AQI PURPLEAIR':
        url = 'https://www.purpleair.com/data.json'
        locations = purpleair.ApiData(url, center, range, threshold, max)
    elif 'AQI FILE' in input5:
        path = input5[9:]
        locations = purpleair.FileData(path, center, range, threshold, max)
    
    return locations.filter_locations()

def get_reverse(data: list[namedtuple]) -> str:
    '''
    Asks the user for the sixth line of input,
    determining how the location names will be obtained
    and returns the location names
    '''
    input6 = input()
    
    return _get_reverse_from_input(input6, data)

def _get_reverse_from_input(input6: str, data: list[namedtuple]) -> str:
    '''Determines how the location names will be obtained
    and returns the location names'''
    if input6 == 'REVERSE NOMINATIM':
        coords = nominatim.ApiLocation(data)
        locations = coords.get_locations()
        return locations
    elif 'REVERSE FILES' in input6:
        input6 = input6.split()
        paths = input6[2:]
        paths = nominatim.FileLocation(paths)
        locations = paths.get_locations()
        return locations

def print_locations(coords: list[namedtuple], locations: list[str], aqis: list[int]) -> None:
    '''
    Prints out the resulting coordinates, location names, and aqi values
    '''
    for i in range(len(coords)):
        print(f'AQI {str(aqis[i])}')
        print(format_coordinate(coords[i]))
        print(locations[i])

def format_coordinate(coord: namedtuple) -> str:
    '''
    Given a coordinate in the form of a namedtuple,
    returns a string of the coordinate in a more readable format
    '''
    lat = float(coord.lat)
    lon = float(coord.lon)
    if lat < 0:
        lat_dir = 'S'
    else:
        lat_dir = 'N'
    
    if lon < 0:
        lon_dir = 'W'
    else:
        lon_dir = 'E'

    coord_str = f'{str(abs(lat))}/{lat_dir} {str(abs(lon))}/{lon_dir}'

    return coord_str

def _simulate_printing_results(coords: list[namedtuple], locations: list[str], aqis: list[int]):
    '''Given three lists, returns what would be printed out from the print_locations() function as a string'''
    output = ''
    for i in range(len(coords)):
        output += f'AQI {str(aqis[i])}\n'
        output += format_coordinate(coords[i]) + '\n'
        output += locations[i] + '\n'
    
    return output

def main() -> None:
    '''Run the entire program when the main function is called'''
    center = get_location()
    range1 = get_range()
    threshold = get_threshold()
    max = get_max()
    airdata = get_air_data(center, range1, threshold, max)
    reverse = get_reverse(airdata[0])
    print('CENTER', end=' ')
    print(format_coordinate(center))
    print_locations(airdata[0], reverse, airdata[1])

def test_main() -> None:
    '''Tests the main function given a set of inputs, solely using locally stored data'''
    center = _get_location_from_input('CENTER FILE nominatim_center.json')
    range1 = _get_range_from_input('RANGE 30')
    threshold = _get_threshold_from_input('THRESHOLD 50')
    max = _get_max_from_input('MAX 3')
    airdata = _get_air_data_from_input('AQI FILE purpleair.json', center, range1, threshold, max)
    reverse = _get_reverse_from_input('REVERSE FILES nominatim_reverse1.json nominatim_reverse2.json nominatim_reverse3.json', airdata[0])
    output = 'AQI 159\n33.838673/N 118.29809/W\nWest Carson, Los Angeles County, California, 90502, United States\nAQI 65\n33.716675/N 118.309906/W\n1498, West Hamilton Avenue, Los Angeles, Los Angeles County, California, 90731, United States\nAQI 54\n33.753635/N 117.85664/W\n1040, Stafford Street, Logan, Santa Ana, Orange County, California, 92701, United States\n'
    
    assert _simulate_printing_results(airdata[0], reverse, airdata[1]) == output

test_main()

if __name__ == '__main__':
    main()




    