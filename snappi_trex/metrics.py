import json
from snappi_trex.info import Info
from snappi_trex.util import Util

class Metrics(object):

    def __init__(self, trexclient):
        self._client = trexclient


    def get_port_metrics(self, request, port_ids, capture, link):
        req = json.loads(request.serialize())
        mc = Info.get_metrics_columns()
        if 'port' not in req:
            req['port'] = {'port_names': [], 'column_names': []}

        ports = list(range(len(port_ids)))
        if Util.list_not_empty('port_names', req['port']):
            ports = []
            for p_name in req['port']['port_names']:
                ports.append(port_ids.index(p_name))

        col_names = ['link', 'capture', 'frames_tx', 'frames_rx',
                    'bytes_tx', 'bytes_rx', 'frames_tx_rate', 'frames_rx_rate', 
                    'bytes_tx_rate', 'bytes_rx_rate']
        if Util.list_not_empty('column_names', req['port']):
            col_names = req['port']['column_names']

        metrics = self._client.get_stats(ports=ports)
        port_metrics  = []
        for p in ports:
            m = {}
            m['name'] = port_ids[p]

            if 'capture' in col_names:
                m['capture'] = 'stopped'
                if capture.is_started(p):
                    m['capture'] = 'started'

            if 'link' in col_names:
                m['link'] = 'down'
                if link.is_up(p):
                    m['link'] = 'up'

            metrics_p = metrics[p]
            for col in mc:
                if col in col_names:
                    metric_name_trex = mc[col]
                    m[col] = metrics_p[metric_name_trex]

            port_metrics.append(m)

        return port_metrics
     