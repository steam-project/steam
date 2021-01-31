import requests
from steam.endpoint import *


class HTTPEndpoint(Endpoint):
    def config(self, endpoint):
        self._endpoint = endpoint
        self._session = requests.Session()
        
    def send(self):
        ret, out = self.formatData()
        if ret:
            if type(out) == dict:
                self._session.post(self._endpoint, json=out)
            else:
                self._session.post(self._endpoint, data=out)
