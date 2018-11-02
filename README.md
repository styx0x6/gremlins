[![Python 3.3+](https://img.shields.io/badge/Python-3.3+-blue.svg)](https://www.python.org/)
[![License AGPL-3.0+](https://img.shields.io/badge/License-AGPL--3.0+-blue.svg)](https://raw.githubusercontent.com/styx0x6/gremlins/master/LICENSE)

# Gremlins

About
----

**Gremlins** is an open source tool made to help you to protect your privacy by keeping *gremlins* out of your stuff!

A lot of entities in the world are spying your private and/or self-hosted internet-fronted services like file sharing
(mainly using BitTorrent) and others... The fundamentals rights that belong to each one of us are to obviously be able
to block anyone or any entity that would like to be a little bit more curious on our stuff, and prevent them to access
our services by our simple desire!

If you can prevent anyone to physicaly access your home, you must be able to do the same on your internet-fronted
services!

_**How it works?**_

The script build a blocking policy based on IPv4/IPv6 addresses. The main feature is the capability to automatically
set the blocking policy on many devices:

* Linux-based servers via **iptables**
* **Sophos UTM 9** firewall (v9.408+)
* **FreeboxOS** Download (v3+, APIv4) *- NOT YET IMPLEMENTED*
* NetGate **pfSense** firewall *- NOT YET IMPLEMENTED*
* Deciso **OPNsense** firewall *- NOT YET IMPLEMENTED*

Also the script can simply generate the list to block in CSV format:

    <CIDR_IP_RANGE>,<VERSION>,<SOURCE>,<MATCHED_KEYWORD>,<NAME>

*Workflow:*

1. iBlockList and RIPE database requests based on predefined keywords in order to not block all the internet.
2. Format IPs in a standard way.
3. Do what you want: list IPs, set rulesets on devices (iptables, firewalls...).

*Additional information:*

_**The script doesn't guarantee a full protection from gremlins, the list isn't guaranteed as exhaustive as
it's generated from requests based on keywords. Also, it's possible that the generated list contains false-positive but
it's better to be safe than sorry.**_

**Warning:**

This tool has been made to prevent from being monitored by external entities, govermental or not, as if you would been
protected from rubbers, you can can protect your sharing services as you would did it for your home.

The fact of protecting you infrastructure/services for being stalked by strangers, named here *gremlins*, do **NOT**
allow you to share protected and copyrighted content. Gremlins' developpers and contributors are not responsible of
your acts and we do **NOT** encourage you to do anything wrong or illegal.

Stay in the right way, do only legal things, protect your privacy from *gremlins* and may the force be with you.

Installation
----

You can download the latest tarball by clicking [here](https://github.com/styx0x6/gremlins/tarball/master) or the
latest zipball by clicking  [here](https://github.com/styx0x6/gremlins/zipball/master).

Preferably, you can download Gremlins by cloning the [Git](https://github.com/styx0x6/gremlins) repository:

    git clone --depth 1 https://github.com/styx0x6/gremlins.git gremlins

Gremlins works out of the box with [Python](http://www.python.org/download/) version **3.3** and more on any platform.
Libraries and dependancies are embedded within the software.

Getting Started
----

*Coming soon...*

Links
----

* Homepage: https://github.com/styx0x6/gremlins
* Download: [.tar.gz](https://github.com/styx0x6/gremlins/tarball/master) or [.zip](https://github.com/styx0x6/gremlins/zipball/master)
* Git repository: git://github.com/styx0x6/gremlins.git
* Issues tracker: https://github.com/styx0x6/gremlins/issues

References
----

Some interesting links:

* [http://seclists.org/fulldisclosure/2011/May/434](http://seclists.org/fulldisclosure/2011/May/434)

Third-Party Librairies
----

Gremlins includes bundled packages and here are their associated licensing terms.

* **colorama-0.3.7** - The Colorama library located under `thirdparty/colorama/`.

    Copyright (C) 2013, Jonathan Hartley, BSD 3-Clause license.  
    [https://pypi.python.org/pypi/colorama/](https://pypi.python.org/pypi/colorama/)

* **paramiko-2.1.1** - The Paramiko library located under `thirdparty/paramiko/`.

    Copyright (C) 2003-2011, Robey Pointer, LGPL license.  
    [http://www.paramiko.org/](http://www.paramiko.org/)

* **requests-2.13.0** - The Requests library located under `thirdparty/requests/`.

    Copyright (C) 2016, Kenneth Reitz, Apache 2.0 license.  
    [http://docs.python-requests.org/](http://docs.python-requests.org/)
