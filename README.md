# geocoding-proxy-service
A simple HTTP service that can resolve the lat, lng coordinates for an address
by using third party geocoding services. The two currently supported services are:

  [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/start)

  [Here Geocoder API](https://developer.here.com/documentation/geocoder/topics/quick-start.html)

The service will use the "preferred" service (defaults to Google) initially but
if that service returns no results or the call fails, the next service is called.
The first lat/lng result found is what gets returned.

## Running the server

#### (Optional) Set up a python virtual environment
    $ virtualenv env && source env/bin/activate

#### Install dependencies and start the server
    $ pip install -r requirements.txt
    $ python main.py --google-api-key YOUR_KEY --here-credentials YOUR_APP_ID YOUR_APP_CODE

#### Give it a shot
    $ curl http://localhost:5000/api/address-lookup?address=123+fake+st+springfield+usa

#### Command line options

    --google-api-key        APIKEY         API key for Google Maps Geocoding API
    --here-credentials      APPID APPCODE  API key for Google Maps Geocoding API
    [--preferred-service]   [google|here]  The preferred geocoding service to use
    [--debug]                              Run Flask in debug mode
    [--help]                               Show a help message and exit

## Running the tests

Make sure the dependencies are installed and run:

    $ python -m unittest discover --pattern=*_test.py -v


## API

There's only one endpoint:

    /api/address-lookup?address=660+king+st+san+francisco

The only param is ```address```, the address to look up. It returns a JSON object
with the following structure:

    {
      "lat": 44.98798,
      "lng": -92.1964799,
      "service": "Here Geocoder API"
    }

Where ```service``` is the service that found the result.

This endpoint will return 404 if all calls to the 3rd party API's fail,
or if no results are found by any service.

## TODO's
 * Cache lat/lng responses to save on calls to 3rd party API's
 * Add a "fast mode" where requests are made to all services in parallel
 * Add more geocoding services