# Roadmap

## Features

### Milestone version 1.0.0

* Implement **iptables** support.
* Implement **Sophos UTM 9** support.

### Milestone version 1.1.0

* Implement **FreeboxOS Download** support.

### Others

* Implement **NetGate pfSense** support.
* Implement **Deciso OPNsense** support.
* Others ISP home box.

## Fixes & Improvments

* SSH with certificates support (implementation + helps to be reviewed).
* *List to complete...*

# Changelog

## Version 0.y.z (*Coming soon...*)

* Full RIPE database support.
* IPv6 full support.

## Version 0.1.0 (*Coming soon...*)

First release with standard features:

* Build for Python 3.4+ (v3.3 mandatory for ipaddress module, v3.4 mandatory for enum module and Paramiko...).
* PEP8 code style with docstring.
* Build under AGPL-3.0+ license.
* Core structure ready arguments parsing and next features.
* iBlockList support.
* Manage objects into an internal memory database.
* Format and manage IPs as CIDR.
* Display IPs in CSV format.
* Code ready for a full IPv4 and IPv6 support. IPv6 not yet fully supported.
* Properly manage stdout/stderr and colorization.
* Handling custom exceptions and error messages properly.
* Documentation with `-h, --help`.
* Setup Travis CI build validation.
