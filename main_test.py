import flask
import geocode_client
import httplib
import json
import main
import mock
import response_mocks
import unittest
import urllib

TEST_API_KEY = 'test_api_key'
TEST_APP_ID = 'test_app_id'
TEST_APP_CODE = 'test_app_code'

CREDENTIALS_OPTIONS = [
    '--google-api-key', TEST_API_KEY,
    '--here-credentials', TEST_APP_ID, TEST_APP_CODE
]

MOCK_LAT_LNG = (23.01, 144.88)


class TestGeocodingProxyService(unittest.TestCase):

    def setUp(self):
        self.app = main.app.test_client()
        self.patcher = mock.patch.object(urllib, 'urlopen')
        self.mock_urlopen = self.patcher.start()
        main._initialize(TEST_API_KEY, (TEST_APP_ID, TEST_APP_CODE),
                         main.GOOGLE_GEOCODE_SERVICE)

    def test_service_initializes_defaults_properly(self):
        first_client = main.clients[0]

        self.assertEqual(2, len(main.clients))
        self.assertIsInstance(first_client, geocode_client.GoogleGeocodeClient)
        self.assertEqual({'api_key': TEST_API_KEY}, first_client.credentials)

    def test_service_uses_preferred_service_first(self):
        main._initialize(TEST_API_KEY, (TEST_APP_ID, TEST_APP_CODE),
                         main.HERE_GEOCODE_SERVICE)

        first_client = main.clients[0]

        self.assertEqual(2, len(main.clients))
        self.assertIsInstance(first_client, geocode_client.HereGeocodeClient)
        self.assertEqual({'app_id': TEST_APP_ID, 'app_code': TEST_APP_CODE},
                         first_client.credentials)

    def test_address_lookup_api_succeeds_with_valid_address(self):
        self.mock_urlopen.return_value = response_mocks.MockGoogleResponse(
            code=httplib.OK, search_results=[MOCK_LAT_LNG])

        response = self.app.get('/api/address-lookup?address=660+king+st')
        response_data = json.loads(response.data)

        expected_data = {
            'lat': MOCK_LAT_LNG[0],
            'lng': MOCK_LAT_LNG[1],
            'service': 'Google Maps Geocoding API',
        }

        self.assertEqual(httplib.OK, response.status_code)
        self.assertEqual(expected_data, response_data)
        self.assertEqual(1, self.mock_urlopen.call_count)

    def test_address_lookup_calls_other_services_if_first_service_fails(self):
        self.mock_urlopen.return_value = response_mocks.MockGoogleResponse(
            code=httplib.NOT_FOUND)

        self.app.get('/api/address-lookup?address=660+king+st')

        self.assertEqual(2, self.mock_urlopen.call_count)

    def test_address_lookup_returns_404_if_all_services_fail(self):
        self.mock_urlopen.return_value = response_mocks.MockGoogleResponse(
            code=httplib.NOT_FOUND)

        response = self.app.get('/api/address-lookup?address=660+king+st')

        expected_data = {'error': 'Search term yielded no results'}
        actual_data = json.loads(response.data)

        self.assertEqual(httplib.NOT_FOUND, response.status_code)
        self.assertEqual(expected_data, actual_data)

    def test_address_lookup_returns_400_with_invalid_params(self):
        response = self.app.get('/api/address-lookup?invalid=660+king+st')

        expected_data = {'error': 'Bad request'}
        actual_data = json.loads(response.data)

        self.assertEqual(httplib.BAD_REQUEST, response.status_code)
        self.assertEqual(expected_data, actual_data)