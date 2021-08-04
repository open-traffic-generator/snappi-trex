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

def test_setsize_good():
    sizes = json.load(open('tests/data/setsize_validation_good.json'))
    for s in sizes:
        Validation.validate_size(s)

def test_setsize_bad():
    sizes = json.load(open('tests/data/setsize_validation_bad.json'))
    for s in sizes:
        with pytest.raises(SnappiTrexException):
            Validation.validate_size(s)
