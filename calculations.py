import math
from collections import namedtuple
from nominatim import Coordinate

def calc_distance(center: namedtuple, location: namedtuple) -> tuple:
    '''Given 2 locations, calculates the distance between them'''
    R = 3958.8

    dlat = abs(math.radians(float(location.lat)) - math.radians(float(center.lat)))
    dlon = abs(math.radians(float(location.lon)) - math.radians(float(center.lon)))
    alat = (math.radians(float(center.lat)) + math.radians(float(location.lat))) / 2

    x = dlon * math.cos(alat)
    d = math.sqrt(x ** 2 + dlat ** 2) * R

    return d

def _calc_aqi_per_pm(pm_lower_bound: float, pm_upper_bound: float, aqi_lower_bound: int, aqi_upper_bound: int) -> float:
    '''Given the pm concentration range and the aqi value range,
        calculates the aqi per 1 pm'''
    pm_range = pm_upper_bound - pm_lower_bound
    aqi_range = aqi_upper_bound - aqi_lower_bound

    return aqi_range / pm_range

def _round_num(num: float) -> int:
    '''Rounds a number normally where .5 always round up to the next whole number'''
    if num - math.floor(num) < .5:
        return math.floor(num)
    return math.ceil(num)

def calc_aqi(pm: float) -> int:
    '''Given the pm concentration, calculates its AQI value'''
    if 0.0 <= pm < 12.1:
        aqi = pm * _calc_aqi_per_pm(0.0, 12.0, 0, 50)
    elif 12.1 <= pm < 35.5:
        aqi = 51 + (pm - 12.1) * _calc_aqi_per_pm(12.1, 35.4, 51, 100)
    elif 35.5 <= pm < 55.5:
        aqi = 101 + (pm - 35.5) * _calc_aqi_per_pm(35.5, 55.4, 101, 150)
    elif 55.5 <= pm < 150.5:
        aqi = 151 + (pm - 55.5) * _calc_aqi_per_pm(55.5, 150.4, 151, 200)
    elif 150.5 <= pm < 250.5:
        aqi = 201 + (pm - 150.5) * _calc_aqi_per_pm(150.5, 250.4, 201, 300)
    elif 250.5 <= pm < 350.5:
        aqi = 301 + (pm - 250.5) * _calc_aqi_per_pm(250.5, 350.4, 301, 400)
    elif 350.5 <= pm < 500.5:
        aqi = 401 + (pm - 350.5) * _calc_aqi_per_pm(350.5, 500.4, 401, 500)
    elif 500.5 <= pm:
        aqi = 501
    
    return _round_num(aqi)

def calc_distance_tests() -> None:
    center = Coordinate(33.64324045, -117.84185686276017)
    coord1 = Coordinate(33.53814, -117.5998)
    coord2 = Coordinate(33.69037, -118.03055)
    coord3 = Coordinate(33.68315, -117.66642)
    coord4 = Coordinate(33.816, -118.23275)
    coord5 = Coordinate(33.86117, -117.96228)

    # used https://www.geodatasource.com/demo#distance-calculator 
    # to double check that the calculated distances were accurate
    assert round(calc_distance(center, coord1), 2) == 15.71
    assert round(calc_distance(center, coord2), 2) == 11.33
    assert round(calc_distance(center, coord3), 2) == 10.46
    assert round(calc_distance(center, coord4), 2) == 25.44
    assert round(calc_distance(center, coord5), 2) == 16.57

# Tests for calculating the aqi value
assert calc_aqi(0.0) == 0
assert calc_aqi(6.0) == 25
assert calc_aqi(12.0) == 50
assert calc_aqi(12.1) == 51
assert calc_aqi(23.75) == 76
assert calc_aqi(35.4) == 100
assert calc_aqi(35.5) == 101
assert calc_aqi(45.45) == 126
assert calc_aqi(55.4) == 150
assert calc_aqi(55.5) == 151
assert calc_aqi(102.95) == 176
assert calc_aqi(150.4) == 200
assert calc_aqi(150.5) == 201
assert calc_aqi(200.45) == 251
assert calc_aqi(250.4) == 300
assert calc_aqi(250.5) == 301
assert calc_aqi(300.45) == 351
assert calc_aqi(350.4) == 400
assert calc_aqi(350.5) == 401
assert calc_aqi(425.45) == 451
assert calc_aqi(500.4) == 500
assert calc_aqi(500.5) == 501
assert calc_aqi(600) == 501

# Tests for calculating the distance
calc_distance_tests()



