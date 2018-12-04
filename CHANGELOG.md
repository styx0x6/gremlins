# Roadmap

## Features

* Implement **NetGate pfSense** support.
* Implement **Deciso OPNsense** support.
* Others ISP home box.
* FreeboxOS One/Delta (API v5?) support.
* Deluge/uTorrent IPBlock auto configuration support.

## Fixes & Improvments

* SSH with certificates support (implementation + helps to be reviewed).
* A better management of keywords to include, with easy customization.
* Upgrade third-party libraries.
* iptables: add an option for logging `-l, --log` and logging path `--log-path`.

# Changelog

## Version 1.0.0 (*Coming soon...*)

* Full RIPE database support. *TODO*
* IPv6 full support. *TODO*
* Implemented **iptables** support. *IN PROGRESS*
* Implemented **Sophos UTM 9** support. *TODO*
* Implemented **FreeboxOS Download** support. *TODO*
* Added a french version of the README file.
* Added Travis build notifications on gitter (https://gitter.im/styx0x6/Gremlins).
* Reviewed README file with more running details and fixes.

## Version 0.1.1 (2018-11-03)

* Removed Python 3.7 from Travis CI build validation.

## Version 0.1.0 (2018-11-03)

First release with standard features:

* Build for Python 3.4+ (v3.3 mandatory for ipaddress module, v3.4 mandatory for enum module and Paramiko...).
* PEP8 code style with docstring.
* Build under AGPL-3.0+ license.
* Core structure ready arguments parsing and next features.
* iBlockList support.
* Format and manage IPs as CIDR.
* Display IPs in CSV format.
* Manage objects into an internal memory database.
* Code ready for a full IPv4 and IPv6 support. IPv6 not yet fully supported.
* Properly manage stdout/stderr and colorization.
* Handling custom exceptions and error messages properly.
* Documentation with `-h, --help`.
* Setup Travis CI build validation.
