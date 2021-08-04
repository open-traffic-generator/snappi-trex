import sys, os
import dotenv

dotenv.load_dotenv()

TREX_PATH = os.getenv('TREXPATH')

sys.path.insert(0, os.path.abspath(TREX_PATH))

import snappi



def hello_snappi():
    # create a new API instance where host points to controller
    # api = snappi_trex.snappi_api.Api() # Use local copy of snappi_trex
    api = snappi.api(ext='trex', host='localhost:4501') # Use installed package of snappi_trex
    
    # and an empty traffic configuration to be pushed to controller later on
    cfg = api.config()

    # add two ports where location points to traffic-engine (aka ports)
    p1, p2 = (
        cfg.ports
        .port(name='p1')
        .port(name='p2')
    )

    # add layer 1 property to configure same speed on both ports
    ly = cfg.layer1.layer1(name='ly')[-1]
    ly.port_names = [p1.name, p2.name]
    ly.speed = ly.SPEED_1_GBPS

    # enable packet capture on both ports
    cp = cfg.captures.capture(name='cp')[-1]
    cp.port_names = [p1.name, p2.name]

    # add two traffic flows
    f1, f2 = cfg.flows.flow(name='flow p1->p2').flow(name='flow p2->p1')
    # and assign source and destination ports for each
    f1.tx_rx.port.tx_name, f1.tx_rx.port.rx_name = p1.name, p2.name
    f2.tx_rx.port.tx_name, f2.tx_rx.port.rx_name = p2.name, p1.name

    # configure packet size, rate and duration for both flows
    f1.size.fixed = 1024
    f2.size.fixed = 512
    for f in cfg.flows:
        # send 1000 packets and stop
        f.duration.fixed_packets.packets = 1000
        # send 1000 packets per second
        f.rate.pps = 1000

    # configure packet with Ethernet, IPv4 and UDP headers for both flows
    eth1, ip1, icmpv61 = f1.packet.ethernet().ipv6().icmpv6()
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

    ip1.hop_limit.increment.start = 128
    ip1.hop_limit.increment.step = 1
    ip1.hop_limit.increment.count = 255
    
    ip1.flow_label.decrement.start = 500000
    ip1.flow_label.decrement.step = 100
    ip1.flow_label.decrement.count = 1000

    ip1.src.values = [
        '1111:2222:3333:4444:5555:6666:7777:8888',
        '2222:2222:3333:4444:5555:6666:7777:8888'
    ]
    ip1.dst.decrement.start = '1122:3344:5566:7788:8000:0000:0000:0000'
    ip1.dst.decrement.step = '0000:0000:0000:0000:0000:0123:1423:a43e'
    ip1.dst.decrement.count = 1000

    # set incrementing port numbers as source UDP ports
    udp22.src_port.value = 5002
    udp2.src_port.decrement.start = 5000
    udp2.src_port.decrement.step = 1
    udp2.src_port.decrement.count = 1000

    # assign list of port numbers as destination UDP ports
    udp22.dst_port.value = 5002
    udp2.dst_port.increment.start = 5000
    udp2.dst_port.increment.step = 1
    udp2.dst_port.increment.count = 1000

    icmpv61.echo.type.value = 128
    icmpv61.echo.code.increment.start = 234
    icmpv61.echo.code.increment.step = 1
    icmpv61.echo.code.increment.count = 255
    icmpv61.echo.identifier.values = [40000, 2345, 30000]
    icmpv61.echo.sequence_number.decrement.start = 123
    icmpv61.echo.sequence_number.decrement.step = 2
    icmpv61.echo.sequence_number.decrement.count = 127


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
    # with open('tests/data/pcap/icmpv6/icmpv61_p2.pcap', 'wb') as f:
    #     f.write(api.get_capture(req).getvalue())


if __name__ == '__main__':
    hello_snappi()
