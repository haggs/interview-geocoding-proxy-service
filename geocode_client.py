"""A few classes for making API calls to some geocoding web services.

The currently supported geocoding services are:
    * Google Maps Geocoding API
    * Here Geocoder API

Author: Dan Haggerty
Date: Feb. 2, 2018
"""
import httplib
import json
import urllib


class GeocodeServiceSearchError(Exception):
    """Class for general errors when calling geocoding services."""
    pass


class GeocodeClient(object):
    """Abstract class for geocoding service clients.

    Attributes:
        url_template (string): a template for forming the URL of a service call
        service_name (string): A printable name for the client's service

    Params:
        credentials (dict): A dict containing API keys
    """
    url_template = None
    service_name = None

    def __init__(self, credentials):
        self.credentials = credentials

    def get_lat_lng_from_address(self, address):
        """Interface for getting lat/long from an address.

        Params:
            address (string): the address to search

        Returns:
            A tuple<float, float> containing the lat/lng coordinates of
            the first search result for the given address.
        """
        raise NotImplementedError()


class GoogleGeocodeClient(GeocodeClient):
    """A client for interfacing with the Google Maps Geocoding API.

    Params:
        api_key (string): the Google Maps API key to use for making calls
    """
    url_template = 'https://maps.googleapis.com/maps/api/geocode/json?{}'
    service_name = 'Google Maps Geocoding API'

    def __init__(self, api_key):
        super(GoogleGeocodeClient, self).__init__({'api_key': api_key})

    def get_lat_lng_from_address(self, address):
        """Interface for getting lat/long from an address.

        Params:
            address (string): the address to search

        Returns:
            A tuple<float, float> containing the lat/lng coordinates of
            the first search result for the given address.
        """
        url = self.url_template.format(urllib.urlencode({
            'address': address,
            'api_key': self.credentials['api_key'],
        }))
        response = urllib.urlopen(url)

        if response.code != httplib.OK:
            raise GeocodeServiceSearchError(
                '{} returned status code {} for search term {}'.format(
                    self.service_name, response.code, address))

        results = json.loads(response.read())

        if not results['results']:
            raise GeocodeServiceSearchError(
                '{} found no results for search term: {}'.format(
                    self.service_name, address))

        location = results['results'][0]['geometry']['location']
        return location['lat'], location['lng']


class HereGeocodeClient(GeocodeClient):
    """A client for interfacing with the Here Geocoder API.

    Params:
        app_id (string): the app ID to use for making calls to Here
        app_code (string): the app code to use for making calls to Here
    """
    url_template = 'https://geocoder.cit.api.here.com/6.2/geocode.json?{}'
    service_name = 'Here Geocoder API'

    def __init__(self, app_id, app_code):
        super(HereGeocodeClient, self).__init__({
            'app_id': app_id, 'app_code': app_code})

    def get_lat_lng_from_address(self, address):
        """Interface for getting lat/long from an address.

        Params:
            address (string): the address to search

        Returns:
            A tuple<float, float> containing the lat/lng coordinates of
            the first search result for the given address.
        """
        url = self.url_template.format(urllib.urlencode({
            'searchtext': address,
            'app_id': self.credentials['app_id'],
            'app_code': self.credentials['app_code'],
        }))
        response = urllib.urlopen(url)

        if response.code != httplib.OK:
            raise GeocodeServiceSearchError(
                '{} returned status code {} for search term {}'.format(
                    self.service_name, response.code, address))

        results = json.loads(response.read())

        if not results['Response']['View'][0]['Result']:
            raise GeocodeServiceSearchError(
                '{} found no results for {}'.format(
                    self.service_name, address))

        location = results['Response']['View'][0]['Result'][0][
            'Location']['DisplayPosition']

        return location['Latitude'], location['Longitude']
