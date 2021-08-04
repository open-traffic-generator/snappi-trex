import sys, os
import dotenv
from scapy.all import *
import json

dotenv.load_dotenv()

TREX_PATH = os.getenv('TREXPATH')
sys.path.insert(0, os.path.abspath(TREX_PATH))
sys.path.insert(0, os.path.abspath('.'))
from snappi_trex.setconfig import SetConfig

def test_setsize():
    sizes = json.load(open('tests/data/setsize.json'))
    for s in sizes:
        pkt_base = Ether()/IP()/UDP()
        layers = ['Ether', 'IP', 'UDP']
        vm_cmds, pad = SetConfig.set_packet_size(s['test'], pkt_base, layers)
        assert len(vm_cmds) == s['res']['len_cmds']
        assert len(pad) == s['res']['len_pad']
        for i in range(len(vm_cmds)):
            if i == 0:
                var = vm_cmds[0]
                res_var = s['res']['vm_cmds'][0]
                assert var.name == res_var['name']
                assert var.size == res_var['size']
                assert var.op == res_var['op']
                assert var.step == res_var['step']
                assert var.min_value == res_var['min_value']
                assert var.max_value == res_var['max_value']
                assert var.init_value == res_var['init_value']
                assert var.value_list == res_var['value_list']
            elif i == 1:
                var = vm_cmds[1]
                res_var = s['res']['vm_cmds'][1]
                assert var.fv_name == res_var['fv_name']
            else:
                var = vm_cmds[i]
                res_var = s['res']['vm_cmds'][i]
                assert var.fv_name == res_var['fv_name']
                assert var.offset_fixup == res_var['offset_fixup']
                assert var.pkt_offset == res_var['pkt_offset']
                assert var.add_val == res_var['add_val']
                assert var.is_big == res_var['is_big']

