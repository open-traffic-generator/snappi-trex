import sys, os
import dotenv
import pytest
import json
import snappi

dotenv.load_dotenv()

TREX_PATH = os.getenv('TREXPATH')
sys.path.insert(0, os.path.abspath(TREX_PATH))
sys.path.insert(0, os.path.abspath('.'))
from snappi_trex.exceptions import SnappiTrexException
from snappi_trex.validation import Validation

port_list = ["p1", "p2", "p3", "p4"]

def test_setcapture_good():
    api = snappi.api()
    captures = json.load(open('tests/data/setcapture_validation_good.json'))
    for c in captures:
        cs = api.capture_state()
        cs.state = c['state']
        cs.port_names = c['port_names']
        Validation.validate_capture(cs, port_list)

def test_setcapture_bad():
    api = snappi.api()
    captures = json.load(open('tests/data/setcapture_validation_bad.json'))
    for c in captures:
        with pytest.raises(SnappiTrexException):
            cs = api.capture_state()
            cs.state = c['state']
            cs.port_names = c['port_names']
            Validation.validate_capture(cs, port_list)
