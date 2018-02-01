import json
import urllib


class GeocodeClient(object):
    url_template = None
    service_name = None

    def __init__(self, credentials):
        self.credentials = credentials

    def get_lat_lng_from_address(self, address):
        raise NotImplementedError()


class GoogleGeocodeClient(GeocodeClient):
    url_template = 'https://maps.googleapis.com/maps/api/geocode/json?{}'
    service_name = 'Google Maps Geocoding API'

    def __init__(self, api_key):
        super(GoogleGeocodeClient, self).__init__({'api_key': api_key})

    def get_lat_lng_from_address(self, address):
        url = self.url_template.format(urllib.urlencode({
            'address': address,
            'api_key': self.credentials['api_key'],
        }))
        response = urllib.urlopen(url)
        results = json.loads(response.read())
        location = results['results'][0]['geometry']['location']
        return location['lat'], location['lng']


class HereGeocodeClient(GeocodeClient):
    url_template = 'https://geocoder.cit.api.here.com/6.2/geocode.json?{}'
    service_name = 'Here Geocoder API'

    def __init__(self, app_id, app_code):
        super(HereGeocodeClient, self).__init__({
            'app_id': app_id, 'app_code': app_code})

    def get_lat_lng_from_address(self, address):
        url = self.url_template.format(urllib.urlencode({
            'searchtext': address,
            'app_id': self.credentials['app_id'],
            'app_code': self.credentials['app_code'],
        }))

        response = urllib.urlopen(url)

        results = json.loads(response.read())

        location = results['Response']['View'][0]['Result'][0][
            'Location']['DisplayPosition']

        return location['Latitude'], location['Longitude']


