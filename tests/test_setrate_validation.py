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

def test_setrate_good():
    rates = json.load(open('tests/data/setrate_validation_good.json'))
    for r in rates:
        Validation.validate_rate(r)

def test_setrate_bad():
    rates = json.load(open('tests/data/setrate_validation_bad.json'))
    for r in rates:
        with pytest.raises(SnappiTrexException):
            Validation.validate_rate(r)