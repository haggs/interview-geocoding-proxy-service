import json


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


class MockHereResponse(object):

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
        return json.dumps(self.data)