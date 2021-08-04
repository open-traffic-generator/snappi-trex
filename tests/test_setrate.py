import sys, os
import dotenv
import json

dotenv.load_dotenv()

TREX_PATH = os.getenv('TREXPATH')
sys.path.insert(0, os.path.abspath(TREX_PATH))
sys.path.insert(0, os.path.abspath('.'))
from snappi_trex.setconfig import SetConfig

def test_setrate():
    rates = json.load(open('tests/data/setrate.json'))
    for r in rates:
        assert SetConfig.set_rate(r['test']) == tuple(r['res'])
