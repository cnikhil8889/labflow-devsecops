# CNK | Nikhil Kumar Choudavarapu | LabFlow DevSecOps
import concurrent.futures
import http.client
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from app.server import Registry, handler_for

class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(self.registry))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def request(self, method, path, body=None, content_type="application/json"):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=3)
        connection.request(method, path, body, {"Content-Type": content_type})
        response = connection.getresponse()
        result = response.status, json.loads(response.read())
        connection.close()
        return result

    def test_health_and_not_found(self):
        for path in ("/healthz", "/readyz"):
            self.assertEqual(self.request("GET", path)[0], 200)
        self.assertEqual(self.request("GET", "/unknown")[0], 404)

    def test_create_read_duplicate(self):
        run = {"run_id": "demo-1", "instrument": "scope-1", "status": "queued"}
        self.assertEqual(self.request("POST", "/runs", json.dumps(run)), (201, run))
        self.assertEqual(self.request("GET", "/runs")[1], {"runs": [run]})
        self.assertEqual(self.request("POST", "/runs", json.dumps(run))[0], 409)

    def test_invalid_payloads(self):
        for payload in ("{", "[]", "null", '{"run_id":"x"}', '{"run_id":"../x","instrument":"x","status":"queued"}', '{"run_id":"x","instrument":"x","status":[]}'):
            self.assertEqual(self.request("POST", "/runs", payload)[0], 400)
        self.assertEqual(self.request("POST", "/runs", "x" * 4097)[0], 413)
        self.assertEqual(self.request("POST", "/runs", "{}", "text/plain")[0], 415)

    def test_concurrent_duplicate_is_atomic(self):
        run = {"run_id": "same", "instrument": "demo", "status": "queued"}
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
            statuses = list(pool.map(lambda _: self.request("POST", "/runs", json.dumps(run))[0], range(5)))
        self.assertEqual(statuses.count(201), 1)
        self.assertEqual(statuses.count(409), 4)

    def test_capacity_is_bounded(self):
        self.registry.runs = {str(i): {} for i in range(1000)}
        self.assertEqual(self.request("POST", "/runs", '{"run_id":"new","instrument":"demo","status":"queued"}')[0], 503)

if __name__ == "__main__":
    unittest.main()
