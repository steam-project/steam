import requests
from steam.endpoint import *

class HTTPEndpoint(Endpoint):
    def config(self, endpoint):
        self._endpoint = endpoint
        self._session = requests.Session()
        
    def send(self):
        #print('\r{}'.format(self._data['id']), end='')
        data = {'event': self._data}
        self._session.post(self._endpoint, json=data)