[![Last Release](https://img.shields.io/github/tag/styx0x6/gremlins.svg?label=Release&colorB=34bf49)](https://github.com/styx0x6/gremlins)
[![Build Status](https://travis-ci.org/styx0x6/gremlins.svg?branch=master)](https://travis-ci.org/styx0x6/gremlins)
[![Python 3.4+](https://img.shields.io/badge/Python-3.4+-blue.svg)](https://www.python.org/)
[![License AGPL-3.0+](https://img.shields.io/badge/License-AGPL--3.0+-blue.svg)](https://raw.githubusercontent.com/styx0x6/gremlins/master/LICENSE)
[![Gitter Chat](https://img.shields.io/badge/Gitter-styx0x6%2fGremlins%20%e2%86%92-grey.svg?colorB=ed1965)](https://gitter.im/styx0x6/Gremlins)

French version here: [[README-FR](README-FR.md)]

# Gremlins

About
----

**Gremlins** is an open source tool made to help you to protect your privacy by keeping the little *gremlins* out of your stuff!

All started [here](http://seclists.org/fulldisclosure/2011/May/434) and with the "HADOPI" french law.

A lot of entities in the world, like the HADOPI agency in France by example, are spying your private and self-hosted
internet-fronted services, like file sharing, especially on BitTorrent, and others... The fundamentals rights that belong to
each one of us are obviously to be able to block any of these entities that would like to be too much curious on our
stuff, and also, prevent them to access our files and services based on our simple desire!

If you can prevent anyone to physicaly access your home, you must also be able to do the same on your internet-fronted
services.

The main purpose of this tool is to facilitate the blocking of these *gremlins* onto and from your BitTorrent services.

**How it works?**

The script build a blocking policy based on IPv4/IPv6 addresses from **iBlockList** and the **RIPE** database. Requests
are based on predefined keywords in order to don't block the whole internet... Then, it had the capability to
automatically set the blocking policy on many devices:

* Linux-based servers via **iptables**
* **Sophos UTM 9** firewall (v9.408+)
* **FreeboxOS** Download (v3+, APIv4) _- NOT YET IMPLEMENTED_
* NetGate **pfSense** firewall _- NOT YET IMPLEMENTED_
* Deciso **OPNsense** firewall _- NOT YET IMPLEMENTED_

Also, the script can simply generate the blocking list in CSV format:

    <CIDR_IP_RANGE>,<VERSION>,<SOURCE>,<MATCHED_KEYWORD>,<NAME>

_**Warning:**_

This tool has been made to help people to prevent them from being monitored by external entities (governmental or not).
You can protect, with the help of this tool, your sharing services in the same way you
would did it with your home against rubbers.

The fact of protecting your infrastructure and services from being stalked by strangers, named here *gremlins*, do
**NOT** allow you to share protected and copyrighted content without any permission. Gremlins developpers and
contributors are not responsible of your acts and they do **NOT** encourage you to do anything wrong or illegal.

_**The script doesn't guarantee a full protection against gremlins, the list isn't guaranteed as exhaustive as
it's generated from requests based on keywords. Also, it's possible that the generated list contains false-positives but
it's better to be safe than sorry.**_

Stay in the right way, do legal things, protect your privacy against *gremlins* and may the force be with you.

Installation
----

You can download the latest tarball by clicking [here](https://github.com/styx0x6/gremlins/tarball/master) or the
latest zipball by clicking [here](https://github.com/styx0x6/gremlins/zipball/master).

Preferably, you can download Gremlins by cloning the [Git](https://github.com/styx0x6/gremlins) repository:

    git clone --depth 1 https://github.com/styx0x6/gremlins.git gremlins

Gremlins works out of the box with [Python](http://www.python.org/download/) version **3.4** and more on any platform.
Libraries and dependancies are embedded within the script for better convenience.

Getting Started
----

`python gremlins.py [-v | -h] [-d] [-c] [-Dc] [-De] [-D4 | -D6] [-Dr, -Di] <command> [<command_options...>]`

![help](help.png)

`python gremlins.py list [-h]`

Links
----

* Homepage: https://github.com/styx0x6/gremlins
* Download: [.tar.gz](https://github.com/styx0x6/gremlins/tarball/master) or [.zip](https://github.com/styx0x6/gremlins/zipball/master)
* Git repository: git://github.com/styx0x6/gremlins.git
* Issues tracker: https://github.com/styx0x6/gremlins/issues

Roadmap & Changelog
----

All details are here: [[CHANGELOG](CHANGELOG.md)]

Contributing
----

Feel free to submit *issues* and enhancement *pull requests*!

[[Bugs & Support](https://github.com/styx0x6/gremlins/issues)]  
[[How to contribute to a project on Github](https://gist.github.com/MarcDiethelm/7303312)] by Marc Diethelm

*dev* branch status:  
[![Build Status](https://travis-ci.org/styx0x6/gremlins.svg?branch=dev)](https://travis-ci.org/styx0x6/gremlins)

Third-Party Libraries
----

* **Shields.io** - Badges as a service.

    ![License: CC0](https://img.shields.io/badge/License-CC0-lightgrey.svg)  
    [http://shields.io/](http://shields.io/)  
    [https://github.com/badges/shields/](https://github.com/badges/shields/)

Gremlins includes bundled packages and below are their associated licensing terms:

* **colorama-0.3.7** - The Colorama library located in `thirdparty/colorama/`.

    Copyright (C) 2013, Jonathan Hartley.  
    ![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-orange.svg)  
    [https://pypi.org/project/colorama/](https://pypi.org/project/colorama/)  
    [https://github.com/tartley/colorama/](https://github.com/tartley/colorama/)

* **paramiko-2.1.1** - The Paramiko library located in `thirdparty/paramiko/`.

    Copyright (C) 2003-2011, Robey Pointer.  
    Copyright (c) 2013-2018, Jeff Forcier.  
    ![License: LGPL](https://img.shields.io/badge/License-LGPL-blue.svg)  
    [http://www.paramiko.org/](http://www.paramiko.org/)  
    [https://github.com/paramiko/paramiko/](https://github.com/paramiko/paramiko/)

* **requests-2.13.0** - The Requests library located in `thirdparty/requests/`.

    Copyright (C) 2016, Kenneth Reitz.  
    ![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)  
    [http://docs.python-requests.org/](http://docs.python-requests.org/)  
    [https://github.com/requests/requests/](https://github.com/requests/requests/)
