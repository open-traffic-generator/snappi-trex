import sys, os
import dotenv

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
    fil1 = cp.filters.filter()[-1]
    fil1.ethernet.src.value = '10aabbccddee'
    fil1.ethernet.src.negate = True

    # add two traffic flows
    f1, f2 = cfg.flows.flow(name='flow p1->p2').flow(name='flow p2->p1')
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
        f.rate.pps = 1000

    # configure packet with Ethernet, IPv4 and UDP headers for both flows
    eth1, ip1, ip12, udp1, udp12 = f1.packet.ethernet().ipv4().ipv4().udp().udp()
    eth2, ip2, ip22, udp2, udp22 = f2.packet.ethernet().ipv4().ipv4().udp().udp()

    # set source and destination MAC addresses
    eth2.src.value, eth2.dst.value = '00:AA:00:00:00:AA', '12:34:56:78:9A:BC'
    eth1.src.increment.start = '10:AA:BB:CC:DD:EE'
    eth1.src.increment.step = '00:00:00:00:00:02'
    eth1.src.increment.count = 1000
    eth2.src.values = ['11:22:33:44:55:66', '22:22:22:22:22:22']
    eth1.dst.decrement.start = '10:AA:00:00:04:00'
    eth1.dst.decrement.step = '00:00:00:00:00:04'
    eth1.dst.decrement.count = 1000

    # set source and destination IPv4 addresses
    ip2.src.value, ip2.dst.value = '10.0.0.2', '10.0.0.1'
    ip22.src.value, ip22.dst.value = '10.0.0.3', '10.0.0.4'
    ip12.src.value, ip12.dst.value = '10.0.0.1', '10.0.0.2'

    ip1.src.increment.start = '11.0.0.1'
    ip1.src.increment.step = '0.0.0.2'
    ip1.src.increment.count = 1000
    ip1.dst.decrement.start = '12.0.0.0'
    ip1.dst.decrement.step = '0.0.0.4'
    ip1.dst.decrement.count = 1000

    # set incrementing port numbers as source UDP ports
    udp12.src_port.value = 5001
    udp22.src_port.value = 5002
    udp1.src_port.value = 5000
    udp2.src_port.decrement.start = 5000
    udp2.src_port.decrement.step = 1
    udp2.src_port.decrement.count = 1000

    # assign list of port numbers as destination UDP ports
    udp12.dst_port.value = 5001
    udp22.dst_port.value = 5002
    udp2.dst_port.increment.start = 5000
    udp2.dst_port.increment.step = 1
    udp2.dst_port.increment.count = 1000
    udp1.dst_port.values = [8000, 8004, 8049, 9001]


    print('Pushing traffic configuration ...')
    print(cfg.serialize())
    api.set_config(cfg)

    print('Starting packet capture on all configured ports ...')
    cs = api.capture_state()
    cs.state = cs.START
    api.set_capture_state(cs)

    print('Starting transmit on all configured flows ...')
    ts = api.transmit_state()
    ts.state = ts.START
    api.set_transmit_state(ts)

    api.wait_on_traffic([0,1])

    print('capturing...')
    req = api.capture_request()
    req.port_name = 'p2'
    # with open('tests/data/pcap/udp/udp_test_p2.pcap', 'wb') as f:
    #     f.write(api.get_capture(req).getvalue())



if __name__ == '__main__':
    hello_snappi()
