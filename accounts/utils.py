from geopy.geocoders import Nominatim


def get_lat_long(address):
    geolocator = Nominatim(user_agent="accounts_app")
    location = geolocator.geocode(address)

    if location:
        return location.latitude, location.longitude

    return None, None