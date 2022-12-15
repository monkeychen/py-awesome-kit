import http.client
import urllib
import urllib.parse
import urllib.request
import unittest
import json
from awekit import base
from awekit.base.util import strings


class HttpTest(unittest.TestCase):
    def test_http_client(self):
        conn = http.client.HTTPConnection("localhost:8193")
        headers = {"Content-Type": "application/json"}
        params = json.dumps({"username": "admin", "password": strings.md5("*****")})  # --- OK
        # params = json.dumps({"username": "admin", "password": strings.md5("admin123")}).encode(base.UTF8)  # --- OK
        conn.request("POST", '/topo/api/login', params, headers)
        res = conn.getresponse()
        print(res.read().decode(base.UTF_8))  # 自己解码

    def test_urllib_http_post(self):
        # params = json.dumps({"username": "admin", "password": strings.md5("admin123")})  # --- FAIL
        params = json.dumps({"username": "admin", "password": strings.md5("******")}).encode(base.UTF_8)  # --- OK
        # params = ('{"username": "admin", "password": "' + strings.md5("admin123") + '"}').encode(base.UTF8) # --- OK
        headers = {"Content-Type": "application/json"}
        req = urllib.request.Request("http://localhost:8193/topo/api/login", data=params, headers=headers)
        res = urllib.request.urlopen(req)
        msg = res.read().decode(base.UTF_8)
        msg_obj = json.loads(msg)
        print(msg_obj)

    def test_urllib_http_get(self):
        params = urllib.parse.urlencode({"sid": "测试用户SID", "other": 111}, encoding=base.UTF_8)
        url = f"http://localhost:8193/topo/api/ssologin?{params}"
        headers = {"Content-Type": "application/json"}
        req = urllib.request.Request(url, headers=headers, method="GET")
        res = urllib.request.urlopen(req)
        msg = res.read().decode(base.UTF_8)
        msg_obj = json.loads(msg)
        print(msg_obj)
