import sys, os
import dotenv
import json

dotenv.load_dotenv()

TREX_PATH = os.getenv('TREXPATH')
sys.path.insert(0, os.path.abspath(TREX_PATH))
sys.path.insert(0, os.path.abspath('.'))
from snappi_trex.setconfig import SetConfig

def test_dst():
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
        # Writing bytes 4:7
        wr_4_7 = vm_cmds[1]
        res_wr_4_7 = p['res'][1]
        assert wr_4_7.fv_name == res_wr_4_7['fv_name']
        assert wr_4_7.offset_fixup == res_wr_4_7['offset_fixup']
        assert wr_4_7.pkt_offset == res_wr_4_7['pkt_offset']
        assert wr_4_7.pkt_cast_size == res_wr_4_7['pkt_cast_size']
        assert wr_4_7.mask == res_wr_4_7['mask']
        assert wr_4_7.shift == res_wr_4_7['shift']
        assert wr_4_7.add_value == res_wr_4_7['add_value']
        assert wr_4_7.is_big == res_wr_4_7['is_big']
        # Writing bytes 3
        wr_3 = vm_cmds[2]
        res_wr_3 = p['res'][2]
        assert wr_3.fv_name == res_wr_3['fv_name']
        assert wr_3.offset_fixup == res_wr_3['offset_fixup']
        assert wr_3.pkt_offset == res_wr_3['pkt_offset']
        assert wr_3.pkt_cast_size == res_wr_3['pkt_cast_size']
        assert wr_3.mask == res_wr_3['mask']
        assert wr_3.shift == res_wr_3['shift']
        assert wr_3.add_value == res_wr_3['add_value']
        assert wr_3.is_big == res_wr_3['is_big']
        # Writing bytes 2
        wr_2 = vm_cmds[3]
        res_wr_2 = p['res'][3]
        assert wr_2.fv_name == res_wr_2['fv_name']
        assert wr_2.offset_fixup == res_wr_2['offset_fixup']
        assert wr_2.pkt_offset == res_wr_2['pkt_offset']
        assert wr_2.pkt_cast_size == res_wr_2['pkt_cast_size']
        assert wr_2.mask == res_wr_2['mask']
        assert wr_2.shift == res_wr_2['shift']
        assert wr_2.add_value == res_wr_2['add_value']
        assert wr_2.is_big == res_wr_2['is_big']
        # Writing bytes 1
        wr_1 = vm_cmds[4]
        res_wr_1 = p['res'][4]
        assert wr_1.fv_name == res_wr_1['fv_name']
        assert wr_1.offset_fixup == res_wr_1['offset_fixup']
        assert wr_1.pkt_offset == res_wr_1['pkt_offset']
        assert wr_1.pkt_cast_size == res_wr_1['pkt_cast_size']
        assert wr_1.mask == res_wr_1['mask']
        assert wr_1.shift == res_wr_1['shift']
        assert wr_1.add_value == res_wr_1['add_value']
        assert wr_1.is_big == res_wr_1['is_big']
        # Writing bit 0
        wr_0 = vm_cmds[5]
        res_wr_0 = p['res'][5]
        assert wr_0.fv_name == res_wr_0['fv_name']
        assert wr_0.offset_fixup == res_wr_0['offset_fixup']
        assert wr_0.pkt_offset == res_wr_0['pkt_offset']
        assert wr_0.pkt_cast_size == res_wr_0['pkt_cast_size']
        assert wr_0.mask == res_wr_0['mask']
        assert wr_0.shift == res_wr_0['shift']
        assert wr_0.add_value == res_wr_0['add_value']
        assert wr_0.is_big == res_wr_0['is_big']
