#!/usr/bin/env python

# Copyright (C) 2017  @styx0x6
#
# This file is part of Gremlins.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# TODO link information details to those into __init__.py
PROJECT_NAME = "Gremlins"
PROJECT_TITLE = "gremlins"
DESCRIPTION = "Protect your privacy, protect from gremlins!"
DESCRIPTION_2 = "Keep gremlins out of your stuff!"
LICENSE = "GNU Affero General Public License (AGPL-3.0+)"
LICENSE_SHORT = "AGPL-3.0+"
COPYRIGHT = "Copyright (C) 2017 @styx0x6"

VERSION = "0.1.0"
VERSION_STRING = "%s/%s" % (PROJECT_TITLE, VERSION)
VALID_PYTHON_VERSION = "3.3"

CACHE_DIR = "cache"

AUTHOR = "@styx0x6"
AUTHOR_PAGE = "https://github.com/styx0x6"
HOME_PAGE = "https://github.com/styx0x6/gremlins"
ISSUES_PAGE = "https://github.com/styx0x6/gremlins/issues"
GIT_REPOSITORY = "git://github.com/styx0x6/gremlins.git"

# TODO add author, desc, others? contibutors?
BANNER = """
%sGremlins%s %s%s%s - %s

Home page: %s
Report bugs at: %s
Author: %s, License: %s
""" % ("%s", "%s", "%s", VERSION, "%s", DESCRIPTION_2, HOME_PAGE, ISSUES_PAGE, AUTHOR, LICENSE_SHORT)

HELP = """
Usage: %s [-v | -h] [-c, -Dc] [-Dr, -Di] <command> [<command_options...>]

Options:

  -v, --version                 Show version and exit
  -h, --help                    Show this help message

  -c, --clean-output            Do not show running output, keep only some commands results
  -Dc, --disable-coloring       Disable terminal coloring

  -Dr, --disable-ripe           Disable RIPE database searching requests
  -Di, --disable-iblocklist     Disable iBlockList download requests

Commands:

  list                          Show the CIDR IP addresses list
  iptables                      Push iptables blocking ruleset
  fbxos (TBI)                   Push FreeboxOS Download Blacklist blocking ruleset (v3+)
  utm9                          Push Sophos UTM 9 Firewall blocking ruleset (v9.408+)
  pfsense (TBI)                 Push NetGate pfSense firewall blocking ruleset
  opnsense (TBI)                Push Deciso OPNsense Firewall blocking ruleset

  For further details about commands, use: %s <command> -h
"""

# TODO Detail args and add long args
# TODO Detail output format
HELP_LIST = """
Usage: %s %s [-h]

Show the CIDR IP addresses list
"""

# TODO Detail args and add long args
HELP_IPTABLES = """
Usage: %s %s [-h] [-l] [-H <host> [-P <port>] [-u <user> -p <password>] [-Ds]]

Push iptables blocking ruleset
"""

# TODO Detail args and add long args
# TODO TO BE IMPLEMENTED
HELP_FBXOS = """
Usage: %s %s [-h] [-H <host> [-P <port>] -u <user> -p <password>] [-s]

Push FreeboxOS Download Blacklist blocking ruleset (Freebox Revolution v3) - TO BE IMPLEMENTED
"""

# TODO Detail args and add long args
HELP_UTM9 = """
Usage: %s %s [-h] [-H <host> [-P <port>] [-t <REST token ID>] [-u <user> -p <password>] [-Dl]]

Push Sophos UTM 9 Firewall blocking ruleset (v9.408+)
"""

# TODO Detail args and add long args
# TODO TO BE IMPLEMENTED
HELP_PFSENSE = """
Usage: %s %s [-h] [-H <host> [-P <port>] [-u <user> -p <password>] [-Dl]]

Push pfSense firewall blocking ruleset - TO BE IMPLEMENTED
"""

# TODO Detail args and add long args
# TODO TO BE IMPLEMENTED
HELP_OPNSENSE = """
Usage: %s %s [-h] [-H <host> [-P <port>] [-u <user> -p <password>] [-Dl]]

Push OPNsense Firewall blocking ruleset - TO BE IMPLEMENTED
"""
