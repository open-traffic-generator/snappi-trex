[<< snappi-trex TOC](../README.md#Table-of-Contents)

# Features
This document is a full list of supported and unsupported snappi features and the limitations. Keep in mind that this document does not describe the function of each feature, but only describes what is supported, unsupported, and the limitations of these features. For the full description of each snappi feature, read the Open Traffic Generator API [Documentation](https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/open-traffic-generator/models/master/artifacts/openapi.yaml)
* <font color="RED">UNSUPPORTED</font>: Feature is not supported in snappi-trex
* <font color="GREEN">FULLY SUPPORTED</font>: Feature is fully supported in snappi-trex without additional limitations
* <font color="GREEN">SUPPORTED</font>: Feature is supported in snappi-trex with limitations or some unsupported subfeatures

## set_config
<details>
<summary>ports: <font color="GREEN">SUPPORTED</font></summary>

Array() [
+ <details>
    <summary>name: <font color="GREEN">FULLY SUPPORTED</font></summary>
    The name of the port
    </details>
+ <details>
    <summary>location: <font color="RED">UNSUPPORTED</font></summary>
    TRex does not support port locations
    </details>
]
</details>
<details>
<summary>lags: <font color="RED">UNSUPPORTED</font></summary>
<font color="RED">UNSUPPORTED</font> FEATURE
</details>
<details>
<summary>layer1: <font color="RED">UNSUPPORTED</font></summary>
<font color="RED">UNSUPPORTED</font> FEATURE
</details>
<details>
<summary>captures: <font color="GREEN">SUPPORTED</font></summary>

Array() [
+ <details>
    <summary>port_names :<font color="GREEN">FULLY SUPPORTED</font></summary>
    A list of the names of ports that the capture configuration will apply to.
    </details>
+ <details>
    <summary>filters: <font color="GREEN">SUPPORTED</font></summary>
    
    + <details>
        <summary>choice: <font color="GREEN">SUPPORTED</font></summary>

        `"ethernet,"` `"vlan,"` or `"ipv4"`
        </details>
    + <details>
        <summary>custom: <font color="RED">UNSUPPORTED</font></summary>
        <font color="RED">UNSUPPORTED</font> FEATURE
        </details>
    + <details>
        <summary>ethernet: <font color="GREEN">SUPPORTED</font></summary>
        
        * `"src,"` `"dst,"` and `"ether_type"` are fully supported
        * pfc_queue is unsupported
        </details>
    + <details>
        <summary>vlan: <font color="GREEN">SUPPORTED</font></summary>
        
        * `"id"` is supported, however mask is unsupported
        </details>
    + <details>
        <summary>ipv4: <font color="GREEN">SUPPORTED</font></summary>
        
        * all fields fully supported
        </details>
    </details>
+ <details>
    <summary>overwrite: <font color="RED">UNSUPPORTED</font></summary>
    <font color="RED">UNSUPPORTED</font> FEATURE
    </details>
+ <details>
    <summary>packet_size: <font color="RED">UNSUPPORTED</font></summary>
    <font color="RED">UNSUPPORTED</font> FEATURE
    </details>
+ <details>
    <summary>format: <font color="RED">UNSUPPORTED</font></summary>
    <font color="RED">UNSUPPORTED</font> FEATURE
    </details>
+ <details>
    <summary>name: <font color="GREEN">FULLY SUPPORTED</font></summary>
    Globally unique name of the capture filter
    </details>
]
</details>
<details>
<summary>devices: <font color="RED">UNSUPPORTED</font></summary>
<font color="RED">UNSUPPORTED</font> FEATURE
</details>
<details>
<summary>flows: <font color="GREEN">SUPPORTED</font></summary>

Array() [
+ <details>
    <summary>tx_rx: <font color="GREEN">SUPPORTED</font></summary>
    
    + <details>
        <summary>port: <font color="GREEN">SUPPORTED</font></summary>
        
        + <details>
            <summary>tx_name: <font color="GREEN">FULLY SUPPORTED</font></summary>
            The unique name of a port that is the transmit port
            </details>
        + <details>
            <summary>rx_name: <font color="RED">UNSUPPORTED</font></summary>
            TRex does not support rx port names
            </details>
        </details>
    + <details>
        <summary>device: <font color="RED">UNSUPPORTED</font></summary>
        tx_rx devices are currently not supported
        </details>
    </details>
+ <details>
    <summary>packet: <font color="GREEN">SUPPORTED</font></summary>

    + <details open>
        <summary>Header Field Limitations:</summary>

        * For all packet header fields, loop-around is not support for incrementing/decrementing values. Values can only `increment`/`decrement` for however long the header field is. 
            * Ex. A 16 bit `UDP src port` can increment with a step size of 1 and a count of 65535. However, it cannot increment with a step size of 2 and a count of 40000 because step * count exceeds the maximum 16 bit integer.
            * This rule applies for any start value. `UDP src port` can start at 50000, increment up to 65,535, overflow down to 0, and increment back to a maximum of 49999. It cannot loop-around back to 50000
        * metric_groups are unsupported for all header fields
        * A maximum of `64 bytes` of header fields can be set per flow
        * `8 byte` header fields cannot `increment` past 0xffffffffffffffff or `decremenent` below zero. 
        </details>
    Array() [
    + <details>
        <summary>custom: <font color="RED">UNSUPPORTED</font></summary>
        Not currently supported
        </details>
    + <details>
        <summary>ethernet: <font color="GREEN">SUPPORTED</font></summary>
        
        + <details>
            <summary>dst: <font color="GREEN">SUPPORTED</font></summary>
            </details>
        + <details>
            <summary>src: <font color="GREEN">SUPPORTED</font></summary>
            </details>
        + <details>
            <summary>ether_type: <font color="GREEN">SUPPORTED</font></summary>
            </details>
        + <details>
            <summary>pfc_queue: <font color="RED">UNSUPPORTED</font></summary>
            Scapy does not support pfc_queue field
            </details>
        </details>
    + <details>
        <summary>vlan: <font color="GREEN">SUPPORTED</font></summary>
        All fields supported (with limitations above)
        </details>
    + <details>
        <summary>vxlan: <font color="GREEN">SUPPORTED</font></summary>
        All fields supported (with limitations above)
        </details>
    + <details>
        <summary>ipv4: <font color="GREEN">SUPPORTED</font></summary>

        + <details>
            <summary>header_length: <font color="GREEN">SUPPORTED</font> WITH LIMITATION</summary>

            * Note that this field gets overwritten if `random` or `increment` packet `size` option is used.
            </details>
        + <details>
            <summary>priority: <font color="GREEN">SUPPORTED</font></summary>
            
            + <details>
                <summary>raw: <font color="GREEN">SUPPORTED</font></summary>
                Only raw priority is supported
                </details>
            + <details>
                <summary>tos: <font color="RED">UNSUPPORTED</font></summary>
                Not currently supported
                </details>
            + <details>
                <summary>dscp: <font color="RED">UNSUPPORTED</font></summary>
                Not currently supported
                </details>
            </details>
        + <details>
            <summary>header_checksum: <font color="RED">UNSUPPORTED</font></summary>
            Not currently supported
            </details>
        All other fields supported (with limitations above)
        </details>
    + <details>
        <summary>ipv6: <font color="GREEN">SUPPORTED</font></summary>
        
        + <details>
            <summary>src and dst: <font color="GREEN">SUPPORTED</font> WITH LIMITATION</summary>

            * TRex only supports pattern variables of size 64 bits. Since `ipv6` `src` and `dst` are 128 bits long, only the last 64 bits will be pattern bits, and the first 64 bits will remain the same. (for `increment` and `decrement`)
            </details>
        All other fields supported (with limitations above)
        </details>
    + <details>
        <summary>pfcpause: <font color="RED">UNSUPPORTED</font></summary>
        Not currently supported
        </details>
    + <details>
        <summary>ethernetpause: <font color="RED">UNSUPPORTED</font></summary>
        Not currently supported
        </details>
    + <details>
        <summary>tcp: <font color="GREEN">SUPPORTED</font></summary>
        All fields supported (with limitations above)
        </details>
    + <details>
        <summary>udp: <font color="GREEN">SUPPORTED</font></summary>
        + <details>
            <summary>length: <font color="GREEN">SUPPORTED</font> WITH LIMITATION</summary>

            * Note that this field gets overwritten if `random` or `increment` packet `size` option is used.
            </details>
        + <details>
            <summary>checksum: <font color="RED">UNSUPPORTED</font></summary>
            Not currently supported
            </details>
        All other fields supported (with limitations above)
        </details>
    + <details>
        <summary>gre: <font color="GREEN">SUPPORTED</font></summary>
        
        + <details>
            <summary>checksum: <font color="RED">UNSUPPORTED</font></summary>
            Not currently supported
            </details>
        + <details>
            <summary>reserved1: <font color="GREEN">SUPPORTED</font> WITH LIMITATION</summary>
            
            * This will modify the 2 bytes after `protocol`. Thus, if there is an optional checksum present, this will modify the checksum.
            </details>
        All other fields supported (with limitations above)
        </details>
    + <details>
        <summary>gtpv1: <font color="RED">UNSUPPORTED</font></summary>
        Not currently supported
        </details>
    + <details>
        <summary>gtpv2: <font color="RED">UNSUPPORTED</font></summary>
        Not currently supported
        </details>
    + <details>
        <summary>arp: <font color="GREEN">SUPPORTED</font></summary>
        All fields supported (with limitations above)
        </details>
    + <details>
        <summary>icmp: <font color="GREEN">SUPPORTED</font></summary>
        
        + <details>
            <summary>checksum: <font color="RED">UNSUPPORTED</font></summary>
            Not currently supported
            </details>
        All other fields supported (with limitations above)
        </details>
    + <details>
        <summary>icmpv6: <font color="GREEN">SUPPORTED</font></summary>
        
        + <details>
            <summary>checksum: <font color="RED">UNSUPPORTED</font></summary>
            Not currently supported
            </details>
        All other fields supported (with limitations above)
        </details>
    + <details>
        <summary>ppp: <font color="RED">UNSUPPORTED</font></summary>
        Not currently supported
        </details>
    + <details>
        <summary>igmpv1: <font color="RED">UNSUPPORTED</font></summary>
        Not currently supported
        </details>
    ]
    </details>
+ <details>
    <summary>size: <font color="GREEN">FULLY SUPPORTED</font></summary>

    * The frame size which overrides the total length of the packet. Note that using `increment` or `random` option will overwrite packets' length fields. 
        * Ex: `udp`'s `length` field will be overwritten if packet size option is `increment`
    </details>
+ <details>
    <summary>rate: <font color="GREEN">FULLY SUPPORTED</font></summary>
    The rate of packet transmission
    </details>
+ <details>
    <summary>duration: <font color="GREEN">SUPPORTED</font></summary>
    
    + <details>
        <summary>fixed_packets: <font color="GREEN">SUPPORTED</font></summary>
        
        + <details>
            <summary>packets: <font color="GREEN">FULLY SUPPORTED</font></summary>
            Stop transmit of flow after this number of packets
            </details>
        + <details>
            <summary>gap: <font color="RED">UNSUPPORTED</font></summary>
            TRex does not support inter-packet gaps
            </details>
        + <details>
            <summary>delay: <font color="RED">UNSUPPORTED</font></summary>
            TRex does not support flow delays
            </details>
    + <details>
        <summary>fixed_seconds: <font color="RED">UNSUPPORTED</font></summary>
        TRex does not support fixed_seconds duration
        </details>
    + <details>
        <summary>burst: <font color="GREEN">SUPPORTED</font></summary>
        
        + <details>
            <summary>packets: <font color="GREEN">FULLY SUPPORTED</font></summary>
            The number of packets transmitted per burst
            </details>
        + <details>
            <summary>gap: <font color="RED">UNSUPPORTED</font></summary>
            TRex does not support inter-packet gaps
            </details>
        + <details>
            <summary>delay: <font color="RED">UNSUPPORTED</font></summary>
            TRex does not support flow delays
            </details>
        + <details>
            <summary>inter_burst_gap: <font color="GREEN">SUPPORTED</font></summary>
            
            + <details>
                <summary>bytes: <font color="RED">UNSUPPORTED</font></summary>
                TRex does not support bytes inter_burst_gap
                </details>
            + <details>
                <summary>nanoseconds: <font color="GREEN">FULLY SUPPORTED</font></summary>
                The amount of time between bursts in nanoseconds. 0 indicates no gap.
                </details>
            + <details>
                <summary>microseconds: <font color="GREEN">FULLY SUPPORTED</font></summary>
                The amount of time between bursts in microseconds. 0 indicates no gap.
                </details>
            </details>
    + <details>
        <summary>continuous: <font color="GREEN">SUPPORTED</font></summary>

        + <details>
            <summary>gap: <font color="RED">UNSUPPORTED</font></summary>
            TRex does not support inter-packet gaps
            </details>
        + <details>
            <summary>delay: <font color="RED">UNSUPPORTED</font></summary>
            TRex does not support flow delays
            </details>
    </details>
+ <details>
    <summary>metrics: <font color="RED">UNSUPPORTED</font></summary>
    TRex does not support flow metrics
    </details>
+ <details>
    <summary>name: <font color="GREEN">FULLY SUPPORTED</font></summary>
    The globally unique name of the flow
    </details>
]
</details>
<details>
<summary>events: <font color="RED">UNSUPPORTED</font></summary>
<font color="RED">UNSUPPORTED</font> FEATURE
</details>
<details>
<summary>options: <font color="RED">UNSUPPORTED</font></summary>
<font color="RED">UNSUPPORTED</font> FEATURE
</details>

<br>

## set_transmit_state
<details>
<summary>flow_names: <font color="GREEN">SUPPORTED</font></summary>

* TRex does not support transmitting on specific flows. TRex only supports transmitting on specific ports. Therefore, TRex will start, stop, pause, and resume flows by the transmit ports associated with these flows.
</details>
<details>
<summary>state: <font color="GREEN">FULLY SUPPORTED</font></summary>
The transmit state ("start", "stop", or "pause")
</details>

<br>

## set_link_state
<details>
<summary>port_names: <font color="GREEN">FULLY SUPPORTED</font></summary>
The names of ports to apply the configuration
</details>
<details>
<summary>state: <font color="GREEN">FULLY SUPPORTED</font></summary>
The link state ("up" or "down")
</details>

<br>

## set_capture_state
<details>
<summary>port_names: <font color="GREEN">FULLY SUPPORTED</font></summary>
The names of ports to apply the configuration
</details>
<details>
<summary>state: <font color="GREEN">FULLY SUPPORTED</font></summary>
The capture state ("start" or "stop")
</details>

<br>

## set_route_state
<details>
<summary>names: <font color="RED">UNSUPPORTED</font></summary>
TRex does not support route states
</details>
<details>
<summary>state: <font color="RED">UNSUPPORTED</font></summary>
TRex does not support route states
</details>

<br>

## get_metrics
<details>
<summary>port: <font color="GREEN">FULLY SUPPORTED</font></summary>

+ <details>
    <summary>port_names: <font color="GREEN">FULLY SUPPORTED</font></summary>
    The port result request to the traffic generator
    </details>
+ <details>
    <summary>column_names: <font color="GREEN">SUPPORTED</font></summary>
    
    * TRex does not support `transmit` and `location` columns
    </details>
</details>
<details>
<summary>flow: <font color="RED">UNSUPPORTED</font></summary>
TRex does not support flow metrics
</details>
<details>
<summary>bgpv4: <font color="RED">UNSUPPORTED</font></summary>
TRex does not support bgpv4 metrics
</details>
<details>
<summary>bgpv6: <font color="RED">UNSUPPORTED</font></summary>
TRex does not support bgpv6 metrics
</details>

<br>

## get_state_metrics
<details>
<summary>port_state: <font color="RED">UNSUPPORTED</font></summary>
Not currently supported
</details>
<details>
<summary>flow_state: <font color="RED">UNSUPPORTED</font></summary>
TRex does not support flow state metrics
</details>

<br>

## get_capture
<details open>
<summary>Limitations:</summary>

* TRex captures only supports fetching 1000 packets. So, get_capture will return the most recent 1000 packets
</details>
<details>
<summary>port_name: <font color="GREEN">SUPPORTED</font></summary>
</details>
