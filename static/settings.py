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


# TODO link information details to those into __init__.py?
"""
Gremlins project settings
"""
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

AUTHOR = "@styx0x6"
AUTHOR_PAGE = "https://github.com/styx0x6"
HOME_PAGE = "https://github.com/styx0x6/gremlins"
ISSUES_PAGE = "https://github.com/styx0x6/gremlins/issues"
GIT_REPOSITORY = "git://github.com/styx0x6/gremlins.git"

"""
Gremlins static settings
"""
CMD_LIST = 'list'
CMD_IPTABLES = 'iptables'
CMD_FBXOS = 'fbxos'
CMD_UTM9 = 'utm9'
CMD_PFSENSE = 'pfsense'
CMD_OPNSENSE = 'opnsense'

DEFAULT_SSH_PORT = '22'
DEFAULT_FBX_HTTP_PORT = '80'
# TODO Needed: DEFAULT_FBX_HTTPS_PORT = '48597' ?
DEFAULT_UTM9_HTTPS_PORT = '4444'
DEFAULT_PFSENSE_HTTPS_PORT = '443'
DEFAULT_OPNSENSE_HTTPS_PORT = '443'

# TODO Needed: CACHE_DIR = "cache"

"""
Gremlins outputs settings
"""
# Static variables
STDOUT = 0  # defines stdout within Gremlins
STDERR = 1  # defines stderr within Gremlins
OK = True
NOK = False

# Static strings definition
STR_OK = "OK!"
STR_NOK = "NOK"
STR_ERR = "[ERR]"
STR_DEBUG = "[%s] "  # debug information shall be provided here

# Default parameters for outputs
DEFAULT_COLORIZE_OUTPUT = True  # by default, output is colorized
DEFAULT_SHOW_RUNNING_OUTPUT = True  # by default, running output messages are shown
DEFAULT_SHOW_DEBUG_INFO = False  # by default, debug information is not shown
DEFAULT_SHOW_RUNNING_ERROR = True  # by default, running error messages are shown

"""
Banner definition
"""
BANNER = """
%sGremlins%s %s%s%s - %s

Home page: %s
Report bugs at: %s
Author: %s, License: %s
""" % ("%s", "%s", "%s", VERSION, "%s", DESCRIPTION_2, HOME_PAGE, ISSUES_PAGE, AUTHOR, LICENSE_SHORT)

"""
Help definition
"""
HELP = """
Usage: %s [-v | -h | -d] [-c, -Dc] [-Dr, -Di] <command> [<command_options...>]

Options:

  -v, --version                 Show version and exit
  -h, --help                    Show this help message
  -d, --debug                   Enable verbose outputs

  -c, --clean-output            Do not show running output, keep only some commands results
  -Dc, --disable-coloring       Disable terminal coloring

  -Dr, --disable-ripe           Disable RIPE database searching requests
  -Di, --disable-iblocklist     Disable iBlockList download requests

Commands:

  list                          Show the CIDR IP addresses list.
  iptables                      Push iptables blocking ruleset
  fbxos (TBI)                   Push FreeboxOS Download Blacklist blocking ruleset (v3+)
  utm9                          Push Sophos UTM 9 Firewall blocking ruleset (v9.408+)
  pfsense (TBI)                 Push NetGate pfSense firewall blocking ruleset
  opnsense (TBI)                Push Deciso OPNsense Firewall blocking ruleset

  For further details about commands, use: %s <command> -h
"""

HELP_LIST = """
Usage: %s %s [-h]

Show the CIDR IP addresses list. Print each line in CSV format "<NAME>,<CIDR_IP_RANGE>".

Options:

  -h, --help                    Show this help message
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
