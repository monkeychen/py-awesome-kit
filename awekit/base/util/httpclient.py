import urllib
import urllib.parse
import urllib.request
import json
from awekit import base


class HttpClient(object):

    def __init__(self, headers=None, encoding=base.UTF_8):
        if headers is None:
            headers = {"Content-Type": "application/json"}
        self.headers = headers
        self.encoding = encoding

    def restapi_post(self, url, req_params: dict, headers=None) -> dict:
        params = json.dumps(req_params).encode(self.encoding)  # --- OK
        tmp_headers = headers if headers is not None else self.headers
        req = urllib.request.Request(url, data=params, headers=tmp_headers, method="POST")
        res = urllib.request.urlopen(req)
        msg = res.read().decode(self.encoding)
        return json.loads(msg)

    def restapi_get(self, url, req_params: dict, headers=None) -> dict:
        encode_params = urllib.parse.urlencode(req_params, encoding=self.encoding)
        url = f"{url}?{encode_params}"
        tmp_headers = headers if headers is not None else self.headers
        req = urllib.request.Request(url, headers=tmp_headers, method="GET")
        res = urllib.request.urlopen(req)
        msg = res.read().decode(self.encoding)
        return json.loads(msg)

    def send_sms(self, receiver, content, api="http://localhost:8188/sms/api/send", sender=None) -> dict:
        params = {"content": content, "receiver": receiver, "sender": sender}
        return self.restapi_post(api, req_params=params)
