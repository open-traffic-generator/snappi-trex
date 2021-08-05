import trex.stl.api as trex

class Info:
    """This class contains Python dictionaries that have useful information
    for carrying out processes
    """

    @staticmethod
    def get_header_info():
        """In order to add support for new packet headers, just add all of
        the necessary header info into this dictionary.
        Note: The packet header must be supported in Scapy

        Format:
        {
            header name in snappi: {
                "scapy_pkt": (construct scapy packet header)
                "scapy_name": (scapy header name)
                (snappi field 1): {
                    "field_str": (scapy field name)
                    "length": (length of field in bits)
                    "bit_fixup": (bits to shift right. More info below)
                },

                ...

                (snappi field X): {
                    "field_str": (scapy field name)
                    "length": (length of field in bits)
                    "bit_fixup": (bits to shift right. More info below)
                }
            }
        }

        Bit fixup:
        The T-Rex Field Engine uses Scapy field strings to set the fields.
        However, Scapy can only write from the start of an octet. Some header
        fields start in the middle of an octet, so there is a bit fixup to 
        shift right a certain number of bits and then start writing.
        Ex:
            tcp has a ctl_fin field that does not start at the beginning of an
            octet.
            In Scapy, tcp.flags will cause you to write at the start of the flags
            byte. ctl_fin is 15 bits after the start of the flags byte, so we give
            it 15 bits of bit fixup
        """
        return {
            "ethernet": {
                "scapy_pkt": trex.Ether(),
                "scapy_name": "Ethernet",
                "src": {"field_str": "src", "length": 48, "bit_fixup": 0},
                "dst": {"field_str": "dst", "length": 48, "bit_fixup": 0},
                "ether_type": {"field_str": "type", "length": 16, "bit_fixup": 0}
            },
            "ipv4": {
                "scapy_pkt": trex.IP(),
                "scapy_name": "IP",
                "src": {"field_str": "src", "length": 32, "bit_fixup": 0},
                "dst": {"field_str": "dst", "length": 32, "bit_fixup": 0},
                "version": {"field_str": "version", "length": 4, "bit_fixup": 0},
                "header_length": {"field_str": "ihl", "length": 4, "bit_fixup": 4},
                "priority": {"field_str": "tos", "length": 8, "bit_fixup": 0},
                "total_length": {"field_str": "len", "length": 16, "bit_fixup": 0},
                "identification": {"field_str": "id", "length": 16, "bit_fixup": 0},
                "reserved": {"field_str": "flags", "length": 1, "bit_fixup": 0},
                "dont_fragment": {"field_str": "flags", "length": 1, "bit_fixup": 1},
                "more_fragments": {"field_str": "flags", "length": 1, "bit_fixup": 2},
                "fragment_offset": {"field_str": "frag", "length": 13, "bit_fixup": 3},
                "time_to_live": {"field_str": "ttl", "length": 8, "bit_fixup": 0},
                "protocol": {"field_str": "proto", "length": 8, "bit_fixup": 0}
            },
            "udp": {
                "scapy_pkt": trex.UDP(),
                "scapy_name": "UDP",
                "src_port": {"field_str": "sport", "length": 16, "bit_fixup": 0},
                "dst_port": {"field_str": "dport", "length": 16, "bit_fixup": 0},
                "length": {"field_str": "len", "length": 16, "bit_fixup": 0}
            },
            "tcp": {
                "scapy_pkt": trex.TCP(),
                "scapy_name": "TCP",
                "src_port": {"field_str": "sport", "length": 16, "bit_fixup": 0},
                "dst_port": {"field_str": "dport", "length": 16, "bit_fixup": 0},
                "seq_num": {"field_str": "seq", "length": 32, "bit_fixup": 0},
                "ack_num": {"field_str": "ack", "length": 32, "bit_fixup": 0},
                "data_offset": {"field_str": "dataofs", "length": 4, "bit_fixup": 0},
                "ecn_ns": {"field_str": "flags", "length": 1, "bit_fixup": 7},
                "ecn_cwr": {"field_str": "flags", "length": 1, "bit_fixup": 8},
                "ecn_echo": {"field_str": "flags", "length": 1, "bit_fixup": 9},
                "ctl_urg": {"field_str": "flags", "length": 1, "bit_fixup": 10},
                "ctl_ack": {"field_str": "flags", "length": 1, "bit_fixup": 11},
                "ctl_psh": {"field_str": "flags", "length": 1, "bit_fixup": 12},
                "ctl_rst": {"field_str": "flags", "length": 1, "bit_fixup": 13},
                "ctl_syn": {"field_str": "flags", "length": 1, "bit_fixup": 14},
                "ctl_fin": {"field_str": "flags", "length": 1, "bit_fixup": 15},
                "window": {"field_str": "window", "length": 16, "bit_fixup": 0}
            },
            "arp": {
                "scapy_pkt": trex.ARP(),
                "scapy_name": "ARP",
                "hardware_type": {"field_str": "hwtype", "length": 16, "bit_fixup": 0},
                "protocol_type": {"field_str": "ptype", "length": 16, "bit_fixup": 0},
                "hardware_length": {"field_str": "hwlen", "length": 8, "bit_fixup": 0},
                "protocol_length": {"field_str": "plen", "length": 8, "bit_fixup": 0},
                "operation": {"field_str": "op", "length": 16, "bit_fixup": 0},
                "sender_hardware_addr": {"field_str": "hwsrc", "length": 48, "bit_fixup": 0},
                "sender_protocol_addr": {"field_str": "psrc", "length": 32, "bit_fixup": 0},
                "target_hardware_addr": {"field_str": "hwdst", "length": 48, "bit_fixup": 0},
                "target_protocol_addr": {"field_str": "pdst", "length": 32, "bit_fixup": 0}
            },
            "vlan": {
                "scapy_pkt": trex.Dot1Q(),
                "scapy_name": "Dot1Q",
                "priority": {"field_str": "prio", "length": 3, "bit_fixup": 0},
                "cfi": {"field_str": "id", "length": 1, "bit_fixup": 3},
                "id": {"field_str": "vlan", "length": 12, "bit_fixup": 4},
                "tpid": {"field_str": "type", "length": 16, "bit_fixup": 0}
            },
            "ipv6": {
                "scapy_pkt": trex.IPv6(),
                "scapy_name": "IPv6",
                "version": {"field_str": "version", "length": 4, "bit_fixup": 0},
                "traffic_class": {"field_str": "tc", "length": 8, "bit_fixup": 4},
                "flow_label": {"field_str": "fl", "length": 20, "bit_fixup": 4},
                "payload_length": {"field_str": "plen", "length": 16, "bit_fixup": 0},
                "next_header": {"field_str": "nh", "length": 8, "bit_fixup": 0},
                "hop_limit": {"field_str": "hlim", "length": 8, "bit_fixup": 0},
                "src": {"field_str": "src", "length": 128, "bit_fixup": 0},
                "dst": {"field_str": "dst", "length": 128, "bit_fixup": 0},
            },
            "gre": {
                "scapy_pkt": trex.GRE(),
                "scapy_name": "GRE",
                "checksum_present": {"field_str": "chksum_present", "length": 1, "bit_fixup": 0},
                "reserved0": {"field_str": "routing_present", "length": 12, "bit_fixup": 1},
                "version": {"field_str": "version", "length": 3, "bit_fixup": 5},
                "protocol": {"field_str": "proto", "length": 16, "bit_fixup": 0},
                "reserved1": {"field_str": "offset", "length": 16, "bit_fixup": 0}
            },
            "vxlan": {
                "scapy_pkt": trex.VXLAN(),
                "scapy_name": "VXLAN",
                "flags": {"field_str": "flags", "length": 8, "bit_fixup": 0},
                "reserved0": {"field_str": "reserved0", "length": 24, "bit_fixup": 0},
                "vni": {"field_str": "vni", "length": 24, "bit_fixup": 0},
                "reserved1": {"field_str": "reserved2", "length": 8, "bit_fixup": 0}
            },
            "icmp": {
                "scapy_pkt": trex.ICMP(),
                "scapy_name": "ICMP",
                "type": {"field_str": "type", "length": 8, "bit_fixup": 0},
                "code": {"field_str": "code", "length": 8, "bit_fixup": 0},
                "identifier": {"field_str": "id", "length": 16, "bit_fixup": 0},
                "sequence_number": {"field_str": "seq", "length": 16, "bit_fixup": 0}
            },
            "icmpv6": {
                "scapy_pkt": trex.ICMPv6EchoRequest(),
                "scapy_name": "ICMPv6EchoRequest",
                "type": {"field_str": "type", "length": 8, "bit_fixup": 0},
                "code": {"field_str": "code", "length": 8, "bit_fixup": 0},
                "identifier": {"field_str": "id", "length": 16, "bit_fixup": 0},
                "sequence_number": {"field_str": "seq", "length": 16, "bit_fixup": 0}
            },
            # "ppp": {
            #     "scapy_pkt": PPP(),
            #     "scapy_name": "PPP",
                # "address": {"field_str": "type", "length": 8, "bit_fixup": 0},
                # "control": {"field_str": "code", "length": 8, "bit_fixup": 0},
            #     "protocol_type": {"field_str": "proto", "length": 16, "bit_fixup": 0}
            # }
        }

    @staticmethod
    def get_metrics_columns():
        return {
            "frames_tx": "opackets",
            "frames_rx": "ipackets",
            "bytes_tx": "obytes",
            "bytes_rx": "ibytes",
            "frames_tx_rate": "tx_pps",
            "frames_rx_rate": "rx_pps",
            "bytes_tx_rate": "tx_bps",
            "bytes_rx_rate": "rx_bps"
        }

    @staticmethod
    def get_capture_filter_info():
        return {
            "ethernet": {
                "name": "ether",
                "src": {},
                "dst": {},
                "ether_type": {"offset":"[12:2]", "mask":0xffff}
            },
            "vlan": {
                "name": "vlan",
                "id": {}
            },
            "ipv4": {
                "name": "ip",
                "version": {"offset":"[0]", "mask":0xf0},
                "header_length": {"offset":"[0]", "mask":0x0f},
                "priority": {"offset":"[1]", "mask":0xff},
                "total_length": {"offset":"[2:2]", "mask":0xffff},
                "identification": {"offset":"[4:2]", "mask":0xffff},
                "reserved": {"offset":"[6]", "mask":0x80},
                "dont_fragment": {"offset":"[6]", "mask":0x40},
                "more_fragments": {"offset":"[6]", "mask":0x20},
                "fragment_offset": {"offset":"[6:2]", "mask":0x1fff},
                "time_to_live": {"offset":"[8]", "mask":0xff},
                "protocol": {"offset":"[9]", "mask":0xff},
                "header_checksum": {"offset":"[10:2]", "mask":0xffff},
                "src": {"offset":"[12:4]", "mask":0xffffffff},
                "dst": {"offset":"[16:4]", "mask":0xffffffff},
            }
        }