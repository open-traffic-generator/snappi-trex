import sys, os
import dotenv
# from scapy.all import rdpcap

dotenv.load_dotenv()

TREX_PATH = os.getenv('TREXPATH')
sys.path.insert(0, os.path.abspath(TREX_PATH))

import snappi



def hello_snappi():
    # create a new API instance where host points to controller
    # api = snappi_trex.snappi_api.Api() # Use local copy of snappi_trex
    api = snappi.api(ext='trex') # Use installed package of snappi_trex
    
    # and an empty traffic configuration to be pushed to controller later on
    cfg = api.config()

    # add two ports where location points to traffic-engine (aka ports)
    p1, p2 = (
        cfg.ports
        .port(name='p1', location='localhost:5555')
        .port(name='p2', location='localhost:5556')
    )

    # add layer 1 property to configure same speed on both ports
    ly = cfg.layer1.layer1(name='ly')[-1]
    ly.port_names = [p1.name, p2.name]
    ly.speed = ly.SPEED_1_GBPS

    # enable packet capture on both ports
    cp = cfg.captures.capture(name='cp')[-1]
    cp.port_names = [p1.name, p2.name]

    # add two traffic flows
    f1, f2 = cfg.flows.flow(name='p1->p2').flow(name='p2->p1')
    # and assign source and destination ports for each
    f1.tx_rx.port.tx_name, f1.tx_rx.port.rx_name = p1.name, p2.name
    f2.tx_rx.port.tx_name, f2.tx_rx.port.rx_name = p2.name, p1.name

    # configure packet size, rate and duration for both flows
    f1.size.fixed = 128
    f2.size.fixed = 256
    for f in cfg.flows:
        # send 1000 packets and stop
        f.duration.fixed_packets.packets = 1000
        # send 1000 packets per second
        f.rate.pps = 500

    # configure packet with Ethernet, IPv4 and UDP headers for both flows
    eth1, ip1, tcp1, udp12 = f1.packet.ethernet().ipv4().tcp().udp()
    eth2, ip2, tcp2, udp22 = f2.packet.ethernet().ipv4().tcp().udp()

    # set source and destination MAC addresses
    eth2.src.value, eth2.dst.value = '00:AA:00:00:00:AA', '12:34:56:78:9A:BC'
    eth1.src.increment.start = '00:00:F0:00::1'
    eth1.src.increment.step = '00:00:01:00:00:00'
    eth1.src.increment.count = 1000
    eth2.src.values = ['11:22:33:44:55:66', '22:22:22:22:22:22']
    eth1.dst.decrement.start = '7F:FF:FF:FF:FF:FF'
    eth1.dst.decrement.step = '01:00:00:00:00:00'
    eth1.dst.decrement.count = 255

    # set source and destination IPv4 addresses
    ip2.src.value, ip2.dst.value = '10.0.0.2', '10.0.0.1'

    ip1.src.increment.start = '11.0.0.1'
    ip1.src.increment.step = '0.0.0.2'
    ip1.src.increment.count = 1000
    ip1.dst.decrement.start = '12.0.0.0'
    ip1.dst.decrement.step = '0.0.0.4'
    ip1.dst.decrement.count = 1000

    # set incrementing port numbers as source UDP ports
    udp12.src_port.value = 5001
    udp22.src_port.value = 5002
    tcp1.src_port.value = 5000
    tcp2.src_port.value = 5003
    tcp1.src_port.increment.start = 5000
    tcp1.src_port.increment.step = 1
    tcp1.src_port.increment.count = 1000
    tcp2.src_port.decrement.start = 5000
    tcp2.src_port.decrement.step = 1
    tcp2.src_port.decrement.count = 1000

    # assign list of port numbers as destination UDP ports
    udp12.dst_port.value = 5001
    udp22.dst_port.value = 5002
    tcp1.dst_port.value = 5000
    tcp2.dst_port.value = 5003
    tcp1.dst_port.increment.start = 5000
    tcp1.dst_port.increment.step = 1
    tcp1.dst_port.increment.count = 1000
    tcp2.dst_port.increment.start = 5000
    tcp2.dst_port.increment.step = 1
    tcp2.dst_port.increment.count = 1000
    tcp1.dst_port.values = [8000, 8004, 8049, 9001]


    tcp1.seq_num.increment.start = 30000
    tcp1.seq_num.increment.step = 10
    tcp1.seq_num.increment.count = 1000
    tcp1.ack_num.decrement.start = 9000000
    tcp1.ack_num.decrement.step = 10000
    tcp1.ack_num.decrement.count = 1000
    tcp1.data_offset.decrement.start = 15
    tcp1.data_offset.decrement.step = 1
    tcp1.data_offset.decrement.count = 5
    tcp1.ecn_ns.decrement.start = 1
    tcp1.ecn_ns.decrement.step = 1
    tcp1.ecn_ns.decrement.count = 1
    tcp1.ecn_cwr.increment.start = 0
    tcp1.ecn_cwr.increment.step = 1
    tcp1.ecn_cwr.increment.count = 1
    tcp1.ctl_rst.values = [1, 0]
    tcp1.ctl_fin.value = 1
    tcp1.window.increment.start = 13
    tcp1.window.increment.step = 10
    tcp1.window.increment.count = 1000


    print('Pushing traffic configuration ...')
    print(cfg.serialize())
    api.set_config(cfg)

    print('Starting packet capture on all configured ports ...')
    cs = api.capture_state()
    cs.state = cs.START
    cs.port_names = ['p1', 'p2']
    api.set_capture_state(cs)

    print('Starting transmit on all configured flows ...')
    ts = api.transmit_state()
    ts.state = ts.START
    api.set_transmit_state(ts)


    print('Checking metrics on all configured ports ...')
    print('Expected\tTotal Tx\tTotal Rx')
    assert wait_for(lambda: metrics_ok(api, cfg)), 'Metrics validation failed!'

    api.wait_on_traffic([0,1])

    ms = api.metrics_request()
    ms.port.port_names = ['p1', 'p2']
    ms.port.column_names = []
    metrics = api.get_metrics(ms)
    print(metrics)


    req = api.capture_request()
    req.port_name = 'p2'
    # with open('tests/data/pcap/tcp/tcp1_p2.pcap', 'wb') as f:
    #     f.write(api.get_capture(req).getvalue())
    
    
if __name__ == '__main__':
    hello_snappi()
