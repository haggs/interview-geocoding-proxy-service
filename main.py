import click
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@click.command()
@click.option('--api-key', help='The API key')
@click.option('--preferred-service', default='google', help='The prefer')
@click.option('--fast-mode', default=False, is_flag=True, help='Make parallel requests to both Geocache services every time')
@click.option('--debug', default=False, help='Run Flask in debug mode')
def run(api_key, preferred_service, fast_mode, debug):
    print 'API KEY:', type(api_key), api_key
    print 'PREFERRED SERVICE:', type(preferred_service), preferred_service
    print 'FAST MODE:', type(fast_mode), fast_mode
    # app.run(debug=debug)

if __name__ == '__main__':
    run()