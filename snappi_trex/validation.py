from snappi_trex.exceptions import SnappiTrexException
from snappi_trex.util import Util

class Validation(object):
    """This class contains functions to validate the input of various
    configuration components. It will throw a SnappiTrexException for any
    invalid inputs that it detects.
    """

    @staticmethod
    def validate_import():
        error = None
        try:
            import trex.stl.api as trex
        except Exception as e:
            error = e
        if error is not None:
            raise SnappiTrexException('Failed to import TRex STL API. Please check that the correct system path was added. See usage.md for details.')


    @staticmethod
    def validate_connection(c):
        error = None
        try:
            # connect to server
            c.connect()
        except Exception as e:
            error = e
        
        if error is not None:
            print(error)
            raise SnappiTrexException('Could not connect to T-Rex server. Please verify connection info.')

    
    @staticmethod
    def validate_host(host):
        parse_host = host.split(':')
        if len(parse_host) > 2:
            raise SnappiTrexException('\'{}\' is an invalid hostname'.format(host))
        if len(parse_host) > 1 and not parse_host[1].isdigit():
            raise SnappiTrexException('\'{}\' is an invalid hostname'.format(host))


    @staticmethod
    def validate_rate(rate):
        """
        """
        pps = bps = percent = None
        if rate['choice'] == 'pps':
            pps = rate['pps']
        elif rate['choice'] == 'bps':
            bps = rate['bps']
        elif rate['choice'] == 'kbps':
            bps = rate['kbps']
        elif rate['choice'] == 'mbps':
            bps = rate['mbps']
        elif rate['choice'] == 'gbps':
            bps = rate['gbps']
        elif rate['choice'] == 'percentage':
            percent = rate['percentage']
        else:
            raise SnappiTrexException('Invalid \'rate\' choice')

        if pps is not None:
            if not isinstance(pps, float) and not isinstance(pps, int):
                print(isinstance(pps, float))
                raise SnappiTrexException('\'pps\' must be integer or float')
        if bps is not None:
            if not isinstance(bps, float) and not isinstance(bps, int):
                raise SnappiTrexException('\'(k/m/g)bps\' must be integer or float')
        if percent is not None:
            if not isinstance(percent, float) and not isinstance(percent, int):
                raise SnappiTrexException('\'percentage\' must be integer or float')

    @staticmethod
    def validate_duration(duration):
        """
        """
        if duration['choice'] == 'fixed_packets':
            if not isinstance(duration['fixed_packets']['packets'], int):
                raise SnappiTrexException('\'fixed_packets\' must be integer')

        elif duration['choice'] == 'fixed_seconds':
            raise SnappiTrexException('T-Rex does not support fixed_seconds duration choice')

        elif duration['choice'] == 'continuous':
            pass

        elif duration['choice'] == 'burst':
            if 'inter_burst_gap' in duration['burst']:
                if duration['burst']['inter_burst_gap']['choice'] == 'nanoseconds':
                    ibg = duration['burst']['inter_burst_gap']['nanoseconds']
                elif duration['burst']['inter_burst_gap']['choice'] == 'microseconds':
                    ibg = duration['burst']['inter_burst_gap']['microseconds']
                elif duration['burst']['inter_burst_gap']['choice'] == 'bytes':
                    raise SnappiTrexException('T-Rex does not support bytes \'inter_burst_gap\' choice')
                else:
                    raise SnappiTrexException('Invalid \'inter_burst_gap\' option')

                if not isinstance(ibg, float) and not isinstance(ibg, int):
                    raise SnappiTrexException('\'inter_burst_gap\' must be integer or float')
        else:
            raise SnappiTrexException('Invalid \'duration\' choice')

    
    @staticmethod
    def validate_packet(packet_headers):
        from snappi_trex.info import Info
        header_info = Info.get_header_info()
        if packet_headers is None:
            raise SnappiTrexException('Flow packet cannot be empty')
        for header in packet_headers:

            header_name = header['choice']
            scapy_header = header_info[header_name]['scapy_name']

            if header_name not in header_info:
                raise SnappiTrexException('Invalid packet \'header\' choice')

            for field in header[header_name]:

                if field == 'choice':
                    continue

                if (header_name == 'icmp' or header_name == 'icmpv6') and field == 'echo':
                    for icmp_field in header[header_name][field]:
                        field_info = header_info[header_name][icmp_field]
                        Validation.validate_value_option(
                            header_field=header[header_name][field][icmp_field],
                            layer_type=scapy_header,
                            length=field_info['length']
                        )
                    continue

                if field not in header_info[header_name]:
                    raise SnappiTrexException('\'{0}\' is not a supported \'{1}\' field'.format(field, header_name))
                        
                header_field = header[header_name][field]
                if header_name == 'ipv4' and field == 'priority':
                    if 'raw' not in header['ipv4']['priority']:
                        raise SnappiTrexException('ipv4 \'priority\' only supports \'raw\' option')
                    header_field = header['ipv4'][field]['raw']
                field_info = header_info[header_name][field]
                Validation.validate_value_option(
                    header_field=header_field,
                    layer_type=scapy_header,
                    length=field_info['length']
                )


    @staticmethod
    def validate_size(f_size):
        if f_size['choice'] == 'increment':
            start = f_size['increment']['start']
            end = f_size['increment']['end']
            step = f_size['increment']['step']
            if not isinstance(start, int):
                raise SnappiTrexException('increment packet size \'start\' must be integer')
            if not isinstance(end, int):
                raise SnappiTrexException('increment packet size \'end\' must be integer')
            if not isinstance(step, int):
                raise SnappiTrexException('increment packet size \'step\' must be integer')

        elif f_size['choice'] == 'random':
            start = f_size['random']['min']
            end = f_size['random']['max']
            if not isinstance(start, int):
                raise SnappiTrexException('random packet size \'start\' must be integer')
            if not isinstance(end, int):
                raise SnappiTrexException('random packet size \'end\' must be integer')

        elif f_size['choice'] == 'fixed':
            val = f_size['fixed']
            if not isinstance(val, int):
                raise SnappiTrexException('\'fixed\' packet size must be integer')

        else:
            raise SnappiTrexException('Invalid packet \'size\' choice')


    @staticmethod
    def validate_value_option(header_field, layer_type, length):
        if header_field['choice'] == 'value':
            Validation.validate_address(header_field['value'], layer_type, length)
        elif header_field['choice'] == 'values':
            for val in header_field['values']:
                Validation.validate_address(val, layer_type, length)
        elif header_field['choice'] == 'increment':
            Validation.validate_increment(header_field['increment'], layer_type, length, 1)
        elif header_field['choice'] == 'decrement':
            Validation.validate_increment(header_field['decrement'], layer_type, length, -1)
        else: 
            raise SnappiTrexException('Invalid field value choice')

    
    @staticmethod
    def validate_increment(field_inc, layer_type, length, dir):
        Validation.validate_address(field_inc['start'], layer_type, length)
        Validation.validate_address(field_inc['step'], layer_type, length)
        length = min(length, 64)
        if not isinstance(field_inc['count'], int):
            raise SnappiTrexException('\'count\' must be integer')
        start = Util.convert_to_long(field_inc['start'], layer_type)
        step = Util.convert_to_long(field_inc['step'], layer_type)
        cnt = field_inc['count']
        if step * cnt > Util.get_mask(length):
            raise SnappiTrexException('step*count cannot exceed the header field range')
        if length == 64 and start + dir*step*cnt > Util.get_mask(64) and start + dir*step*cnt < 0:
            raise SnappiTrexException('step*count is too high. Overflow is not support for 8 byte fields')

    
    @staticmethod
    def validate_address(addr, layer_type, length):
        error = False
        try:
            val = Util.convert_to_long(addr, layer_type)
            if val > Util.get_mask(length):
                error = True
        except ValueError as e:
            error = True
        except SyntaxError as e:
            error = True
        if error:
            raise SnappiTrexException('{0} is not a valid {1} address'.format(addr, layer_type))


    @staticmethod
    def validate_transmit(payload, config):
        if config is None:
            return
        all_flows = []
        for f in config.flows:
            all_flows.append(f.name)

        if payload.flow_names is not None:
            for f in payload.flow_names:
                if f not in all_flows:
                    raise SnappiTrexException('{} is an unrecognized flow name'.format(f))
        if (payload.state != 'start') and (payload.state != 'stop') and (payload.state != 'pause'):
            raise SnappiTrexException('{} is not a valid transmit state'.format(payload.state))


    @staticmethod
    def validate_capture(payload, port_ids):
        if payload.port_names is not None:
            for p_name in payload.port_names:
                if p_name not in port_ids:
                    raise SnappiTrexException('{} is an unrecognized port name'.format(p_name))
        if (payload.state != 'start') and (payload.state != 'stop'):
            raise SnappiTrexException('{} is not a valid capture state'.format(payload.state))


    @staticmethod
    def validate_capture_request(request, port_ids):
        p_name = request.port_name
        if p_name not in port_ids:
            raise SnappiTrexException('{} is an unrecognized port name'.format(p_name))


    @staticmethod
    def validate_link(payload, port_ids):
        if payload.port_names is not None:
            for p_name in payload.port_names:
                if p_name not in port_ids:
                    raise SnappiTrexException('\'{}\' is an unrecognized port name'.format(p_name))
        if (payload.state != 'up') and (payload.state != 'down'):
            raise SnappiTrexException('{} is not a valid link state'.format(payload.state))


    @staticmethod
    def validate_metrics_request(request, port_ids):
        if request.choice is not None and request.choice != 'port':
            raise SnappiTrexException('\'{}\' is not a supported metrics choice'.format(request.choice))
        if request.port.port_names is not None:
            for p_name in request.port.port_names:
                if p_name not in port_ids:
                    raise SnappiTrexException('\'{}\' is not a recognized port'.format(p_name))

        col_names = ['link', 'capture', 'frames_tx', 'frames_rx',
                    'bytes_tx', 'bytes_rx', 'frames_tx_rate', 'frames_rx_rate', 
                    'bytes_tx_rate', 'bytes_rx_rate']
        if request.port.column_names is not None:
            for col in request.port.column_names:
                if col not in col_names:
                    raise SnappiTrexException('\'{}\' is not a supported metrics column'.format(col))


    @staticmethod
    def validate_capture_settings(settings, port_ids):
        from snappi_trex.info import Info
        if settings is None:
            return
        for s in settings:
            for p_name in s['port_names']:
                if p_name not in port_ids:
                    raise SnappiTrexException('\'{}\' is not a recognized port'.format(p_name))

            if s['format'] != 'pcap':
                raise SnappiTrexException('\'{}\' is not a supported capture format'.format(s['format']))
            if 'packet_size' in s and s['packet_size'] is not None:
                raise SnappiTrexException('maximum capture packet size options are not supported')
            if s['overwrite']:
                raise SnappiTrexException('overwrite not supported for captures')

            capture_filter_info = Info.get_capture_filter_info()
            if 'filters' in s:
                for f in s['filters']:
                    for proto in f:
                        if proto == 'choice':
                            continue
                        if proto not in capture_filter_info:
                            raise SnappiTrexException('\'{}\' is not a supported capture filter protocol'.format(proto))
                        for field in f[proto]:
                            if field not in capture_filter_info[proto]:
                                raise SnappiTrexException('\'{}\' is not a supported capture filter {} field'.format(field, proto))








