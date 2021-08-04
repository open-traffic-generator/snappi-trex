[<< snappi-trex TOC](../README.md#Table-of-Contents)

# TRex-Tutorial
Here is a quick tutorial to set up TRex and some demo files to get it up and running! In this tutorial, I will only be going over TRex Stateless mode (STL). <br>
(Note: This tutorial was made using Ubuntu 20.04)
<br><br>

- [Table of contents](README.md)
    - [What is TRex?](#What-is-TRex)
    - [TRex Docker](#TRex-Docker)
    - [Installing TRex](#Installing-TRex)
    - [First Time Configuration of Network Interfaces](#First-Time-Configuration-of-Network-Interfaces)
    - [Running TRex](#Running-TRex)
        - [TRex Console](#TRex-Console)
        - [Python API](#Python-API)
    - [Conclusion](#That-is-all!)

## What is TRex?
TRex is a software traffic generator designed by Cisco that simulates real packet traffic across a network. TRex is fully configurable by the user. To learn more, visit the [TRex](https://trex-tgn.cisco.com) website. 

## Installing TRex
First, create a directory for TRex.
```sh
sudo mkdir /opt/trex
cd /opt/trex
```

Now, download the latest TRex version and extract the tar file (This tutorial was made using v2.90.)
```sh 
sudo wget --no-cache --no-check-certificate https://trex-tgn.cisco.com/trex/release/v2.90.tar.gz
sudo tar -xzvf v2.90.tar.gz
```

## Run TRex: two ways to run TRex (Pick one)
<details>
<summary>RUN USING TRex DOCKER IMAGE -- (Easier, less flexible)</summary>

## TRex Docker
### Docker installation
If docker is not installed on your machine, follow these instructions to install.
```sh
sudo apt-get update
sudo apt-get install curl
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Run TRex Docker image
To run a pre-configured 2 port TRex, simply download the snappi-trex docker image. This TRex is pre-configured with the same configuration as the instructions below.
```sh
sudo docker pull fyzhang2001/snappi-trex
```
<details>
<summary> (Optional) You can also build the docker image from `docker/Dockerfile` in the github Repo
</summary>

```sh
cd [snappi-trex github repo path]
sudo docker build --network=host docker -t snappi-trex
```
</details>
<br>

Then, run the docker container using
```sh
sudo docker run --rm -t --privileged --cap-add=ALL -p 4500:4500 -p 4501:4501 -p 4507:4507 fyzhang2001/snappi-trex
```
</details>

<details>
<summary>RUN USING TRex ON NATIVE MACHINE -- (tedious, more flexible)</summary>

## First Time Configuration of Network Interfaces
Make sure python-pip3 is installed
```sh
sudo apt-get install python3-pip
```
Change directories into the extracted TRex directory. (Replace v2.90 with version downloaded)
```sh
cd /opt/trex/v2.90
```

TRex operates by using the network interfaces on your machine as its ports. To create a virtual ethernet pair, run the following.
```sh
sudo ip link add veth1 type veth peer name veth2
sudo ip link set veth1 up
sudo ip link set veth2 up
```

To configure using the TRex port setup script provided in the installation, simply run the following script and follow the instructions. This script will create a config file `/etc/trex_cfg.yaml`. You can read more on [section 3.2](https://trex-tgn.cisco.com/trex/doc/trex_manual.html#_script_for_creating_config_file) of TRex's official documentation
```sh
sudo ./dpdk_setup_ports.py -i
```
If this script does not work for any reason, don't panic. If you're like me, the script doesn't show any of the network interfaces (maybe because I am on a VM). Instead, you can create a config file manually. (Note: use the text editor of your choice. I am using GEdit)
```sh
sudo touch /etc/trex_cfg.yaml
sudo gedit /etc/trex_cfg.yaml
```
Here is an example of a 2-port configuration. Paste this into `trex_cfg.yaml` (Note: YAML files are strict with spacing. DO NOT use tabs.)
```
- port_limit    : 2 # Increase if you would like more interfaces. Use even numbers.
  version       : 2
  low_end       : true
  interfaces    : ["veth1", "veth2"]   # list of the interfaces to bind run ./dpdk_nic_bind.py --status
  port_info     :  # set eh mac addr

                 - ip         : 1.1.1.1
                   default_gw : 2.2.2.2
                 - ip         : 2.2.2.2
                   default_gw : 1.1.1.1
```
TRex is now configured to map port 0 and port 1 to veth1 and veth2 respectively. You can add any network interfaces that you would like (eth, tap, veth, br, etc.). Just make sure to increase the port_limit

## Running TRex
Make sure python-pip3 is installed
```sh
sudo apt-get install python3-pip
```
Change directories into the extracted TRex directory if not already. (Replace v2.90 with version)
```sh
cd /opt/trex/v2.90
```

To run TRex, simply execute this command.
```sh
sudo ./t-rex-64 -i
```
You should now see the console running TRex. Here is what that should look like.
```
-Per port stats table 
      ports |               0 |               1 | 
 -----------------------------------------------------------------------------------------
   opackets |               0 |               0 |
     obytes |               0 |               0 |  
   ipackets |               0 |               0 |  
     ibytes |               0 |               0 | 
    ierrors |               0 |               0 | 
    oerrors |               0 |               0 | 
      Tx Bw |       0.00  bps |       0.00  bps |

-Global stats enabled 
 Cpu Utilization : 0.0  %
 Platform_factor : 1.0  
 Total-Tx        :       0.00  bps  
 Total-Rx        :       0.00  bps  
 Total-PPS       :       0.00  pps  
 Total-CPS       :       0.00  cps  

 Expected-PPS    :       0.00  pps  
 Expected-CPS    :       0.00  cps  
 Expected-BPS    :       0.00  bps  

 Active-flows    :        0  Clients :        0   Socket-util : 0.0000 %    
 Open-flows      :        0  Servers :        0   Socket :        0 Socket/Clients :  -nan 
 drop-rate       :       0.00  bps   
 current time    : X.X sec  
 test duration   : 0.0 sec  
 ```
 
</details>

<br>

## You now have T-Rex installed and running. 

<br>
<br>

 ## (OPTIONAL) Generating Traffic Using TRex (not required for Quickstart)
 
 <details>
 <summary>click for details</summary>
 
 To interface with the TRex application, we can either use the TRex Console, or the TRex Python API.
 ### TRex Console
 In order to open the TRex Console, simply open another terminal while TRex is running, and execute this command.
 ```sh
 ./trex-console
 ```
 Now that you have access to the console, let's try sending simple UDP packets across the ports. To do this, we are simply going to start a pre-configured traffic profile. You can find many other traffic profiles in the `stl` directory. To run the `udp_1pkt_1mac.py` profile, execute this command in the TRex console.
 ```sh
start -f stl/udp_1pkt_1mac.py -m 10kpps --port 0
 ```
 This will start a packet stream using the profile defined in `udp_1pk_1mac.py` with a multiplier of 10kpps on port 0 (veth1 in our case). You can also run the given YAML traffic profiles using the same command. Just replace the python script path with the YAML file path. 
 <br><br>
 You can also create your own traffic profiles. For more info on how to configure traffic profiles, visit the TRex [Stateless API Reference](https://trex-tgn.cisco.com/trex/doc/cp_stl_docs/api/index.html)
 <br><br>
Now, if you check the TRex application, you should see traffic running from port 0 to port 1. You can access other statistics by opening the TRex console and running this command. (make sure to enlarge the terminal)
```sh
tui
```

 ### Python API
 The other way to interface with TRex is by using the Python API. There are example Python scripts to look at in the `automation/trex_control_plane/interactive/trex/examples/stl` directory. Try running `stl_simple_burst.py`.
 ```sh
 python3 automation/trex_control_plane/interactive/trex/examples/stl/stl_simple_burst.py
 ```
 Again, once this python script is running, you can check the TRex application and see traffic running between the ports.
 <br><br>
 The Python API has various features that gives you full control of the kind of traffic you are sending over the ports. You can change source and destination MAC addresses, IPv4's, and ports. For more information on how to customize your traffic generator using the Python API, visit the TRex [Python API Documentation](https://trex-tgn.cisco.com/trex/doc/cp_stl_docs/api/client_code.html).

 ## That is all!
 You can now create custom traffic profiles and Python scripts to generate traffic across your network! :)

 </details>