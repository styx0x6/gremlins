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

VERSION = "0.1.1"
VERSION_STRING = "%s/%s" % (PROJECT_TITLE, VERSION)
VALID_PYTHON_VERSION = "3.4"

AUTHOR = "@styx0x6"
AUTHOR_PAGE = "https://github.com/styx0x6"
HOME_PAGE = "https://github.com/styx0x6/gremlins"
ISSUES_PAGE = "https://github.com/styx0x6/gremlins/issues"
GIT_REPOSITORY = "git://github.com/styx0x6/gremlins.git"

"""
Gremlins static settings
"""
CMD_HELP = 'help'
CMD_LIST = 'list'
CMD_IPTABLES = 'iptables'
CMD_FBXOS = 'fbxos'
CMD_UTM9 = 'utm9'
CMD_PFSENSE = 'pfsense'
CMD_OPNSENSE = 'opnsense'

DEFAULT_SSH_PORT = '22'
DEFAULT_FBX_HOST = 'mafreebox.freebox.fr'
DEFAULT_FBX_HTTPS_PORT = '443'
DEFAULT_UTM9_HTTPS_PORT = '4444'
DEFAULT_PFSENSE_HTTPS_PORT = '443'
DEFAULT_OPNSENSE_HTTPS_PORT = '443'

# TODO Needed: CACHE_DIR = "cache"

# iBlockList static settings
IBL_HTTP_FILEFORMAT = 'p2p'
IBL_HTTP_ARCHIVEFORMAT = 'gz'
IBL_HTTP_URL = "http://list.iblocklist.com/index.php?list=%s&fileformat=%s&archiveformat=%s" \
               % ("%s", IBL_HTTP_FILEFORMAT, IBL_HTTP_ARCHIVEFORMAT)
IBL_LIST_ENC = 'utf-8'
IBL_SEP = ":"

# RIPE static settings
RIPE_HTTP_RESP_TYPE = 'json'
RIPE_HTTP_REST_URL = "https://rest.db.ripe.net/search.%s?query-string=%s&flags=no-filtering" \
                     % (RIPE_HTTP_RESP_TYPE, "%s")
RIPE_JSON_NAME_LIST = ['netname', 'descr']
RIPE_JSON_INETNUM = 'inetnum'

# Information gathering settings
IBL_LISTS = ['bt_level1', 'bt_level2']
KEYWORDS_LIST = ["hadopi", "tmg", "trident mediguard", "trident mediaguard", "trident medi guard",
                 "trident media guard"]

# iptables commands
IPTABLES_DROP = ""
IPTABLES_SAVE = ""

"""
Gremlins outputs settings
"""
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
Help definitions
"""
HELP = """
Usage: %s [-v | -h] [-d] [-c] [-Dc] [-De] [-D4 | -D6] [-Dr, -Di] <command> [<command_options...>]

Options:

  -v, --version                 Show version and exit
  -h, --help                    Show this help message

  -d, --debug                   Enable verbose outputs
  -c, --clean-output            Do not show running output, keep only some commands results
  -Dc, --disable-coloring       Disable terminal coloring
  -De, --disable-error          Disable error messages

  -D4, --disable-ipv4           Disable IPv4 (TO BE IMPLEMENTED)
  -D6, --disable-ipv6           Disable IPv6 (TO BE IMPLEMENTED)

  -Dr, --disable-ripe           Disable RIPE database searching requests
  -Di, --disable-iblocklist     Disable iBlockList download requests

Commands:

  list                          Show the CIDR IP addresses list
  iptables                      Push iptables blocking ruleset
  fbxos (NYI)                   Push FreeboxOS Download Blacklist blocking ruleset (v3+, APIv4)
  utm9                          Push Sophos UTM 9 firewall blocking ruleset (v9.408+)
  pfsense (NYI)                 Push NetGate pfSense firewall blocking ruleset
  opnsense (NYI)                Push Deciso OPNsense firewall blocking ruleset

  For further details about commands, use: %s <command> -h.

"""

HELP_LIST = """
Usage: %s %s [-h]

Show the CIDR IP addresses list. Print each line in CSV format:

  <CIDR_IP_RANGE>,<VERSION>,<SOURCE>,<MATCHED_KEYWORD>,<NAME>

    where <VERSION> is '4' or '6'
    where <SOURCE> is 'RIPE','bt_level1'...

Options:

  -h, --help                    Show this help message

"""

HELP_IPTABLES = """
Usage: %s %s [-h] [-l] [-H <host> [-P <port>] [-u <user> -p <password>] [-Ds]]

Push iptables blocking ruleset using CLI via SSH.

Options:

  -h, --help                    Show this help message
  -l, --list                    List only the iptables commands, will not push them
  -H, --host                    The remote server hostname or IP address
  -P, --port                    The remote server SSH port, '22' by default
  -u, --user                    The username used to connect and push commands on the remote server
  -p, --password                The user's password to connect on the remote server
  -Ds, --do-not-save            Will not save the pushed commands, thus configuration will not be persistent

"""

HELP_FBXOS = """
Usage: %s %s [-h] [-H <host> [-P <port>] -u <user> -p <password>]

/!\ NOT YET IMPLEMENTED /!\\

Push FreeboxOS Download Blacklist blocking ruleset using the REST API (Freebox Revolution v3+, APIv4).

Options:

  -h, --help                    Show this help message
  -H, --host                    The remote Freebox hostname or IP address, 'mafreebox.freebox.fr' by default
  -P, --port                    The remote Freebox HTTPS port, '443' by default
  -u, --user                    The authentication username to get the token challenge
  -p, --password                The user's password to get the token challenge

"""

HELP_UTM9 = """
Usage: %s %s [-h] [-H <host> [-P <port>] [-t <REST token ID>] [-u <user> -p <password>] [-Dl]]

Push Sophos UTM 9 firewall blocking ruleset using the REST API (v9.408+).

Options:

  -h, --help                    Show this help message
  -H, --host                    The remote Sophos UTM 9 firewall hostname or IP address
  -P, --port                    The remote Sophos UTM 9 firewall HTTPS port, '4444' by default
  -t, --token                   The REST authentication token ID, if do not use user/password credentials
  -u, --user                    The authentication username on the REST service, if do not use a token ID
  -p, --password                The user's password to be authenticated on the REST service with credentials
  -Dl, --do-not-log             Set the generated rules with no logging

"""

HELP_PFSENSE = """
Usage: %s %s [-h] [-H <host> [-P <port>] [-u <user> -p <password>] [-Dl]]

/!\ NOT YET IMPLEMENTED /!\\

Push pfSense firewall blocking ruleset using the REST API.

Options:

  -h, --help                    Show this help message
  -H, --host                    The remote pfSense firewall hostname or IP address
  -P, --port                    The remote pfSense firewall HTTPS port, '443' by default
  -u, --user                    The authentication username to get the token challenge
  -p, --password                The user's password to get the token challenge
  -Dl, --do-not-log             Set the generated rules with no logging

"""

HELP_OPNSENSE = """
Usage: %s %s [-h] [-H <host> [-P <port>] [-u <user> -p <password>] [-Dl]]

/!\ NOT YET IMPLEMENTED /!\\

Push OPNsense firewall blocking ruleset using the REST API.

Options:

  -h, --help                    Show this help message
  -H, --host                    The remote OPNsense firewall hostname or IP address
  -P, --port                    The remote OPNsense firewall HTTPS port, '443' by default
  -u, --user                    The authentication username to get the token challenge
  -p, --password                The user's password to get the token challenge
  -Dl, --do-not-log             Set the generated rules with no logging

"""
