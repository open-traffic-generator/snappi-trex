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

def test_setduration_good():
    durations = json.load(open('tests/data/setduration_validation_good.json'))
    for d in durations:
        Validation.validate_duration(d)

def test_setduration_bad():
    durations = json.load(open('tests/data/setduration_validation_bad.json'))
    for d in durations:
        with pytest.raises(SnappiTrexException):
            Validation.validate_duration(d)
