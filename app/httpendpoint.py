import requests
from steam.endpoint import *


class HTTPEndpoint(Endpoint):
    def __init__(self, url):
        super().__init__()
        self._url = url
        self._session = requests.Session()
        
    def send(self):
        ret, out = self.formatData()
        if ret:
            if type(out) == dict:
                self._session.post(self._url, json=out)
            else:
                self._session.post(self._url, data=out)
