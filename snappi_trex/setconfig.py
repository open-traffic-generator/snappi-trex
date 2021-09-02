import trex.stl.api as trex
from snappi_trex.info import Info
from snappi_trex.valueoptions import ValueOptions
from snappi_trex.validation import Validation

class SetConfig:

    @staticmethod
    def set_rate(rate):
        """
        Returns packets per second, bits per second, and percent values.
        (Only one of the three will be set, the rest will be Null)
        args: 
            - rate: A dictionary object containing all of the rate configuration info
        """
        Validation.validate_rate(rate)
        pps = bps = percent = None
        if rate['choice'] == 'pps':
            pps = rate['pps']
        elif rate['choice'] == 'bps':
            bps = rate['bps']
        elif rate['choice'] == 'kbps':
            bps = rate['kbps'] * 1000
        elif rate['choice'] == 'mbps':
            bps = rate['mbps'] * 1000000
        elif rate['choice'] == 'gbps':
            bps = rate['gbps'] * 1000000000
        elif rate['choice'] == 'percentage':
            percent = rate['percentage']
        return pps, bps, percent

    
    @staticmethod
    def set_duration(duration, pps, bps, percent):
        """
        Returns a STLTXMode object with correct rate and duration configurations
        args: 
            - duration: A dictionary object containing all of the duration config info
            - pps: packets per second
            - bps: bits per second
            - percent: percent of layer 2 bit rate
            Note: Only one of (pps, bps, percent) will have a value. The rest are None.
        """
        Validation.validate_duration(duration)
        if duration['choice'] == 'fixed_packets':
            mode = trex.STLTXSingleBurst(
                total_pkts=duration['fixed_packets']['packets'], 
                pps=pps, bps_L2=bps, percentage=percent
            )

        elif duration['choice'] == 'continuous':
            mode = trex.STLTXCont(pps=pps, bps_L2=bps, percentage=percent)

        elif duration['choice'] == 'burst':
            # TODO: Fix the ibg param to inter burst gap, not gap
            ibg = 0.0
            if 'inter_burst_gap' in duration['burst']:
                if duration['burst']['inter_burst_gap']['choice'] == 'nanoseconds':
                    ibg = duration['burst']['inter_burst_gap']['nanoseconds']
                elif duration['burst']['inter_burst_gap']['choice'] == 'microseconds':
                    ibg = duration['burst']['inter_burst_gap']['microseconds'] / 1000
            mode = trex.STLTXMultiBurst(
                pkts_per_burst=duration['burst']['packets'],
                ibg=ibg,
                count=duration['burst']['bursts'],
                pps=pps, bps_L2=bps, percentage=percent)

        return mode

    
    @staticmethod
    def set_packet_headers(packet_headers):
        """
        Returns list of VM instructions to correctly configure each packet header
        and each header field with correct value configurations. Also returns a list
        of packet headers added. Also returns list of strings representing the appended
        layers.
        args:
            - packet_headers: An array of objects that represent packet headers and all
            of their fields
        """
        Validation.validate_packet(packet_headers)
        header_info = Info.get_header_info()
        pkt_headers = []
        vm_cmds = []
        layers = [] # Keeps track of all of the layer types in order
        layer_cnt = {} # Counts the occurrences of each layer type
        for header in packet_headers:

            # Declare info
            header_name = header['choice']
            scapy_header = header_info[header_name]['scapy_name']
            scapy_pkt = header_info[header_name]['scapy_pkt']

            # Append packet header
            pkt_headers.append((scapy_pkt)); layers.append(scapy_header)

            # Increment the packet header count
            layer_cnt[scapy_header] = layer_cnt[scapy_header]+1 if scapy_header in layer_cnt else 1

            # Now configure the header fields
            for field in header[header_name]:

                # Skip the choice field
                if field == 'choice':
                    continue

                # Edge case for all icmp echo header fields
                if (header_name == 'icmp' or header_name == 'icmpv6') and field == 'echo':
                    for icmp_field in header[header_name][field]:
                        field_info = header_info[header_name][icmp_field]
                        vm_cmds += ValueOptions.get_value_cmds(
                            layer_type=scapy_header, 
                            layer_cnt=layer_cnt[scapy_header], 
                            header_field=header[header_name][field][icmp_field], 
                            length=field_info['length'], 
                            field_str=field_info['field_str'],
                            bit_fixup=field_info['bit_fixup']
                        )
                    continue

                header_field = header[header_name][field]
                # Edge case for ipv4's priority field
                if header_name == 'ipv4' and field == 'priority':
                    header_field = header['ipv4'][field]['raw']

                # General case
                field_info = header_info[header_name][field]
                vm_cmds += ValueOptions.get_value_cmds(
                    layer_type=scapy_header, 
                    layer_cnt=layer_cnt[scapy_header], 
                    header_field=header_field, 
                    length=field_info['length'], 
                    field_str=field_info['field_str'],
                    bit_fixup=field_info['bit_fixup']
                )
            
        return vm_cmds, pkt_headers, layers


    @staticmethod
    def set_packet_size(f_size, pkt_base, layers):
        """
        Returns a list of VM instructions to configure the correct size option. Also 
        returns a stream of bytes representing the padding of the packets
        args: 
            - f_size: A dictionary object containing all of the flow packet size config info
            - pkt_base: A Scapy packet containing all of the header information for every layer
            - layers: An ordered list of strings representing the order of headers on the packet base
                    Strings must conform to supported Scapy protocols
        """
        Validation.validate_size(f_size)
        fcs = 0
        if layers[0] == 'Ethernet':
            fcs = 4
        vm_cmds = []
        if f_size['choice'] == 'increment':
            needs_trim = True
            start = f_size['increment']['start']
            max_pkt_size = end = f_size['increment']['end']
            step = f_size['increment']['step']
            vm_cmds.append(trex.STLVmFlowVar(name = 'pkt_len', size = 2, op = 'inc', step = step,
                                            min_value = start-fcs,
                                            max_value = end-fcs))

        elif f_size['choice'] == 'random':
            needs_trim = True
            start = f_size['random']['min']
            max_pkt_size = end = f_size['random']['max']
            vm_cmds.append(trex.STLVmFlowVar(name = 'pkt_len', size = 2, op = 'random',
                                            min_value = start-fcs,
                                            max_value = end-fcs))

        elif f_size['choice'] == 'fixed':
            needs_trim = False
            max_pkt_size = f_size['fixed']

        # Trim packets and fix len field if needed
        if needs_trim:
            vm_cmds.append(trex.STLVmTrimPktSize('pkt_len'))
            layers_with_len = {'IP': 0, 'UDP': 0}
            for i, layer in enumerate(layers):
                if layer in layers_with_len:
                    pkt_offset = "{0}:{1}.len".format(layer, layers_with_len[layer])
                    vm_cmds.append(trex.STLVmWrFlowVar(fv_name='pkt_len',
                                                pkt_offset=pkt_offset,
                                                add_val=len(pkt_base[i])-len(pkt_base)
                    ))
                    layers_with_len[layer] += 1

        # Fill the rest of the packet with x's
        max_pkt_size -= fcs
        pad = max(0, max_pkt_size - len(pkt_base)) * '\0'

        return vm_cmds, pad


    @staticmethod
    def fix_checksum(layers):
        vm_cmds = []

        if layers is None:
            return vm_cmds

        # Fix all IP and checksums
        layers_with_cs = {'IP': 0, 'UDP': 0, 'TCP': 0, 'IPv6': 0}
        for layer in layers:
            if layer == 'IP':
                vm_cmds.append(trex.STLVmFixIpv4('IP:{}'.format(layers_with_cs['IP'])))
            if layer in layers_with_cs:
                layers_with_cs[layer] += 1

        # Fix UDP and TCP checksums in reverse
        for i, layer in reversed(list(enumerate(layers))):
            if i == 0:
                continue

            # Only fix the ones that sit on top of valid l3 protocols
            if layers[i-1] == 'IP' or layers[i-1] == 'IPv6':
                if layer == 'UDP':
                    vm_cmds.append(trex.STLVmFixChecksumHw(
                        l3_offset = layers[i-1] + ':' + str(layers_with_cs[layers[i-1]] - 1),
                        l4_offset = layer + ':' + str(layers_with_cs[layer] - 1),
                        l4_type = trex.CTRexVmInsFixHwCs.L4_TYPE_UDP
                    ))
                if layer == 'TCP':
                    vm_cmds.append(trex.STLVmFixChecksumHw(
                        l3_offset = layers[i-1] + ':' + str(layers_with_cs[layers[i-1]] - 1),
                        l4_offset = layer + ':' + str(layers_with_cs[layer] - 1),
                        l4_type = trex.CTRexVmInsFixHwCs.L4_TYPE_TCP
                    ))

            if layer in layers_with_cs:
                layers_with_cs[layer] -= 1

        return vm_cmds