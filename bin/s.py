#!/usr/bin/env python3.5

from prometheus_client.core import CounterMetricFamily, REGISTRY
from prometheus_client import start_http_server
import json
import requests
import time
import socket
import os

class CustomCollector(object):
    def _getKibanaServers(self):
      for env in os.environ:
        if 'kibana' in env:
          yield {"key": env, "value": os.environ[env]}

    def _isValid(self, payload):
      for status in payload['status']['statuses']:
          if status['state'] != 'green':
              return False
      return True

    def collect(self):
        c = CounterMetricFamily('kibana_status_total', 'Kibana status total', labels=['kibana', 'hostname'])
        for kibana in self._getKibanaServers():
          response = json.loads(requests.get('http://{}:5601/api/status'.format(kibana["key"])).content.decode('UTF-8'))
          c.add_metric([kibana["key"], socket.gethostname()], 1 if self._isValid(response) else 0)
        yield c

if __name__ == '__main__':

  start_http_server(8034)
  REGISTRY.register(CustomCollector())

  while True: time.sleep(1)
