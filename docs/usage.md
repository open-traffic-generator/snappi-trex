[<< snappi-trex TOC](../README.md#Table-of-Contents)

# Usage
`snappi-trex` follows the standard usage of `snappi` with a few modifications to keep in mind.

## 1. Use ext='trex'
In the python script, declare snappi-trex api using
```
api = snappi.api(ext='trex')
```

## 2. TRex must be installed
TRex must be installed, and all snappi-trex Python scripts must have TRex's path added to the system path. To do this, scripts must start with the following imports.

```
import snappi
import sys, os

# Change '/opt/trex' if you installed TRex in another location
install_path = '/opt/trex/'
# Gets the most recent version of TRex installed
trex_version = max(os.listdir(install_path)) if len(os.listdir(install_path))>0 else ""
trex_path = '{0}{1}/automation/trex_control_plane/interactive'.format(install_path, trex_version)
sys.path.insert(0, os.path.abspath(trex_path))
```
Note: you can also do custom system paths, as long as they point to a valid version of TRex STL API.
```
import snappi
import sys, os

trex_path = 'opt/trex/v2.90/automation/trex_control_plane/interactive'
sys.path.insert(0, os.path.abspath(trex_path))
```

If the system path is invalid or no system path was added, snappi-trex will raise a `SnappiTrexException`

## 3. snappi Ports must be declared in same order as TRex Ports

The network interfaces in `/etc/trex_cfg.yaml` should be in the same order as the ports are declared in the snappi scripts. For example, say we have this `trex_cfg.yaml` with 4 ports.
```
- port_limit    : 4
  version       : 2
  low_end       : true
  interfaces    : ["veth1", "veth2", "veth3", "veth4"]
  port_info     :  # set ethernet header mac addr

                 - ip         : 1.1.1.1
                   default_gw : 2.2.2.2
                 - ip         : 2.2.2.2
                   default_gw : 1.1.1.1
                 - ip         : 3.3.3.3
                   default_gw : 4.4.4.4
                 - ip         : 4.4.4.4
                   default_gw : 3.3.3.3
```
Now, we create this snappi script segment that initializes 4 ports.
```
api = snappi.api(ext='trex')
cfg = api.config()
alice, bob, charlie, dave = (
    cfg.ports
    .port(name='alice')
    .port(name='bob')
    .port(name='charlie')
    .port(name='dave')
)
```
Port `alice` will transmit from `veth1`, port `bob` will transmit from `veth2`, port `charlie` will transmit from `veth3`, and so on.