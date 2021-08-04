import json
import snappi
from snappi_trex.validation import Validation
Validation.validate_import()
from snappi_trex.setconfig import SetConfig
from snappi_trex.capture import Capture
from snappi_trex.metrics import Metrics
from snappi_trex.link import Link
from snappi_trex.util import Util

import trex.stl.api as trex


class Api(snappi.Api):
    """T-Rex implementation of the abstract-open-traffic-generator package

    Args
    ----
    - host (str): The address and port of the T-Rex Server
    - port (str): The rest port of the T-Rex Server
    - username (str): The username for T-Rex Server
    """
    def __init__(self, **kwargs):
        """Create a session
        - address (str): The ip address of the TestPlatform to connect to
        where test sessions will be created or connected to.
        - port (str): The rest port of the TestPlatform to connect to.
        - username (str): The username to be used for authentication
        """
        location = kwargs.get('location')
        location = 'localhost:4501' if location is None else location
        Validation.validate_host(location)
        parse_loc = location.split(':')
        if len(parse_loc) > 0:
            server = parse_loc[0]
        if len(parse_loc) > 1:
            sync_port = int(parse_loc[1])
                
        super(Api, self).__init__()
        self._c = trex.STLClient(server=server,
                            sync_port=sync_port
        )

        self._port_ids = []
        self._transmit_states = {}
        self._capture = Capture(self._c)
        self._metrics = Metrics(self._c)
        self._link = Link(self._c)
        self._config = None

        Validation.validate_connection(self._c)

    
    def wait_on_traffic(self, ports):
        self._c.wait_on_traffic(ports = ports)


    # Maps port names used in Snappi to port index for T-Rex
    def _loadPorts(self):
        cfg_obj = json.loads(self._config.serialize())
        if 'ports' in cfg_obj:
            for p in cfg_obj['ports']:
                self._port_ids.append(p['name'])


    def set_config(self, config):
        """Set or update the configuration
        """
        # Create response
        res = self.response_warning()

        self._config = config
        cfg_obj = json.loads(self._config.serialize())
        self._loadPorts()
        self._capture.set_port_ids(self._port_ids)

        if 'captures' in cfg_obj:
            Validation.validate_capture_settings(cfg_obj['captures'], self._port_ids)
            self._capture.set_capture_settings(self._config.captures)

        self._c.reset(ports = list(range(len(self._port_ids))))
        # for each Snappi flow, construct the equivalent T-Rex stream
        for f in cfg_obj["flows"]:
            # Configure variable manager commands
            vmCmds = []

            # Configure flow rate
            pps, bps, percent = SetConfig.set_rate(rate=f['rate'])

            # Configure duration and initialize the transmit mode using rate and duration info
            mode = SetConfig.set_duration(duration=f['duration'], pps=pps, bps=bps, percent=percent)

            # Parse config all packet headers. Creates a Scapy packet with provided packet headers
            headerCmds, pkt_headers, layers = SetConfig.set_packet_headers(f['packet'])
            vmCmds += headerCmds
            
            #Constructs the packet base using all headers
            pkt_base = None
            for header in pkt_headers:
                pkt_base = header if pkt_base is None else pkt_base/header

            # Configure packet size: increment, random, or fixed
            sizeCmds, pad = SetConfig.set_packet_size(
                f_size=f['size'], pkt_base=pkt_base, layers=layers
            )
            vmCmds += sizeCmds
            
            # TODO: Now fix the checksum of modified packets
            vmCmds += SetConfig.fix_checksum(layers)

            # Construct the packet with given Flow Variables
            vm = trex.STLScVmRaw(vmCmds)
            pkt = trex.STLPktBuilder(pkt = pkt_base/pad, vm = vm)

            # Create the stream with given config
            s1 = trex.STLStream(packet = pkt,
                        mode = mode)

            # Add the stream to the client
            self._c.add_streams([s1], ports=[self._port_ids.index(f['tx_rx']['port']['tx_name'])])

        return res


    def set_transmit_state(self, payload):
        """Set the transmit state of flows
        """
        # Create response
        res = self.response_warning()

        Validation.validate_transmit(payload, self._config)
        ts = json.loads(payload.serialize())
        cfg_obj = json.loads(self._config.serialize())

        all_flows = not Util.list_not_empty('flow_names', ts)
            # Get all transmit ports names from each flow
        port_names = []
        for f in cfg_obj['flows']:
            if all_flows or f['name'] in ts['flow_names']:
                port_names.append(f['tx_rx']['port']['tx_name'])

        # Create port ID list from port names
        ports = []
        for p_name in port_names:
            p_idx = self._port_ids.index(p_name)
            if p_idx not in ports:
                ports.append(p_idx)

        ports_start = []
        ports_stop = []
        ports_resume = []
        ports_pause = []
        # Sort each port into start, stop, resume, or pause based on current state
        for p in ports:
            if ts['state'] == 'start':
                if p in self._transmit_states and self._transmit_states[p] == 'pause':
                    ports_resume.append(p)
                else:
                    ports_start.append(p)
            elif ts['state'] == 'stop':
                ports_stop.append(p)
            elif ts['state'] == 'pause':
                ports_pause.append(p)

            self._transmit_states[p] = ts['state']

        if len(ports_start) > 0:
            self._c.clear_stats(ports = ports_start)
            self._c.start(ports = ports_start)
        if len(ports_stop) > 0:
            self._c.stop(ports = ports_stop)
        if len(ports_resume) > 0:
            self._c.resume(ports = ports_resume)
        if len(ports_pause) > 0:
            self._c.pause(ports = ports_pause)

        return res


    def set_link_state(self, payload):
        # Create response
        res = self.response_warning()

        Validation.validate_link(payload, self._port_ids)
        self._link.set_link(payload, self._port_ids)

        return res

    
    def set_capture_state(self, payload):
        """Starts capture on all ports that have capture enabled.
        """
        # Create response
        res = self.response_warning()
        
        Validation.validate_capture(payload, self._port_ids)
        self._capture.set_capture(payload, self._port_ids)
        
        return res
        

    def get_capture(self, request):
        """Gets capture file and returns it as a byte stream
        """
        Validation.validate_capture_request(request, self._port_ids)
        return self._capture.get_capture(request)
        

    def get_metrics(self, request):
        """Gets port, flow and protocol metrics.
        """
        Validation.validate_metrics_request(request, self._port_ids)
        response_obj = {'choice': 'port_metrics'}
        response_obj['port_metrics'] = self._metrics.get_port_metrics(request, self._port_ids, self._capture, self._link)
        return self.metrics_response().deserialize(response_obj)


    def get_config(self):
        return self._config

