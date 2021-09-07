import sys, os
import dotenv
import pytest
import json
import snappi
import dpkt

dotenv.load_dotenv()

TREX_PATH = os.getenv('TREXPATH')
sys.path.insert(0, os.path.abspath(TREX_PATH))
sys.path.insert(0, os.path.abspath('.'))


def test_vlan():
    tests = json.load(open('tests/data/vlan/vlan.json'))
    run_tests(tests)


def test_arp():
    tests = json.load(open('tests/data/arp/arp.json'))
    run_tests(tests)


def test_ipv4():
    tests = json.load(open('tests/data/ipv4/ipv4.json'))
    run_tests(tests)


def test_ipv6():
    tests = json.load(open('tests/data/ipv6/ipv6.json'))
    run_tests(tests)


def test_icmp():
    tests = json.load(open('tests/data/icmp/icmp.json'))
    run_tests(tests)


def test_icmpv6():
    tests = json.load(open('tests/data/icmpv6/icmpv6.json'))
    run_tests(tests)


def test_gre():
    tests = json.load(open('tests/data/gre/gre.json'))
    run_tests(tests)


def test_tcp():
    tests = json.load(open('tests/data/tcp/tcp.json'))
    run_tests(tests)


def test_udp():
    tests = json.load(open('tests/data/udp/udp.json'))
    run_tests(tests)


def test_vxlan():
    tests = json.load(open('tests/data/vxlan/vxlan.json'))
    run_tests(tests)

def test_filters():
    tests = json.load(open('tests/data/filters/filters.json'))
    run_tests(tests)


def run_tests(tests):
    for test in tests:
        api = snappi.api(ext='trex')
        cfg = api.config().deserialize(test['test'])
        api.set_config(cfg)

        cs = api.capture_state()
        cs.state = cs.START
        api.set_capture_state(cs)

        ts = api.transmit_state()
        ts.state = ts.START
        api.set_transmit_state(ts)

        api.wait_on_traffic([0,1])

        req = api.capture_request()
        req.port_name = 'p2'
        cap = api.get_capture(req)

        req = api.metrics_request()
        req.port.port_names = ['p1', 'p2']
        met = api.get_metrics(req)

        with open(test['res'], 'rb') as res:
            res_bytes = b''
            pcap = dpkt.pcap.Reader(res)
            for _, buf in pcap:
                res_bytes +=buf

            cap_bytes = b''
            pcap = dpkt.pcap.Reader(cap)
            for _, buf in pcap:
                cap_bytes +=buf

            assert len(cap_bytes) == len(res_bytes)
            assert cap_bytes == res_bytes
