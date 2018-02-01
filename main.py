"""."""
import click
import geocode_client
import flask
import httplib

GOOGLE_GEOCODE_SERVICE = 'google'
HERE_GEOCODE_SERVICE = 'here'
SERVICES = {GOOGLE_GEOCODE_SERVICE, HERE_GEOCODE_SERVICE}

app = flask.Flask(__name__)
preferred_client = None
clients = []


@app.route('/api/address-lookup', methods=['GET'])
def address_lookup():
    """."""
    address = flask.request.args.get('address')

    if address is None:
        flask.abort(httplib.BAD_REQUEST)

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


def _initialize(google_api_key, here_credentials, preferred_service, debug):
    """."""
    for service in SERVICES:
        if service == GOOGLE_GEOCODE_SERVICE:
            new_client = geocode_client.GoogleGeocodeClient(
                api_key=google_api_key)
        elif service == HERE_GEOCODE_SERVICE:
            new_client = geocode_client.HereGeocodeClient(
                app_id=here_credentials[0], app_code=here_credentials[1])
        else:
            raise AssertionError('Some developer screwed up')

        if service == preferred_service:
            clients.insert(0, new_client)
        else:
            clients.append(new_client)

    app.run(debug=debug)


@click.command()
@click.option('--google-api-key',
              type=unicode,
              prompt='Enter API key for Google Maps Geocoding API',
              help='API key for Google Maps Geocoding API')
@click.option('--here-credentials', nargs=2,
              type=unicode,
              prompt='Enter API key for Here Geocoder API',
              help='API key for Google Maps Geocoding API')
@click.option('--preferred-service',
              type=click.Choice(SERVICES),
              default='google',
              help='The preferred geocoding service to use')
@click.option('--debug',
              is_flag=True,
              default=False,
              help='Run Flask in debug mode')
def run(google_api_key, here_credentials, preferred_service, debug):
    """."""
    _initialize(google_api_key, here_credentials, preferred_service, debug)


if __name__ == '__main__':
    run()
