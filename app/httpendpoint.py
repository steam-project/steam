import json
import requests
from steam.endpoint import *

class HTTPEndpoint(Endpoint):
    def config(self, endpoint):
        self._endpoint = endpoint
        self._session = requests.Session()
        
    def send(self):
        #print('\r{}'.format(self._data['id']), end='')
        data = {'event': self._data}
        # not minified json
        #self._session.post(self._endpoint, json=data)
        # minified json
        self._session.post(self._endpoint, data=json.dumps(data, separators=(',', ':')))
