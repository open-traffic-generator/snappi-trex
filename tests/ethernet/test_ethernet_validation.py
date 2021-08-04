import sys, os
import dotenv
import pytest
import json

dotenv.load_dotenv()

TREX_PATH = os.getenv('TREXPATH')
sys.path.insert(0, os.path.abspath(TREX_PATH))
sys.path.insert(0, os.path.abspath('.'))
from snappi_trex.exceptions import SnappiTrexException
from snappi_trex.validation import Validation

def test_ethernet_dst_good():
    packets = json.load(open('tests/data/ethernet/ethernet_validation_good.json'))
    for p in packets:
        Validation.validate_packet(p)

def test_ethernet_dst_bad():
    packets = json.load(open('tests/data/ethernet/ethernet_validation_bad.json'))
    for p in packets:
        with pytest.raises(SnappiTrexException):
            Validation.validate_packet(p)
