[<< snappi-trex TOC](../README.md#Table-of-Contents)

# Testing

This document outlines the test methodology used in snappi-trex.

* snappi-trex uses [pytest](https://docs.pytest.org/en/6.2.x/contents.html) in order to carry out its unit tests.
* All test scripts are located in the `tests` folder.

## Integration Tests
* In order to execute the integration tests, TRex must be running with `port 0` on one end of a virtual ethernet, and `port 1` on the other end of the virtual ethernet. (`port 1` sends to `port 2`)
    * for help setting this up, follow my [TRex Tutorial](trex-tutorial.md)
* The test works by capturing the transmit from `port 0` to `port 1` with a given snappi configuration, then comparing the capture bytes with a pcap file containing the expected capture bytes.
    * pcap files are stored in `tests/data/pcap`
* Run unit tests using
```sh
pytest -v
```
* All end to end tests are located in `tests/test_end_to_end.py`

### Adding Integration Tests
In order to add an integration test, somewhere in `tests/data`, create a new `json` file. 
* (Ex. `udp` end to end tests are located in `tests/data/udp/udp.json`. `ipv4` end to end tests are located in `tests/data/ipv4/ipv4.json`)

These `json` files follow the following format:
```
[
  # Test #1
  {
    "res": "{path to pcap file containing expected result}",
    "test": {serialized snappi config to run}
  },
  # Test #2
  {
    "res": "{path to pcap file containing expected result}",
    "test": {serialized snappi config to run}
  },

  ...

  # Test #n
  {
    "res": "{path to pcap file containing expected result}",
    "test": {serialized snappi config to run}
  }
]
```
See `tests/data/udp/udp.json` for- example reference.

Now, add a test to `tests/test_end_to_end.py`. The test follows the following format:
```
def test_{name of test}():
    tests = json.load(open({path to json test file}))
    run_tests(tests)
```

Here is an example for `test_udp`.
```
def test_udp():
    tests = json.load(open('tests/data/udp/udp.json'))
    run_tests(tests)
```