[<< snappi-trex TOC](../README.md#Table-of-Contents)

# Contribute

## Report a bug

To report a bug, [open an issue](https://github.com/open-traffic-generator/snappi-trex/issues) on the snappi-trex github repo

## Adding features/Modifying code

* Fork the [snappi-trex github repo](https://github.com/open-traffic-generator/snappi-trex)
* Modify your forked snappi-trex repo
* Submit a [pull request](https://github.com/open-traffic-generator/snappi-trex/pulls) with the main repository

## Adding support for new protocol headers

To add support for other protocol headers, simply modify `get_header_info()` in `snappi_trex/info.py`. Instructions can be found in the file.

* All supportable protocol headers and header fields must be supported in [Scapy](https://scapy.net).
* Some protocol fields require special cases if they do not follow the typical `value`, `values`, `increment`, or `decrement` options.
    * Ex. `checksum` does not have typical value options. `checksum` is either `generated` or `custom`

## Adding integration tests

See [testing.md](testing.md) for instructions

## Unsupported features

There are many snappi features that are currently not supported by snappi-trex. This is where the community can start to contribute by implementing these features. (Ex. custom checksums is a snappi feature that isn't supported in snappi-trex)
* See [features.md](features.md) for a full list of snappi features that are unsupported in snappi-trex.