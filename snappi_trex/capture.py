import io
import json
import dpkt
from snappi_trex.info import Info
from snappi_trex.util import Util

class Capture(object):

    def __init__(self, trexclient):
        self._client = trexclient
        self._captures = {}
        self._capture_states = {}
        self._cache = {}
        self._port_ids = []
        self._filters = {}


    def set_port_ids(self, port_ids):
        self._port_ids = port_ids

        for p in range(len(self._port_ids)):
            self._filters[p] = ''


    def set_capture_settings(self, settings):
        settings_obj = json.loads(settings.serialize())
        filter_info = Info.get_capture_filter_info()

        for s in settings_obj:
            ports = list(range(len(self._port_ids)))
            if Util.list_not_empty('port_names', settings_obj):
                ports = []
                for p_name in s['port_names']:
                    ports.append(self._port_ids.index(p_name))

            # Set filters
            filters = []
            if 'filters' in s:
                for f in s['filters']:
                    for protocol in f:
                        if protocol == 'choice':
                            continue
                        for field in f[protocol]:
                            filters.append(self._get_bpf(
                                f, protocol, field, filter_info)
                            )

            bpf_str = ' && '.join(filters)

            for p in ports:
                self._filters[p] = bpf_str


    def _get_bpf(self, f, protocol, field, filter_info, shift=0):
        # Handle ethernet MAC addresses b/c more than 4 bytes
        ether_src_or_dst = (
            (protocol == 'ethernet' and field == 'src') or
            (protocol == 'ethernet' and field == 'dst')
        )
        if (ether_src_or_dst):
            negate_str = 'not ' if f[protocol][field]['negate'] else ''
            return '{0}(ether {1} {2})'.format(
                negate_str,
                field,
                Util.long_to_MAC(int(f[protocol][field]['value'], 16))
            )

        # Handle VLAN ID
        if (protocol == 'vlan' and field == 'id'):
            negate_str = 'not ' if f[protocol][field]['negate'] else ''
            return '{0}(vlan {1})'.format(
                negate_str,
                '0x' + f[protocol][field]['value']
            )

        # General case
        value = int(f[protocol][field]['value'], 16) >> shift
        value_str = hex(value & filter_info[protocol][field]['mask'])

        if f[protocol][field]['mask'] is None:
            mask_str = ''
        else:
            mask_str = ' & ' + hex(int(f[protocol][field]['mask'], 16) >> shift)

        negate = f[protocol][field]['negate']
        negate_str = ' != ' if negate else ' == '

        bpf = '{0}{1}{2}{3}{4}{5}{6}'.format(
            filter_info[protocol]['name'],
            filter_info[protocol][field]['offset'],
            ' & ' + hex(filter_info[protocol][field]['mask']),
            mask_str,
            negate_str,
            value_str,
            mask_str
        )
        return bpf


    def set_capture(self, payload, port_ids):
        self._state = payload
        self._port_ids = port_ids
        cs = json.loads(payload.serialize())
        ports = list(range(len(port_ids)))
        if Util.list_not_empty('port_names', cs):
            ports = []
            for p_name in cs['port_names']:
                ports.append(port_ids.index(p_name))

        if cs['state'] == 'start':
            for p in ports:
                self._captures[p] = self._client.start_capture(rx_ports = [p], bpf_filter=self._filters[p])
                if p in self._cache:
                    self._cache.pop(p)
                self._capture_states[p] = cs['state']
        elif cs['state'] == 'stop':
            for p in ports:
                if p in self._captures:
                    self._cache[p] = []
                    self._client.fetch_capture_packets(self._captures[p]['id'], self._cache[p])
                    self._client.stop_capture(self._captures[p]['id'])
                    self._captures.pop(p)
                self._capture_states[p] = cs['state']

    def get_capture(self, request):
        port_idx = self._port_ids.index(request.port_name)
        res = io.BytesIO()

        pkt_list = []
        if port_idx in self._captures:
            self._client.fetch_capture_packets(self._captures[port_idx]['id'], pkt_list)
        elif port_idx in self._cache:
            pkt_list = self._cache.pop(port_idx)

        if len(pkt_list) == 0:
            return res

        wr = dpkt.pcap.Writer(res)
        for pkt in pkt_list:
            wr.writepkt(pkt=pkt['binary'], ts=pkt['ts'])

        res.seek(0)
        return res

    def is_started(self, port_id):
        return port_id in self._capture_states and self._capture_states[port_id] == 'start'