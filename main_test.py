import geocode_client
import httplib
import main
import mock
import response_mocks
import unittest
import urllib
from click import testing

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
        self.runner = testing.CliRunner()

    def test_service_initializes_defaults_properly(self):
        result = self.runner.invoke(main.run, CREDENTIALS_OPTIONS)

        first_client = main.clients[0]
        second_client = main.clients[1]

        print result.output

        self.assertEqual(2, len(main.clients))
        self.assertIsInstance(first_client, geocode_client.GoogleGeocodeClient)
        self.assertEqual(first_client.credentials, {'api_key': TEST_API_KEY})

    def test_service_calls_preferred_service_first(self):
        pass

    def test_service_raises_if_preferred_service_isnt_supported(self):
        pass

    def test_address_lookup_api_succeeds_with_valid_address(self):
        pass

    def test_address_lookup_calls_other_services_if_first_service_fails(self):
        pass

    def test_address_lookup_returns_404_if_no_results_found(self):
        pass

    def test_fails_with_invalid_params(self):
        pass
    # def test_address_lookup_api_succeeds(self):
    #     address = '660 King St'
    #     response = self.app.get('/api/address-lookup?address={}'.format(
    #         address))
    #     self.assertEqual(response.status_code, httplib.OK)
    #
    # def test_address_lookup_api_fails_missing_address(self):
    #     address = '660 King St'
    #     response = self.app.get('/api/address-lookup?address={}'.format(
    #         address))
    #     self.assertEqual(response.status_code, httplib.BAD_REQUEST)