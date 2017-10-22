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

import os
import sys
import argparse
import gzip
import unicodedata
import ipaddress

from static.settings import *
from static import error

from lib.thirdparty import colorama
from lib.thirdparty import requests

PYTHON_VERSION = sys.version.split()[0]

# Python version check
if PYTHON_VERSION < VALID_PYTHON_VERSION:
    # TODO raise RuntimeError('')?
    sys.stderr.write(error.ERROR_CRITICAL_VERSION % (PYTHON_VERSION, VALID_PYTHON_VERSION, PROJECT_NAME))
    sys.stderr.write("\n")
    exit(error.ERROR_CODE_VERSION)

OS_IS_WIN = True if os.name is 'nt' else False
OS_IS_POSIX = True if os.name is 'posix' else False
BASENAME_PATH = os.path.basename(sys.argv[0])
BASENAME_PROG = ("python " if OS_IS_WIN else "") + ("\"%s\"" % BASENAME_PATH if " " in BASENAME_PATH else BASENAME_PATH)

# Gremlins static settings
CMD_LIST = 'list'
CMD_IPTABLES = 'iptables'
CMD_FBXOS = 'fbxos'
CMD_UTM9 = 'utm9'
CMD_PFSENSE = 'pfsense'
CMD_OPNSENSE = 'opnsense'

OK = "OK!"
NOK = "NOK"

DEFAULT_SSH_PORT = '22'
DEFAULT_FBX_HTTP_PORT = '80'
DEFAULT_FBX_HTTPS_PORT = '48597'
DEFAULT_UTM9_HTTPS_PORT = '4444'
DEFAULT_PFSENSE_HTTPS_PORT = '443'
DEFAULT_OPNSENSE_HTTPS_PORT = '443'

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


def iprange_to_cidr(ip_range=None):
    """
    Format an IP range addresses string given as "start to end" format ('x.x.x.x-y.y.y.y') to its corresponding CIDR list.
    :param ip_range: IP range addresses string given as "start to end" format ('x.x.x.x-y.y.y.y').
    :return: IP range addresses string as its corresponding CIDR string list.
    """
    cidr_ip_range_list = []
    ip_start, ip_end = ip_range.split("-")
    try:
        cidr_ip_range_list.extend(net.with_prefixlen for net in
                                  ipaddress.summarize_address_range(ipaddress.IPv4Address(ip_start),
                                                                    ipaddress.IPv4Address(ip_end)))
    except ipaddress.AddressValueError as ave:
        raise ave
    except ipaddress.NetmaskValueError as nve:
        raise nve
    except ValueError as ve:
        raise ve
    except TypeError as te:
        raise te
    return cidr_ip_range_list


def get_ibl_list(color=True, run_output=True, keywords_list=[], ibl_lists=[]):
    """
    Get the formatted list from iBlockList. Formatted as [('BAD IPs', 'x.x.x.x/y'),...].
    :param color: Colorized stdout. True by default.
    :param run_output: Show running output in stdout. True by default.
    :param keywords_list: The keywords list to search for gremlins.
    :param ibl_lists: The iBlockList list to parse.
    :return: The formatted iBlockList list as [('BAD IPs', 'x.x.x.x/y'),...].
    """
    ibl_list = []

    if run_output:
        sys.stdout.write("\n")

    for _list in ibl_lists:
        if run_output:
            sys.stdout.write("[get_ibl_list] Get list '%s' from iBlockList... " % _list)
        r = requests.get(IBL_HTTP_URL % _list)
        # Check HTTP response code
        if r.status_code == requests.codes.ok:
            if run_output:
                sys.stdout.write(((colorama.Fore.GREEN + OK + colorama.Style.RESET_ALL) if color else OK))
                sys.stdout.write((" - Downloaded file size: %sMB"
                                  % round((int(r.headers.get('content-length')) / 1024 / 1024), 2)) + "\n")

            # Decompress, decode as UTF-8 string, and split based on the end of line
            working_list = []
            if r.headers.get('content-type') == 'application/x-gzip':
                if run_output:
                    sys.stdout.write("[get_ibl_list] Decompress and decode file...           ")
                working_list = gzip.decompress(r.content).decode(encoding=IBL_LIST_ENC).split("\n")
                if run_output:
                    sys.stdout.write(((colorama.Fore.GREEN + OK + colorama.Style.RESET_ALL) if color else OK) + "\n")
            # case below should never occurs
            elif r.headers.get('content-type') == 'gzip':
                if run_output:
                    sys.stdout.write("[get_ibl_list] Decode file...                   ")
                working_list = r.content.decode(encoding=IBL_LIST_ENC).split("\n")
                if run_output:
                    sys.stdout.write(((colorama.Fore.GREEN + OK + colorama.Style.RESET_ALL) if color else OK) + "\n")
            else:
                # TODO raise Unexpected format downloaded
                pass

            # Parse for concerned lines
            if run_output:
                sys.stdout.write("[get_ibl_list] Parse '%s' from iBlockList...    " % _list)
            # remove the 2 first header lines from the blocking list
            working_list = working_list[2:]
            for line in working_list:
                # http://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison-in-python
                if any(word in unicodedata.normalize("NFKD", line.casefold()) for word in keywords_list):
                    #  format entries
                    name, i = line.split(IBL_SEP)
                    cidr_ip_range_list = iprange_to_cidr(i)
                    for cidr_ip_range in cidr_ip_range_list:
                        #  clean duplicate entries
                        if (name, cidr_ip_range) not in ibl_list:
                            ibl_list.extend([(name, cidr_ip_range)])
            if run_output:
                sys.stdout.write(((colorama.Fore.GREEN + OK + colorama.Style.RESET_ALL) if color else OK) + "\n")
        else:
            # TODO raise not 200 OK response after sys.stdout
            if run_output:
                sys.stdout.write(((colorama.Fore.RED + NOK + colorama.Style.RESET_ALL) if color else NOK) + "\n")

    return ibl_list


# TODO RIPE list to finish
def get_ripe_list(color=True, run_output=True, keywords_list=[]):
    """
    Get the formatted list from the RIPE. Formatted as [('BAD IPs', 'x.x.x.x/y'),...].
    :param color: Colorized stdout. True by default.
    :param run_output: Show running output in stdout. True by default.
    :param keywords_list: The keywords list to search for gremlins.
    :return: The formatted RIPE list as [('BAD IPs', 'x.x.x.x/y'),...].
    """
    ripe_list = []

    if run_output:
        sys.stdout.write("\n")

    for _word in keywords_list:
        if run_output:
            sys.stdout.write("[get_ripe_list] Requesting RIPE for '%s'... " % _word)

        r = requests.get(RIPE_HTTP_REST_URL % _word)

        # Check HTTP response code
        if r.status_code == requests.codes.ok:
            if run_output:
                sys.stdout.write(((colorama.Fore.GREEN + OK + colorama.Style.RESET_ALL) if color else OK) + "\n")

            # Parse the JSON response
            working_list = []
            if r.headers.get('content-type') == 'application/json':
                if run_output:
                    sys.stdout.write("[get_ripe_list] Parsing the JSON response... ")
                # TODO TODOTODOTODOTODOTODO
                """
                dict_parsed_json = r.json()
                if dict_parsed_json !=
                print(dict_parsed_json['objects'].)
                """
                if run_output:
                    sys.stdout.write(((colorama.Fore.GREEN + OK + colorama.Style.RESET_ALL) if color else OK) + "\n")
            # case below should never occurs
            else:
                # TODO raise Unexpected format received
                pass

            # Parse for concerned lines
            if run_output:
                sys.stdout.write("[get_ripe_list] Parse '%s' from iBlockList... " % _list)
            # remove the 2 first header lines from the blocking list
            working_list = working_list[2:]
            for line in working_list:
                # http://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison-in-python
                if any(word in unicodedata.normalize("NFKD", line.casefold()) for word in keywords_list):
                    #  format entries
                    name, ip_range = line.split(IBL_SEP)
                    # TODO format as cidr
                    #  clean duplicate entries
                    if (name, ip_range) not in ripe_list:
                        ripe_list.extend([(name, ip_range)])
            if run_output:
                sys.stdout.write(((colorama.Fore.GREEN + OK + colorama.Style.RESET_ALL) if color else OK) + "\n")
        else:
            # TODO raise not 200 OK response after sys.stdout
            if run_output:
                sys.stdout.write(((colorama.Fore.RED + NOK + colorama.Style.RESET_ALL) if color else NOK) + "\n")

            if r.status_code == requests.codes.bad_request:
                # TODO Illegal input - incorrect value in one or more of the parameters
                # TODO to test and finish
                # TODO r.raise_for_status()
                pass
            elif r.status_code == requests.codes.not_found:
                # TODO No object(s) found
                pass

    return ripe_list


def get_lists(color=True, run_output=True, ibl=True, ripe=True, keywords_list=[], ibl_lists=[]):
    """
    Give a global list generated from the different sources specified in arguments.
    :param color: Colorized stdout. True by default.
    :param run_output: Show running output in stdout. True by default.
    :param ibl: Should use iBlockList as information source. True by default.
    :param ripe: Should use the RIPE as information source. True by default.
    :param keywords_list: The keywords list to search for gremlins.
    :param ibl_lists: The iBlockList list to parse.
    :return: The global list as [('BAD IPs', 'x.x.x.x/y'),...].
    """
    list = []
    if ibl:
        list.extend(get_ibl_list(color, run_output, keywords_list, ibl_lists))
        if run_output:
            sys.stdout.write("[get_list] List from iBlockList generated\n")
    if ripe:
        list.extend(get_ripe_list(color, run_output, keywords_list))
        if run_output:
            sys.stdout.write("[get_list] List from the RIPE generated\n")
    return list


def cmd_list(color=True, run_output=True, ibl=True, ripe=True, keywords_list=[], ibl_lists=[]):
    """
    Run the 'list' command. Print each line in CSV format "<NAME>,<CIDR_IP_RANGE>".
    :param color: Colorized stdout. True by default.
    :param run_output: Show running output in stdout. True by default.
    :param ibl: Should use iBlockList as information source. True by default.
    :param ripe: Should use the RIPE as information source. True by default.
    :param keywords_list: The keywords list to search for gremlins.
    :param ibl_lists: The iBlockList list to parse.
    """
    full_list = get_lists(color, run_output, ibl, ripe, keywords_list, ibl_lists)
    if run_output:
        sys.stdout.write("[cmd_list] Printing the list...\n\n")
    for (name, cidr_ip_range) in full_list:
        sys.stdout.write(name + "," + cidr_ip_range + "\n")


# TODO Iptable commands to be finished + list mode to manage
def cmd_iptables(color=True, run_output=True, ibl=True, ripe=True, keywords_list=[], ibl_lists=[]):
    """
    Run the 'iptables' command.
    :param color: Colorized stdout. True by default.
    :param run_output: Show running output in stdout. True by default.
    :param ibl: Should use iBlockList as information source. True by default.
    :param ripe: Should use the RIPE as information source. True by default.
    :param keywords_list: The keywords list to search for gremlins.
    :param ibl_lists: The iBlockList list to parse.
    """
    full_list = get_lists(color, run_output, ibl, ripe)
    # TODO generate iptables
    sys.stdout.write("[cmd_iptables] IPTABLES COMMAND TO BE DONE\n")


# TODO To be implemented
def cmd_fbxos(color=True, run_output=True, ibl=True, ripe=True, keywords_list=[], ibl_lists=[]):
    pass


def cmd_utm9(color=True, run_output=True, ibl=True, ripe=True, keywords_list=[], ibl_lists=[]):
    """
    Run the 'utm9' command.
    :param color: Colorized stdout. True by default.
    :param run_output: Show running output in stdout. True by default.
    :param ibl: Should use iBlockList as information source. True by default.
    :param ripe: Should use the RIPE as information source. True by default.
    :param keywords_list: The keywords list to search for gremlins.
    :param ibl_lists: The iBlockList list to parse.
    """
    pass


# TODO To be implemented
def cmd_pfsense(color=True, run_output=True, ibl=True, ripe=True, keywords_list=[], ibl_lists=[]):
    pass


# TODO To be implemented
def cmd_opnsense(color=True, run_output=True, ibl=True, ripe=True, keywords_list=[], ibl_lists=[]):
    pass


def init_args(dest='cmd', add_help=False):
    """
    Initialize and parse arguments. Arguments helps are set in settings.
    :param dest: variable name to store the choosen command. 'cmd' by default.
    :param add_help: choose if the parsers have to add help options and associated texts, False by default because they are manually handled.
    :return: the main parser.
    """
    parser = argparse.ArgumentParser(add_help=add_help)
    subparsers = parser.add_subparsers(dest=dest)

    # Core arguments
    parser.add_argument('-h', '--help',
                        dest='showHelp',
                        action='store_true',
                        default=False
                        )
    parser.add_argument('-v', '--version',
                        dest='showVersion',
                        action='store_true',
                        default=False
                        )

    # Options arguments
    parser.add_argument('-Dr', '--disable-ripe',
                        dest='queryRIPE',
                        action='store_false',
                        default=True
                        )
    parser.add_argument('-Di', '--disable-iblocklist',
                        dest='queryiBlockList',
                        action='store_false',
                        default=True
                        )
    parser.add_argument('-Dc', '--disable-coloring',
                        dest='colorOutput',
                        action='store_false',
                        default=True
                        )
    parser.add_argument('-c', '--clean-output',
                        dest='fullOutput',
                        action='store_false',
                        default=True
                        )

    # list command arguments
    parser_list = subparsers.add_parser(CMD_LIST, add_help=add_help)
    parser_list.add_argument('-h', '--help',
                             dest='showListHelp',
                             action='store_true',
                             default=False
                             )

    # iptables command arguments
    parser_iptables = subparsers.add_parser(CMD_IPTABLES, add_help=add_help)
    parser_iptables.add_argument('-h', '--help',
                                 dest='showIptablesHelp',
                                 action='store_true',
                                 default=False
                                 )
    parser_iptables.add_argument('-l', '--list',
                                 dest='showListOnly',
                                 action='store_true',
                                 default=False
                                 )
    parser_iptables.add_argument('-H', '--host',
                                 dest='host',
                                 action='store',
                                 default=None
                                 )
    parser_iptables.add_argument('-P', '--port',
                                 dest='port',
                                 action='store',
                                 default=DEFAULT_SSH_PORT
                                 )
    parser_iptables.add_argument('-u', '--user',
                                 dest='user',
                                 action='store',
                                 default=None
                                 )
    parser_iptables.add_argument('-p', '--password',
                                 dest='password',
                                 action='store',
                                 default=None
                                 )
    parser_iptables.add_argument('-Ds', '--do-not-save',
                                 dest='save',
                                 action='store_false',
                                 default=True
                                 )

    # FreeboxOS Download Blacklist command arguments
    parser_fbxos = subparsers.add_parser(CMD_FBXOS, add_help=add_help)
    parser_fbxos.add_argument('-h', '--help',
                              dest='showFbxOSHelp',
                              action='store_true',
                              default=False
                              )
    parser_fbxos.add_argument('-H', '--host',
                              dest='host',
                              action='store',
                              default=None
                              )
    parser_fbxos.add_argument('-P', '--port',
                              dest='port',
                              action='store',
                              default=DEFAULT_FBX_HTTP_PORT
                              )
    parser_fbxos.add_argument('-u', '--user',
                              dest='user',
                              action='store',
                              default=None
                              )
    parser_fbxos.add_argument('-p', '--password',
                              dest='password',
                              action='store',
                              default=None
                              )
    parser_fbxos.add_argument('-s', '--secure',
                              dest='secure',
                              action='store_true',
                              default=False
                              )

    # Sophos UTM9 command arguments
    parser_utm9 = subparsers.add_parser(CMD_UTM9, add_help=add_help)
    parser_utm9.add_argument('-h', '--help',
                             dest='showUTM9Help',
                             action='store_true',
                             default=False
                             )
    parser_utm9.add_argument('-H', '--host',
                             dest='user',
                             action='store',
                             default=None
                             )
    parser_utm9.add_argument('-P', '--port',
                             dest='port',
                             action='store',
                             default=DEFAULT_UTM9_HTTPS_PORT
                             )
    parser_utm9.add_argument('-t', '--token',
                             dest='token',
                             action='store',
                             default=None
                             )
    parser_utm9.add_argument('-u', '--user',
                             dest='user',
                             action='store',
                             default=None
                             )
    parser_utm9.add_argument('-p', '--password',
                             dest='password',
                             action='store',
                             default=None
                             )
    parser_utm9.add_argument('-Dl', '--do-not-log',
                             dest='log',
                             action='store_false',
                             default=True
                             )

    # pfSense command arguments
    parser_pfsense = subparsers.add_parser(CMD_PFSENSE, add_help=add_help)
    parser_pfsense.add_argument('-h', '--help',
                                dest='showpfSenseHelp',
                                action='store_true',
                                default=False
                                )
    parser_pfsense.add_argument('-H', '--host',
                                dest='user',
                                action='store',
                                default=None
                                )
    parser_pfsense.add_argument('-P', '--port',
                                dest='port',
                                action='store',
                                default=DEFAULT_PFSENSE_HTTPS_PORT
                                )
    parser_pfsense.add_argument('-u', '--user',
                                dest='user',
                                action='store',
                                default=None
                                )
    parser_pfsense.add_argument('-p', '--password',
                                dest='password',
                                action='store',
                                default=None
                                )
    parser_pfsense.add_argument('-Dl', '--do-not-log',
                                dest='log',
                                action='store_false',
                                default=True
                                )

    # OPNsense command arguments
    parser_opnsense = subparsers.add_parser(CMD_OPNSENSE, add_help=add_help)
    parser_opnsense.add_argument('-h', '--help',
                                 dest='showOPNsenseHelp',
                                 action='store_true',
                                 default=False
                                 )
    parser_opnsense.add_argument('-H', '--host',
                                 dest='user',
                                 action='store',
                                 default=None
                                 )
    parser_opnsense.add_argument('-P', '--port',
                                 dest='port',
                                 action='store',
                                 default=DEFAULT_OPNSENSE_HTTPS_PORT
                                 )
    parser_opnsense.add_argument('-u', '--user',
                                 dest='user',
                                 action='store',
                                 default=None
                                 )
    parser_opnsense.add_argument('-p', '--password',
                                 dest='password',
                                 action='store',
                                 default=None
                                 )
    parser_opnsense.add_argument('-Dl', '--do-not-log',
                                 dest='log',
                                 action='store_false',
                                 default=True
                                 )

    return parser


def main():
    try:
        # Parse the command arguments
        parser = init_args()
        args = parser.parse_args()

        # Make ANSI escapes work with MS Windows
        if args.colorOutput and OS_IS_WIN:
            colorama.init()

        # Output standard information
        if args.showVersion:
            sys.stdout.write(VERSION_STRING)
        else:
            if args.fullOutput:
                sys.stdout.write(BANNER % ((colorama.Style.BRIGHT + colorama.Fore.GREEN,
                                            colorama.Style.RESET_ALL,
                                            colorama.Style.BRIGHT + colorama.Fore.WHITE,
                                            colorama.Style.RESET_ALL
                                            ) if args.colorOutput else ('', '', '', '')))
            # Let's go running
            if args.showHelp:
                sys.stdout.write(HELP % (BASENAME_PROG, BASENAME_PROG))
            elif args.cmd == CMD_LIST:
                if args.showListHelp:
                    sys.stdout.write(HELP_LIST % (BASENAME_PROG, CMD_LIST))
                else:
                    cmd_list(args.colorOutput, args.fullOutput, args.queryiBlockList, args.queryRIPE, KEYWORDS_LIST,
                             IBL_LISTS)
            elif args.cmd == CMD_IPTABLES:
                if args.showIptablesHelp:
                    sys.stdout.write(HELP_IPTABLES % (BASENAME_PROG, CMD_IPTABLES))
                else:
                    cmd_iptables(args.colorOutput, args.fullOutput, args.queryiBlockList, args.queryRIPE, KEYWORDS_LIST,
                                 IBL_LISTS)
            elif args.cmd == CMD_FBXOS:
                if args.showFbxOSHelp:
                    sys.stdout.write(HELP_FBXOS % (BASENAME_PROG, CMD_FBXOS))
                else:
                    cmd_fbxos(args.colorOutput, args.fullOutput, args.queryiBlockList, args.queryRIPE, KEYWORDS_LIST,
                              IBL_LISTS)
            elif args.cmd == CMD_UTM9:
                if args.showUTM9Help:
                    sys.stdout.write(HELP_UTM9 % (BASENAME_PROG, CMD_UTM9))
                else:
                    cmd_utm9(args.colorOutput, args.fullOutput, args.queryiBlockList, args.queryRIPE, KEYWORDS_LIST,
                             IBL_LISTS)
            elif args.cmd == CMD_PFSENSE:
                if args.showpfSenseHelp:
                    sys.stdout.write(HELP_PFSENSE % (BASENAME_PROG, CMD_PFSENSE))
                else:
                    cmd_pfsense(args.colorOutput, args.fullOutput, args.queryiBlockList, args.queryRIPE, KEYWORDS_LIST,
                                IBL_LISTS)
            elif args.cmd == CMD_OPNSENSE:
                if args.showOPNsenseHelp:
                    sys.stdout.write(HELP_OPNSENSE % (BASENAME_PROG, CMD_OPNSENSE))
                else:
                    cmd_opnsense(args.colorOutput, args.fullOutput, args.queryiBlockList, args.queryRIPE, KEYWORDS_LIST,
                                 IBL_LISTS)
            else:
                sys.stdout.write(HELP % (BASENAME_PROG, BASENAME_PROG))
    except KeyboardInterrupt as ki:
        sys.stderr.write(str(ki))
        exit(error.ERROR_CODE_EXCEPTION)
    except requests.RequestException as re:
        sys.stderr.write(str(re))
        exit(error.ERROR_CODE_EXCEPTION)
    except Exception as e:
        # TODO exceptions to review
        sys.stderr.write(str(type(e)) + ": " + str(e))
        exit(error.ERROR_CODE_EXCEPTION)
    finally:
        # TODO Clear cache ?
        exit(error.ERROR_CODE_NORMAL)


if __name__ == "__main__":
    main()
