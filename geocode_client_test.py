"""File level comment.
"""
import httplib
import json
import mock
import unittest
import urllib
import geocode_client


class MockGoogleResponse(object):

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
        return json.dumps(self.data)


class TestGoogleGeocodeClient(unittest.TestCase):
    """."""

    def setUp(self):
        self.patcher = mock.patch.object(urllib, 'urlopen')
        self.mock_urlopen = self.patcher.start()
        self.client = geocode_client.GoogleGeocodeClient(api_key='test_key')

    def test_get_lat_lng_succeeds(self):
        """Getting lat/long returns first search result from Google."""
        expected_lat_lng = (42.33, -122.45)
        other_lat_lng = (22.55, 55.77)

        self.mock_urlopen.return_value = MockGoogleResponse(code=200,
                search_results=[expected_lat_lng, other_lat_lng])

        results = self.client.get_lat_lng_from_address('660 King St')

        self.assertEqual(expected_lat_lng, results)

    def test_get_lat_lng_raises_upon_non_success_response(self):
        """."""
        error_response_code = httplib.BAD_REQUEST
        self.mock_urlopen.return_value = MockGoogleResponse(
            code=error_response_code)

        with self.assertRaises(geocode_client.GeocodeServiceSearchError) as err:
            self.client.get_lat_lng_from_address('600 King St')

        self.assertIn(err.message, error_response_code)

    def test_get_lat_lng_raises_upon_when_result_set_is_empty(self):
        self.mock_urlopen.return_value = MockGoogleResponse(
            code=200, search_results=[])

        with self.assertRaises(geocode_client.GeocodeServiceSearchError) as err:
            self.client.get_lat_lng_from_address('600 King St')
            self.assertIn(err.message, )


class TestHereGeocodeClient(unittest.TestCase):
    """."""

    def test_get_lat_lng_succeeds(self):
        """."""
        self.assertTrue(True)

    def test_get_lat_lng_raises_upon_non_success_response(self):
        """."""
        self.assertTrue(True)

    def test_get_lat_lng_raises_upon_when_result_set_is_empty(self):
        """."""
        self.assertTrue(True)