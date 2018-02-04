"""A single method web service for getting the lat/long of an address.

Author: Dan Haggerty
Date: Feb. 2, 2018

The service provides one GET endpoint:
    /api/addres-lookup?address=(address to lookup)

It relies on the following Geocoding web services:
  * Google Maps Geocoding API
  * Here Geocoder API.

If a call to one of these services fails for network reasons or returns no
lat/long results, the next service is called. The order of services is
arbitrary but the preferred service can be configured through the CLI. If all
services fail to give a result, this endpoint returns a 404.

Instructions on starting and configuring the server can be found in README.md.
"""
import click
import geocode_client
import flask
import httplib

GOOGLE_GEOCODE_SERVICE = 'google'
HERE_GEOCODE_SERVICE = 'here'
SERVICES = {GOOGLE_GEOCODE_SERVICE, HERE_GEOCODE_SERVICE}

app = flask.Flask(__name__)
preferred_client = None
clients = None


@app.route('/api/address-lookup', methods=['GET'])
def address_lookup():
    """Handler for address lookup endpoint.

    Returns:
        A flask.wrappers.Response (a JSON doc containing an error message or
        the lat/lng result and the service that was used to achieve the result)
    """
    address = flask.request.args.get('address')

    if address is None:
        return flask.jsonify({'error': 'Bad request'}), httplib.BAD_REQUEST

    for client in clients:
        try:
            lat, lng = client.get_lat_lng_from_address(address)
        except geocode_client.GeocodeServiceSearchError as err:
            app.logger.warning(err.message)
            continue

        return flask.jsonify({
            'lat': lat,
            'lng': lng,
            'service': client.service_name
        })

    return (flask.jsonify({'error': 'Search term yielded no results'}),
            httplib.NOT_FOUND)


def _initialize(google_api_key, here_credentials, preferred_service):
    """Initializes global list of geocode service clients.

    Params:
        google_api_key (string): Google Maps API key
        here_credentials (tuple<string, string>): Here App ID and App Code
        preferred_service (string): identifier for a geocode service
    """
    global clients
    clients = []
    for service in SERVICES:
        if service == GOOGLE_GEOCODE_SERVICE:
            new_client = geocode_client.GoogleGeocodeClient(
                api_key=google_api_key)
        else:
            new_client = geocode_client.HereGeocodeClient(
                app_id=here_credentials[0], app_code=here_credentials[1])

        # Put preferred service's client at the front of the client list
        if service == preferred_service:
            clients.insert(0, new_client)
        else:
            clients.append(new_client)


@click.command()
@click.option('--google-api-key',
              type=unicode,
              prompt='Enter API key for Google Maps Geocoding API',
              help='API key for Google Maps Geocoding API')
@click.option('--here-credentials', nargs=2,
              type=unicode,
              prompt='Enter API key for Here Geocoder API',
              help='API key for Here Geocoder API')
@click.option('--preferred-service',
              type=click.Choice(SERVICES),
              default='google',
              help='The preferred geocoding service to use')
@click.option('--debug',
              is_flag=True,
              default=False,
              help='Run Flask in debug mode')
def run(google_api_key, here_credentials, preferred_service, debug):
    """Entry point for the server that initializes everything.

    Params:
        google_api_key (string): Google Maps API key
        here_credentials (tuple<string, string>): Here App ID and App Code
        preferred_service (string): identifier for a geocode service
        debug (boolean): Flag for running Flask server in debug mode
    """
    _initialize(google_api_key, here_credentials, preferred_service)
    app.run(debug=debug)


if __name__ == '__main__':
    run()
