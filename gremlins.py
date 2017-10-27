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
import inspect
import argparse
import gzip
import unicodedata
import ipaddress

# Import settings
from static.settings import PROJECT_NAME
from static.settings import VERSION_STRING
from static.settings import VALID_PYTHON_VERSION
from static.settings import CMD_HELP
from static.settings import CMD_LIST
from static.settings import CMD_IPTABLES
from static.settings import CMD_FBXOS
from static.settings import CMD_UTM9
from static.settings import CMD_PFSENSE
from static.settings import CMD_OPNSENSE
from static.settings import DEFAULT_SSH_PORT
from static.settings import DEFAULT_FBX_HTTP_PORT
from static.settings import DEFAULT_UTM9_HTTPS_PORT
from static.settings import DEFAULT_PFSENSE_HTTPS_PORT
from static.settings import DEFAULT_OPNSENSE_HTTPS_PORT
from static.settings import IBL_HTTP_URL
from static.settings import IBL_LIST_ENC
from static.settings import IBL_SEP
from static.settings import RIPE_HTTP_REST_URL
from static.settings import RIPE_JSON_NAME_LIST
from static.settings import RIPE_JSON_INETNUM
from static.settings import IBL_LISTS
from static.settings import KEYWORDS_LIST
from static.settings import STDOUT
from static.settings import STDERR
from static.settings import OK
from static.settings import NOK
from static.settings import STR_OK
from static.settings import STR_NOK
from static.settings import STR_ERR
from static.settings import STR_DEBUG
from static.settings import DEFAULT_COLORIZE_OUTPUT
from static.settings import DEFAULT_SHOW_RUNNING_OUTPUT
from static.settings import DEFAULT_SHOW_DEBUG_INFO
from static.settings import DEFAULT_SHOW_RUNNING_ERROR
from static.settings import BANNER
from static.settings import HELP
from static.settings import HELP_LIST
from static.settings import HELP_IPTABLES
from static.settings import HELP_FBXOS
from static.settings import HELP_UTM9
from static.settings import HELP_PFSENSE
from static.settings import HELP_OPNSENSE

# Import error codes and messages
from static.error import ERROR_CODE_NORMAL
from static.error import ERROR_CODE_VERSION
from static.error import ERROR_CODE_EXCEPTION
from static.error import ERR_CRITICAL_VERSION

from lib.thirdparty import colorama
from lib.thirdparty import requests

PYTHON_VERSION = sys.version.split()[0]

# Python version check
if PYTHON_VERSION < VALID_PYTHON_VERSION:
    sys.stderr.write(ERR_CRITICAL_VERSION % (PYTHON_VERSION, VALID_PYTHON_VERSION, PROJECT_NAME) + "\n")
    exit(ERROR_CODE_VERSION)

# Running definition
OS_IS_WIN = True if os.name is 'nt' else False
OS_IS_POSIX = True if os.name is 'posix' else False
BASENAME_PATH = os.path.basename(sys.argv[0])
BASENAME_PROG = ("python " if OS_IS_WIN else "") + ("\"%s\"" % BASENAME_PATH if " " in BASENAME_PATH else BASENAME_PATH)

# Running global variables set with their default values
gvar_colorize_output = DEFAULT_COLORIZE_OUTPUT
gvar_show_running_output = DEFAULT_SHOW_RUNNING_OUTPUT
gvar_show_debug_info = DEFAULT_SHOW_DEBUG_INFO
gvar_show_running_error = DEFAULT_SHOW_RUNNING_ERROR


def write_(message: str, std: int = STDOUT, debug_info: str = "", is_raw_data: bool = False):
    """
    Write message into stdout or stderr in a standardized way according to gvar_show_running_output,
    gvar_show_debug_info and gvar_show_running_error variables. The end of line "\n" char is not automatically handled.
    :param message: The string to write.
    :param std: STDOUT to write in stdout, STDERR to write in stderr.
    :param debug_info: Debugging information that will be shown as prefix. This information is always shown within an
    error messsage. Usually the function name that writen the message for standard outputs.
    :param is_raw_data: Is 'message' considered as raw data. Raw data is only written in STDOUT even if
    gvar_show_running_output variable is set to False or std is set to another output.
    """
    debug_prefix = (STR_DEBUG % debug_info) if ((gvar_show_debug_info or std is STDERR) and debug_info is not "") \
        else ""
    err_prefix = ((colorama.Fore.RED + STR_ERR + colorama.Style.RESET_ALL) if gvar_colorize_output else STR_ERR) \
        + debug_prefix

    if is_raw_data:
        sys.stdout.write(message)
    else:
        if std is STDOUT and gvar_show_running_output:
            sys.stdout.write(debug_prefix + message)
        elif std is STDERR and gvar_show_running_error:
            sys.stderr.write("\n" + err_prefix + message)
        else:
            pass


def write_debug(message: str, std: int = STDOUT, debug_info: str = ""):
    """
    Write message into stdout or stderr in a standardized way in debug mode. The end of line "\n" char is not
    automatically handled.
    :param message: The string to write only in debug mode.
    :param std: STDOUT to write in stdout, STDERR to write in stderr.
    :param debug_info: Debugging information that will be shown as prefix. This information is always shown within an
    error messsage. Usually the function name that writen the message for standard outputs.
    """
    if gvar_show_debug_info:
        write_(message, std, debug_info)


def write_result(result: bool, suffix: str = ""):
    """
    Write a simple OK or NOK result in STDOUT according to the global formatting variables. The end of line "\n" char
    is not automatically handled.
    :param result: OK to write STR_OK, NOK to write STR_NOK.
    :param suffix: Append a string to the result. Empty string by default.
    """
    ok = (colorama.Fore.GREEN + STR_OK + colorama.Style.RESET_ALL) if gvar_colorize_output else STR_OK
    nok = (colorama.Fore.RED + STR_NOK + colorama.Style.RESET_ALL) if gvar_colorize_output else STR_NOK

    if result is OK:
        write_(ok + suffix)
    elif result is NOK:
        write_(nok + suffix)
    else:
        pass


def iprange_to_cidr(ip_range: str = None) -> [str]:
    """
    Format an IP range addresses string given as "start to end" format ('x.x.x.x-y.y.y.y')
    to its corresponding CIDR list.
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


# TODO Return a 3-tuple
def get_ibl_list() -> [(str, str)]:
    """
    Get the formatted list from iBlockList. Formatted as [('bt_level1','BAD IPs', 'x.x.x.x/y'),...].
    :return: The formatted iBlockList list.
    """
    # https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
    _f_name = inspect.currentframe().f_code.co_name  # function name for debug purpose

    ibl_list = []

    for _list in IBL_LISTS:
        write_("Getting list '%s' from iBlockList... " % _list, STDOUT, _f_name)
        r = requests.get(IBL_HTTP_URL % _list)
        # Check HTTP response code
        if r.status_code == requests.codes.ok:
            write_result(OK, " - Downloaded file size: %sMB"
                         % round((int(r.headers.get('content-length')) / 1024 / 1024), 2) + "\n")

            working_list = []
            # Decompress, decode as UTF-8 string, and split based on the end of line
            if r.headers.get('content-type') == 'application/x-gzip':
                write_("Decompressing and decoding the file...      ", STDOUT, _f_name)
                working_list = gzip.decompress(r.content).decode(encoding=IBL_LIST_ENC).split("\n")
                write_result(OK, "\n")
            # case below should never occurs
            elif r.headers.get('content-type') == 'gzip':
                write_("Decoding file...                     ", STDOUT, _f_name)
                working_list = r.content.decode(encoding=IBL_LIST_ENC).split("\n")
                write_result(OK, "\n")
            # if unexpected format is downloaded
            else:
                write_("Unexpected file format downloaded (%s) when getting list '%s'\n"
                       % (r.headers.get('content-type'), _list), STDERR, _f_name)
                continue

            # Parse for concerned lines
            write_("Parsing '%s' from iBlockList...      " % _list, STDOUT, _f_name)
            # remove the two first header lines from the blocking list
            working_list = working_list[2:]
            for _line in working_list:
                # http://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison-in-python
                if any(word in unicodedata.normalize("NFKD", _line.casefold()) for word in KEYWORDS_LIST):
                    #  format entries
                    _name, _ipr = _line.split(IBL_SEP)
                    _cidr_ip_range_list = []
                    try:
                        _cidr_ip_range_list = iprange_to_cidr(_ipr)
                    except ipaddress.AddressValueError as ave:
                        write_("AddressValueError raised when trying to format IP range: %s\n" % str(ave), STDERR,
                               _f_name)
                    except ipaddress.NetmaskValueError as nve:
                        write_("NetmaskValueError raised when trying to format IP range: %s\n" % str(nve), STDERR,
                               _f_name)
                    except ValueError as ve:
                        write_("ValueError raised when trying to format IP range: %s\n" % str(ve), STDERR,
                               _f_name)
                    except TypeError as te:
                        write_("TypeError raised when trying to format IP range: %s\n" % str(te), STDERR,
                               _f_name)
                    for _cidr_ip_range in _cidr_ip_range_list:
                        #  clean duplicate entries
                        if (_name, _cidr_ip_range) not in ibl_list:
                            ibl_list.extend([(_name, _cidr_ip_range)])
            write_result(OK, "\n")
        else:
            # received another response code than 200 OK
            write_result(NOK, " - Received response code %s\n" % r.status_code)

    return ibl_list


# TODO Return a 3-tuple
def get_ripe_list() -> [(str, str)]:
    """
    Get the formatted list from the RIPE. Formatted as [('RIPE','BAD IPs', 'x.x.x.x/y'),...].
    :return: The formatted RIPE list.
    """
    # https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
    _f_name = inspect.currentframe().f_code.co_name  # function name for debug purpose

    ripe_list = []

    for _word in KEYWORDS_LIST:
        write_("Requesting RIPE for '%s'... " % _word, STDOUT, _f_name)
        r = requests.get(RIPE_HTTP_REST_URL % _word)
        # Check HTTP response code
        if r.status_code == requests.codes.ok:
            write_result(OK, "\n")

            working_list = []
            # Parse the JSON response
            if r.headers.get('content-type') == 'application/json':
                write_("Parsing the JSON response...    ", STDOUT, _f_name)
                try:
                    dict_json = r.json()
                    if dict_json is not None:
                        print(dict_json['objects'])
                except ValueError as ve:
                    write_("ValueError raised when trying to decode JSON: %s\n" % str(ve), STDERR, _f_name)
                write_result(OK, "\n")
            # case below should never occurs
            else:
                write_("Unexpected content-type response received (%s) when requesting RIPE for '%s'\n"
                       % (r.headers.get('content-type'), _word), STDERR, _f_name)
        elif r.status_code == 404:
            write_("Not Found\n")
        else:
            # received another response code than 200 OK or 404 Not Found
            write_result(NOK, " - Received response code %s\n" % r.status_code)

    return ripe_list


def get_full_list(ibl: bool = True, ripe: bool = True) -> [(str, str, str)]:
    """
    Give a global list generated from the different sources specified in arguments.
    Formatted as [('bt_level1','BAD IPs', 'x.x.x.x/y'),...].
    :param ibl: Should use iBlockList as information source. True by default.
    :param ripe: Should use the RIPE as information source. True by default.
    :return: The global list.
    """
    # https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
    _f_name = inspect.currentframe().f_code.co_name  # function name for debug purpose

    lists = []

    if ibl:
        lists.extend(get_ibl_list())
        write_("List from iBlockList generated.\n", STDOUT, _f_name)
    if ripe:
        lists.extend(get_ripe_list())
        write_("List from the RIPE generated.\n", STDOUT, _f_name)

    return lists


def cmd_list(ibl: bool = True, ripe: bool = True):
    """
    Run the 'list' command. Print each line in CSV format "<SOURCE>,<NAME>,<CIDR_IP_RANGE>".
    :param ibl: Should use iBlockList as information source. True by default.
    :param ripe: Should use the RIPE as information source. True by default.
    """
    # https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
    _f_name = inspect.currentframe().f_code.co_name  # function name for debug purpose

    full_list = get_full_list(ibl, ripe)

    write_("Printing the full list...\n\n", STDOUT, _f_name)
    # TODO To use with 3-tuple implementation
    """
    for (source, name, cidr_ip_range) in full_list:
        write_(source + "," + name + "," + cidr_ip_range + "\n", is_raw_data=True)
    """
    # TODO To delete after 3-tuple implementation
    for (name, cidr_ip_range) in full_list:
        write_(name + "," + cidr_ip_range + "\n", is_raw_data=True)


# TODO Iptable commands to be finished + Doc + Help
def cmd_iptables(ibl: bool = True, ripe: bool = True, show_list_only: bool = False, host: str = None,
                 port: int = DEFAULT_SSH_PORT, user: str = None, password: str = None, save: bool = True):
    """
    Run the 'iptables' command.
    :param ibl: Should use iBlockList as information source. True by default.
    :param ripe: Should use the RIPE as information source. True by default.
    :param show_list_only:
    :param host:
    :param port:
    :param user:
    :param password:
    :param save:
    """
    # https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
    _f_name = inspect.currentframe().f_code.co_name  # function name for debug purpose

    shell_commands_list = []
    full_list = get_full_list(ibl, ripe)

    # TODO generate iptables shell commands
    write_("IPTABLES COMMAND TO BE DONE\n", STDOUT, _f_name)


# TODO To be implemented
# TODO Args to review
def cmd_fbxos(ibl=True, ripe=True):
    # https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
    _f_name = inspect.currentframe().f_code.co_name  # function name for debug purpose
    pass


# TODO UTM9 to be finished + Doc + Help
def cmd_utm9(ibl=True, ripe=True, host=None, port=DEFAULT_UTM9_HTTPS_PORT, token=None, user=None, password=None,
             log=True):
    """
    Run the 'utm9' command.
    :param ibl: Should use iBlockList as information source. True by default.
    :param ripe: Should use the RIPE as information source. True by default.
    :param host:
    :param port:
    :param token:
    :param user:
    :param password:
    :param log:
    """
    # https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
    _f_name = inspect.currentframe().f_code.co_name  # function name for debug purpose
    pass


# TODO To be implemented
# TODO Args to review
def cmd_pfsense(ibl=True, ripe=True):
    # https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
    _f_name = inspect.currentframe().f_code.co_name  # function name for debug purpose
    pass


# TODO To be implemented
# TODO Args to review
def cmd_opnsense(ibl=True, ripe=True):
    # https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
    _f_name = inspect.currentframe().f_code.co_name  # function name for debug purpose
    pass


def init_args(dest: str = 'cmd', add_help: bool = False):
    """
    Initialize and parse arguments. Arguments helps are set in settings.
    :param dest: Variable name to store the choosen command. 'cmd' by default.
    :param add_help: Choose if the parsers have to add help options and associated texts, False by default because they are manually handled.
    :return: The arguments parser.
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
    parser.add_argument('-d', '--debug',
                        dest='debugMode',
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
                        dest='colorizeOutput',
                        action='store_false',
                        default=True
                        )
    parser.add_argument('-De', '--disable-error',
                        dest='showRunningError',
                        action='store_false',
                        default=True
                        )
    parser.add_argument('-c', '--clean-output',
                        dest='showRunningOutpout',
                        action='store_false',
                        default=True
                        )

    # help command arguments (not documented and so hidden)
    subparsers.add_parser(CMD_HELP, add_help=add_help)

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
                             dest='host',
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
                                dest='host',
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
                                 dest='host',
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
    # https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
    _f_name = inspect.currentframe().f_code.co_name  # function name for debug purpose

    # Load the global variables as writable by the main function
    global gvar_colorize_output, gvar_show_running_output, gvar_show_debug_info, gvar_show_running_error

    try:
        # Parse the command arguments
        parser = init_args()
        args = parser.parse_args()

        # Set the global variables according to the given arguments
        gvar_colorize_output = args.colorizeOutput
        gvar_show_running_output = args.showRunningOutpout
        gvar_show_debug_info = args.debugMode
        gvar_show_running_error = args.showRunningError

        write_debug("Started running: initialized arguments and set global variables\n", STDOUT, _f_name)

        # Make ANSI escapes work with MS Windows
        if gvar_colorize_output and OS_IS_WIN:
            colorama.init()
            write_debug("Initialized colorama for Windows OS\n", STDOUT, _f_name)

        # Output standard information
        if args.showVersion:
            write_(VERSION_STRING, STDOUT, _f_name)
        else:
            if args.showRunningOutpout:
                write_(BANNER % ((colorama.Style.BRIGHT + colorama.Fore.GREEN,
                                  colorama.Style.RESET_ALL,
                                  colorama.Style.BRIGHT + colorama.Fore.WHITE,
                                  colorama.Style.RESET_ALL
                                  ) if args.colorizeOutput else ('', '', '', '')))
            # Let's go running
            if args.showHelp:
                write_(HELP % (BASENAME_PROG, BASENAME_PROG))
            elif args.cmd == CMD_LIST:
                if args.showListHelp:
                    write_(HELP_LIST % (BASENAME_PROG, CMD_LIST))
                else:
                    write_debug("Started executing the cmd: %s\n" % CMD_LIST, STDOUT, _f_name)
                    cmd_list(args.queryiBlockList, args.queryRIPE)
            elif args.cmd == CMD_IPTABLES:
                if args.showIptablesHelp:
                    write_(HELP_IPTABLES % (BASENAME_PROG, CMD_IPTABLES))
                else:
                    write_debug("Started executing the cmd: %s\n" % CMD_IPTABLES, STDOUT, _f_name)
                    cmd_iptables(args.queryiBlockList, args.queryRIPE, args.showListOnly, args.host, args.port,
                                 args.user, args.password, args.save)
            elif args.cmd == CMD_FBXOS:
                if args.showFbxOSHelp:
                    write_(HELP_FBXOS % (BASENAME_PROG, CMD_FBXOS))
                else:
                    write_debug("Started executing the cmd: %s\n" % CMD_FBXOS, STDOUT, _f_name)
                    # TODO Args to review
                    cmd_fbxos(args.queryiBlockList, args.queryRIPE)
            elif args.cmd == CMD_UTM9:
                if args.showUTM9Help:
                    write_(HELP_UTM9 % (BASENAME_PROG, CMD_UTM9))
                else:
                    write_debug("Started executing the cmd: %s\n" % CMD_UTM9, STDOUT, _f_name)
                    cmd_utm9(args.queryiBlockList, args.queryRIPE, args.host, args.port, args.token, args.user,
                             args.password, args.log)
            elif args.cmd == CMD_PFSENSE:
                if args.showpfSenseHelp:
                    write_(HELP_PFSENSE % (BASENAME_PROG, CMD_PFSENSE))
                else:
                    write_debug("Started executing the cmd: %s\n" % CMD_PFSENSE, STDOUT, _f_name)
                    # TODO Args to review
                    cmd_pfsense(args.queryiBlockList, args.queryRIPE)
            elif args.cmd == CMD_OPNSENSE:
                if args.showOPNsenseHelp:
                    write_(HELP_OPNSENSE % (BASENAME_PROG, CMD_OPNSENSE))
                else:
                    write_debug("Started executing the cmd: %s\n" % CMD_OPNSENSE, STDOUT, _f_name)
                    # TODO Args to review
                    cmd_opnsense(args.queryiBlockList, args.queryRIPE)
            else:  # will also match CMD_HELP
                write_(HELP % (BASENAME_PROG, BASENAME_PROG))
    except KeyboardInterrupt as ki:
        write_("KeyboardInterrupt stopped the execution. Exiting the program...\n", STDERR, _f_name)
        exit(ERROR_CODE_EXCEPTION)
    except requests.RequestException as re:
        write_("Unhandled RequestException from the 'requests' library: %s. Exiting the program...\n"
               % str(re), STDERR, _f_name)
        exit(ERROR_CODE_EXCEPTION)
    except Exception as e:
        write_("Unhandled exception (Type: %s): %s. Exiting the program...\n" % (str(type(e)), str(e)), STDERR, _f_name)
        exit(ERROR_CODE_EXCEPTION)
    finally:
        # TODO Clear cache?
        exit(ERROR_CODE_NORMAL)


if __name__ == "__main__":
    main()
