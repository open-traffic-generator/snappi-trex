import sys, os
import dotenv
import json

dotenv.load_dotenv()

TREX_PATH = os.getenv('TREXPATH')
sys.path.insert(0, os.path.abspath(TREX_PATH))
sys.path.insert(0, os.path.abspath('.'))
from snappi_trex.setconfig import SetConfig

def test_setduration():
    durations = json.load(open('tests/data/setduration.json'))
    for d in durations:
        m = SetConfig.set_duration(duration=d['test'], pps=1000, bps=None, percent=None)
        assert m.to_json() == d['res']
