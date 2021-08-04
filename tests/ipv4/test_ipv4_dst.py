import sys, os
import dotenv
import json

dotenv.load_dotenv()

TREX_PATH = os.getenv('TREXPATH')
sys.path.insert(0, os.path.abspath(TREX_PATH))
sys.path.insert(0, os.path.abspath('.'))
from snappi_trex.setconfig import SetConfig

def test_ipv4_dst():
    packets = json.load(open('tests/data/ethernet/ethernet_dst.json'))
    for p in packets:
        vm_cmds, pkt_headers, layers = SetConfig.set_packet_headers(p['test'])
        # Variable declaration
        var = vm_cmds[0]
        res_var = p['res'][0]
        assert var.name == res_var['name']
        assert var.size == res_var['size']
        assert var.op == res_var['op']
        assert var.step == res_var['step']
        assert var.min_value == res_var['min_value']
        assert var.max_value == res_var['max_value']
        assert var.init_value == res_var['init_value']
        assert var.value_list == res_var['value_list']
        # Writing bytes
        wr = vm_cmds[1]
        res_wr = p['res'][1]
        assert wr.fv_name == res_wr['fv_name']
        assert wr.offset_fixup == res_wr['offset_fixup']
        assert wr.pkt_offset == res_wr['pkt_offset']
        assert wr.pkt_cast_size == res_wr['pkt_cast_size']
        assert wr.mask == res_wr['mask']
        assert wr.shift == res_wr['shift']
        assert wr.add_value == res_wr['add_value']
        assert wr.is_big == res_wr['is_big']

# Test increment configuration
def test_dst_inc():
    p1 = [
        {
            'choice': 'ethernet',
            'ethernet': {}
        },
        {
            'choice': 'ipv4',
            'ipv4': {
                'dst': {
                    'choice': 'increment',
                    'increment': {'start': '192.168.0.1', 'step': '0.0.1.2', 'count': 300}
                }
            }
        }
    ]

    vm_cmds, pkt_headers, layers = SetConfig.set_packet_headers(p1)
    # Variable declaration
    var = vm_cmds[0]
    assert var.name == 'IP0_dst:0'
    assert var.size == 4
    assert var.op == 'inc'
    assert var.step == 0x00_00_01_02
    assert var.min_value == 0x00_00_00_00
    assert var.max_value == 0x00_01_2E_58
    assert var.init_value == 0x00_00_00_00
    assert var.value_list == None
    # Writing variable
    wr = vm_cmds[1]
    assert wr.fv_name == 'IP0_dst:0'
    assert wr.offset_fixup == 0
    assert wr.pkt_offset == 'IP:0.dst'
    assert wr.pkt_cast_size == 4
    assert wr.mask == 0xffffffff
    assert wr.shift == 0
    assert wr.add_value == -0x3F_57_FF_FF
    assert wr.is_big == True

# Test decrement configuration
def test_dst_dec():
    p1 = [
        {
            'choice': 'ethernet',
            'ethernet': {}
        },
        {
            'choice': 'ipv4',
            'ipv4': {
                'dst': {
                    'choice': 'decrement',
                    'decrement': {'start': '192.168.0.1', 'step': '1.0.1.2', 'count': 200}
                }
            }
        }
    ]

    vm_cmds, pkt_headers, layers = SetConfig.set_packet_headers(p1)
    # Variable declaration
    var = vm_cmds[0]
    assert var.name == 'IP0_dst:0'
    assert var.size == 4
    assert var.op == 'dec'
    assert var.step == 0x01_00_01_02
    assert var.min_value == 0x37_FF_36_6F
    assert var.max_value == 0xFF_FF_FF_FF
    assert var.init_value == 0xFF_FF_FF_FF
    assert var.value_list == None
    # Writing variable
    wr = vm_cmds[1]
    assert wr.fv_name == 'IP0_dst:0'
    assert wr.offset_fixup == 0
    assert wr.pkt_offset == 'IP:0.dst'
    assert wr.pkt_cast_size == 4
    assert wr.mask == 0xffffffff
    assert wr.shift == 0
    assert wr.add_value == -0x3F_57_FF_FE
    assert wr.is_big == True

    # Test values configuration
def test_dst_vals():
    p1 = [
        {
            'choice': 'ethernet',
            'ethernet': {}
        },
        {
            'choice': 'ipv4',
            'ipv4': {
                'dst': {
                    'choice': 'values',
                    'values': [453143, '192.168.0.4', '10.0.0.1', '48.24.0.1']
                }
            }
        }
    ]

    vm_cmds, pkt_headers, layers = SetConfig.set_packet_headers(p1)
    # Variable declaration
    var = vm_cmds[0]
    assert var.name == 'IP0_dst:0'
    assert var.size == 4
    assert var.op == 'inc'
    assert var.step == 1
    assert var.min_value == None
    assert var.max_value == None
    assert var.init_value == None
    assert var.value_list == [0x00_06_EA_17, 0xC0_A8_00_04, 0x0A_00_00_01, 0x30_18_00_01]
    # Writing variable
    wr = vm_cmds[1]
    assert wr.fv_name == 'IP0_dst:0'
    assert wr.offset_fixup == 0
    assert wr.pkt_offset == 'IP:0.dst'
    assert wr.pkt_cast_size == 4
    assert wr.mask == 0xffffffff
    assert wr.shift == 0
    assert wr.add_value == 0
    assert wr.is_big == True

    # Test value configuration
def test_dst_val():
    p1 = [
        {
            'choice': 'ethernet',
            'ethernet': {}
        },
        {
            'choice': 'ipv4',
            'ipv4': {
                'dst': {
                    'choice': 'value',
                    'value': '16.0.0.1'
                }
            }
        }
    ]

    vm_cmds, pkt_headers, layers = SetConfig.set_packet_headers(p1)
    # Variable declaration
    var = vm_cmds[0]
    assert var.name == 'IP0_dst:0'
    assert var.size == 4
    assert var.op == 'inc'
    assert var.step == 1
    assert var.min_value == 0x10_00_00_01
    assert var.max_value == 0x10_00_00_01
    assert var.init_value == 0x10_00_00_01
    assert var.value_list == None
    # Writing variable
    wr = vm_cmds[1]
    assert wr.fv_name == 'IP0_dst:0'
    assert wr.offset_fixup == 0
    assert wr.pkt_offset == 'IP:0.dst'
    assert wr.pkt_cast_size == 4
    assert wr.mask == 0xffffffff
    assert wr.shift == 0
    assert wr.add_value == 0
    assert wr.is_big == True