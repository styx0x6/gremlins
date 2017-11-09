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

import ipaddress

ERR_INVALID_CIDR_IPV4_NET = "Invalid CIDR IPv4 network format"
ERR_INVALID_CIDR_IPV6_NET = "Invalid CIDR IPv6 network format"
ERR_INVALID_NET_TYPE = "Invalid network type"


class GremlinsListError(Exception):
    def __init__(self, message):
        super(GremlinsListError, self).__init__(message)


class GremlinsListIPv4NetworkError(GremlinsListError):
    def __init__(self):
        super(GremlinsListIPv4NetworkError, self).__init__(ERR_INVALID_CIDR_IPV4_NET)


class GremlinsListIPv6NetworkError(GremlinsListError):
    def __init__(self):
        super(GremlinsListIPv6NetworkError, self).__init__(ERR_INVALID_CIDR_IPV6_NET)


class GremlinsListNetworkTypeError(GremlinsListError):
    def __init__(self):
        super(GremlinsListNetworkTypeError, self).__init__(ERR_INVALID_NET_TYPE)


class GremlinsList:
    """
    Defines an IPv4 dict and an IPv6 dict in which objects are reprensented as below.
    For IPv4:
        Type:       key: str -> (str, str, str)
        Usage:      '<IPV4_RANGE>': ('<SOURCE>', '<SEARCHED_KEYWORD>', '<NAME>')
        Example:    '1.2.3.192/27': ('RIPE', 'world company', 'WLD CPY LTD')
    For IPv6:
        Type:       key: str -> (str, str, str)
        Usage:      '<IPV6_RANGE>': ('<SOURCE>', '<SEARCHED_KEYWORD>', '<NAME>')
        Example:    '2001:db00::0/24': ('RIPE', 'world company', 'WLD CPY LTD')
    """

    def __init__(self):
        self._list_IPv4 = {}
        self._list_IPv6 = {}

    def __str__(self):
        return 'GremlinsList: list_ipv4 length: %i, list_ipv6 length: %i' % (len(self._list_IPv4), len(self._list_IPv6))

    @property
    def list_ipv4(self):
        return self._list_IPv4

    @property
    def list_ipv6(self):
        return self._list_IPv6

    def add_ipv4(self, key: str, value: (str, str, str)):
        try:
            # strict=False to force the most corresponding tight network (it could be a host aka /32).
            if isinstance(ipaddress.ip_network(key, strict=False), ipaddress.IPv4Network):
                self._list_IPv4[key] = value
        # case should never occurs
        except ValueError as ve:
            raise GremlinsListIPv4NetworkError()

    def add_ipv6(self, key: str, value: (str, str, str)):
        try:
            # strict=False to force the most corresponding tight network (it could be a host aka /128).
            if isinstance(ipaddress.ip_network(key, strict=False), ipaddress.IPv6Network):
                self._list_IPv6[key] = value
        # case should never occurs
        except ValueError as ve:
            raise GremlinsListIPv6NetworkError()