"""A few classes for mock HTTP responses from Google and Here geocode services.

Author: Dan Haggerty
Date: Feb. 2, 2018
"""
import json


class MockGoogleResponse(object):
    """Mock class for Google gecoding API response.

    Params:
        code (int): the status code of the response
        search_results (list<tuple<float, float>>): lat/lng results list
    """

    def __init__(self, code=200, search_results=None):
        search_results = search_results or []
        results = []
        for result in search_results:
            results.append({
                'geometry': {
                    'location': {
                        'lat': result[0],
                        'lng': result[1],
                    },
                },
            })

        self.data = {'results': results}
        self.code = code

    def read(self):
        """Gets a JSON string containing the response data."""
        return json.dumps(self.data)


class MockHereResponse(object):
    """Mock class for Here Geocoder API response.

    Params:
        code (int): the status code of the response
        search_results (list<tuple<float, float>>): lat/lng results list
    """
    def __init__(self, code=200, search_results=None):
        search_results = search_results or []
        results = []
        for result in search_results:
            results.append({
               'Location': {
                   'DisplayPosition': {
                       'Latitude': result[0],
                       'Longitude': result[1],
                   }
               }
            })

        self.data = {'Response': {'View': [{'Result': results}]}}
        self.code = code

    def read(self):
        """Gets a JSON string containing the response data."""
        return json.dumps(self.data)
