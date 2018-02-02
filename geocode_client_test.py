"""File level comment.
"""
import httplib
import mock
import unittest
import urllib
import geocode_client
import response_mocks


class TestGoogleGeocodeClient(unittest.TestCase):
    """."""

    def setUp(self):
        self.api_key = 'test_key'
        self.patcher = mock.patch.object(urllib, 'urlopen')
        self.mock_urlopen = self.patcher.start()
        self.client = geocode_client.GoogleGeocodeClient(api_key=self.api_key)

    def test_get_lat_lng_succeeds(self):
        """Getting lat/long returns first search result from Google."""
        expected_lat_lng = (42.33, -122.45)
        other_lat_lng = (22.55, 55.77)

        self.mock_urlopen.return_value = response_mocks.MockGoogleResponse(
            code=200, search_results=[expected_lat_lng, other_lat_lng])

        results = self.client.get_lat_lng_from_address('660 King St')

        self.assertEqual(expected_lat_lng, results)

    def test_get_lat_lng_makes_proper_call_to_google_service(self):
        """Getting lat/long forms a proper request to Here API."""
        self.mock_urlopen.return_value = response_mocks.MockGoogleResponse(
            code=200, search_results=[(42.33, -122.45)])

        address = '660 King St'
        results = self.client.get_lat_lng_from_address(address)

        expected_params = urllib.urlencode({
            'address': address,
            'api_key': self.api_key,
        })
        expected_url = ('https://maps.googleapis.com/maps/api/geocode/json'
                        '?{}').format(expected_params)
        actual_url = self.mock_urlopen.call_args[0][0]

        self.assertEqual(expected_url, actual_url)

    def test_get_lat_lng_raises_upon_non_success_response(self):
        """."""
        error_response_code = httplib.BAD_REQUEST
        self.mock_urlopen.return_value = response_mocks.MockGoogleResponse(
            code=error_response_code)

        with self.assertRaises(geocode_client.GeocodeServiceSearchError) as e:
            self.client.get_lat_lng_from_address('600 King St')

        self.assertIn(str(error_response_code), e.exception.message)

    def test_get_lat_lng_raises_upon_when_result_set_is_empty(self):
        self.mock_urlopen.return_value = response_mocks.MockGoogleResponse(
            code=200, search_results=[])

        with self.assertRaises(geocode_client.GeocodeServiceSearchError) as e:
            self.client.get_lat_lng_from_address('600 King St')

        self.assertIn('found no results', e.exception.message)


class TestHereGeocodeClient(unittest.TestCase):
    """."""

    def setUp(self):
        self.app_id = 'test_id'
        self.app_code = 'test_code'
        self.patcher = mock.patch.object(urllib, 'urlopen')
        self.mock_urlopen = self.patcher.start()
        self.client = geocode_client.HereGeocodeClient(app_id=self.app_id,
                                                       app_code=self.app_code)

    def test_get_lat_lng_succeeds(self):
        """Getting lat/long returns first search result from Google."""
        expected_lat_lng = (42.33, -122.45)
        other_lat_lng = (22.55, 55.77)

        self.mock_urlopen.return_value = response_mocks.MockHereResponse(
            code=200, search_results=[expected_lat_lng, other_lat_lng])

        results = self.client.get_lat_lng_from_address('660 King St')


        self.assertEqual(expected_lat_lng, results)

    def test_get_lat_lng_makes_proper_call_to_here_service(self):
        """Getting lat/long forms a proper request to Here API."""
        self.mock_urlopen.return_value = response_mocks.MockHereResponse(
            code=200, search_results=[(42.33, -122.45)])

        address = '660 King St'
        results = self.client.get_lat_lng_from_address(address)

        expected_params = urllib.urlencode({
            'searchtext': address,
            'app_id': self.app_id,
            'app_code': self.app_code,
        })
        expected_url = ('https://geocoder.cit.api.here.com/6.2/geocode.json'
                        '?{}').format(expected_params)
        actual_url = self.mock_urlopen.call_args[0][0]

        self.assertEqual(expected_url, actual_url)

    def test_get_lat_lng_raises_upon_non_success_response(self):
        """."""
        error_response_code = httplib.BAD_REQUEST
        self.mock_urlopen.return_value = response_mocks.MockHereResponse(
            code=error_response_code)

        with self.assertRaises(geocode_client.GeocodeServiceSearchError) as e:
            self.client.get_lat_lng_from_address('600 King St')

        self.assertIn(str(error_response_code), e.exception.message)

    def test_get_lat_lng_raises_upon_when_result_set_is_empty(self):
        self.mock_urlopen.return_value = response_mocks.MockHereResponse(
            code=200, search_results=[])

        with self.assertRaises(geocode_client.GeocodeServiceSearchError) as e:
            self.client.get_lat_lng_from_address('600 King St')

        self.assertIn('found no results', e.exception.message)