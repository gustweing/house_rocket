import time 
from geopy.geocoders import Nominatim

geolocator = Nominatim( user_agent = 'geopyExercises' )

def get_data( x ):
    index, row = x
    time.sleep( 5 )

    #Chamada API
    response = geolocator.reverse( row['query'] )
  
    road = response.raw['address']['road'] if 'road' in response.raw else 'NA'
    house_number = response.raw['address']['house_number'] if 'house_number' in response.raw['address'] else 'NA'
    neighbourhood = response.raw['address']['neighbourhood'] if 'neighbourhood' in response.raw['address'] else 'NA'
    city = response.raw['address']['city'] if 'city' in response.raw['address'] else 'NA'
    county = response.raw['address']['county'] if 'county' in response.raw['address'] else 'NA'
    state = response.raw['address']['state'] if 'state' in response.raw['address'] else 'NA'
    place_id = response.raw['place_id'] if 'place_id' in response.raw else 'NA'
    osm_type = response.raw['osm_type'] if 'place_id' in response.raw else 'NA'
    country = response.raw['address']['country'] if 'country' in response.raw['address'] else 'NA'
    country_code = response.raw['address']['country_code'] if 'country_code' in response.raw['address'] else 'NA'

    return road, house_number, neighbourhood, city, county, state, place_id, osm_type, country, country_code