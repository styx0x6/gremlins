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

from static.error import ERR_LIST_INSTANCE_ALREADY_INIT
from static.error import ERR_LIST_INVALID_CIDR_IPV4_NET
from static.error import ERR_LIST_INVALID_CIDR_IPV6_NET
from static.error import ERR_LIST_KEY_ALREADY_EXISTS
from static.error import ERR_LIST_KEY_NOT_FOUND


class GremlinsListError(Exception):
    def __init__(self, message):
        super(GremlinsListError, self).__init__(message)


class GremlinsListInstanceInitError(GremlinsListError):
    def __init__(self):
        super(GremlinsListInstanceInitError, self).__init__(ERR_LIST_INSTANCE_ALREADY_INIT)


class GremlinsListIPv4NetworkError(GremlinsListError):
    def __init__(self):
        super(GremlinsListIPv4NetworkError, self).__init__(ERR_LIST_INVALID_CIDR_IPV4_NET)


class GremlinsListIPv6NetworkError(GremlinsListError):
    def __init__(self):
        super(GremlinsListIPv6NetworkError, self).__init__(ERR_LIST_INVALID_CIDR_IPV6_NET)


class GremlinsListKeyAlreadyExists(GremlinsListError):
    def __init__(self):
        super(GremlinsListKeyAlreadyExists, self).__init__(ERR_LIST_KEY_ALREADY_EXISTS)


class GremlinsListKeyNotFound(GremlinsListError):
    def __init__(self):
        super(GremlinsListKeyNotFound, self).__init__(ERR_LIST_KEY_NOT_FOUND)


class GremlinsList:
    """
    Defines an IPv4 dict and an IPv6 dict in which objects are reprensented as below.
    GremlinsList is a Singleton.
    For IPv4:
        Type:       key: str -> (str, str, str, str)
        Usage:      '<CIDR_IP_RANGE>': ('<VERSION>', '<SOURCE>', '<MATCHED_KEYWORD>', '<NAME>')
        Example:    '1.2.3.192/27': ('4', 'RIPE', 'world company', 'WLD CPY LTD')
    For IPv6:
        Type:       key: str -> (str, str, str, str)
        Usage:      '<CIDR_IP_RANGE>': ('<VERSION>', '<SOURCE>', '<MATCHED_KEYWORD>', '<NAME>')
        Example:    '2001:db00::0/24': ('6', 'RIPE', 'world company', 'WLD CPY LTD')
    """

    __instance = None

    @staticmethod
    def get_instance():
        if not isinstance(GremlinsList.__instance, GremlinsList):
            GremlinsList.__instance = GremlinsList()
        return GremlinsList.__instance

    def __init__(self):
        if isinstance(GremlinsList.__instance, GremlinsList):
            raise GremlinsListInstanceInitError()
        else:
            self._dict_IPv4 = {}
            self._dict_IPv6 = {}
            GremlinsList.__instance = self

    def __str__(self):
        return 'GremlinsList: dict_ipv4 length: %i, dict_ipv6 length: %i' % \
               (len(self._dict_IPv4), len(self._dict_IPv6))

    @property
    def get_ipv4(self) -> {str: (str, str, str, str)}:
        """
        :return: The IPv4 dictionnary.
        """
        return self._dict_IPv4

    @property
    def get_ipv6(self) -> {str: (str, str, str, str)}:
        """
        :return: The IPv6 dictionnary.
        """
        return self._dict_IPv6

    def reset(self):
        """
        Reset the IPv4 dict and the IPv6 dict.
        """
        self._dict_IPv4 = {}
        self._dict_IPv6 = {}

    def add_ipv4(self, key: str, value: (str, str, str, str)):
        """
        Add an IPv4 entry into the proper dictionnary if not already exists.
        Raise a GremlinsListIPv4NetworkError exception if key is not an IPv4 CIDR representation and
        a GremlinsListKeyAlreadyExists exception if the IPv4 entry already exists.
        :param key: '<CIDR_IP_RANGE>'.
        :param value: ('<VERSION>', <SOURCE>', '<MATCHED_KEYWORD>', '<NAME>').
        """
        try:
            # strict=False to force the most corresponding tight network (it could be a host aka /32).
            if isinstance(ipaddress.ip_network(key, strict=False), ipaddress.IPv4Network):
                if not self._dict_IPv4.get(key):
                    self._dict_IPv4[key] = value
                else:
                    raise GremlinsListKeyAlreadyExists()
        except GremlinsListKeyAlreadyExists as kae:
            raise kae
        # case should never occurs
        except ValueError as ve:
            raise GremlinsListIPv4NetworkError()

    def add_ipv6(self, key: str, value: (str, str, str, str)):
        """
        Add an IPv6 entry into the proper dictionnary if not already exists.
        Raise a GremlinsListIPv6NetworkError exception if key is not an IPv6 CIDR representation and
        a GremlinsListKeyAlreadyExists exception if the IPv6 entry already exists.
        :param key: '<CIDR_IP_RANGE>'.
        :param value: ('<VERSION>', '<SOURCE>', '<MATCHED_KEYWORD>', '<NAME>').
        """
        try:
            # strict=False to force the most corresponding tight network (it could be a host aka /128).
            if isinstance(ipaddress.ip_network(key, strict=False), ipaddress.IPv6Network):
                if not self._dict_IPv6.get(key):
                    self._dict_IPv6[key] = value
                else:
                    raise GremlinsListKeyAlreadyExists()
        except GremlinsListKeyAlreadyExists as kae:
            raise kae
        # case should never occurs
        except ValueError as ve:
            raise GremlinsListIPv6NetworkError()

    def update_ipv4(self, key: str, value: (str, str, str, str)):
        """
        Update IPv4 entry into the proper dictionnary if it exists.
        Raise a GremlinsListIPv4NetworkError exception if key is not an IPv4 CIDR representation and
        a GremlinsListKeyNotFound exception if the IPv4 entry already exists.
        :param key: '<CIDR_IP_RANGE>'.
        :param value: ('<VERSION>', '<SOURCE>', '<MATCHED_KEYWORD>', '<NAME>').
        """

        try:
            # strict=False to force the most corresponding tight network (it could be a host aka /32).
            if isinstance(ipaddress.ip_network(key, strict=False), ipaddress.IPv4Network):
                if self._dict_IPv4.get(key):
                    self._dict_IPv4[key] = value
                else:
                    raise GremlinsListKeyNotFound()
        except GremlinsListKeyNotFound as knf:
            raise knf
        # case should never occurs
        except ValueError as ve:
            raise GremlinsListIPv4NetworkError()

    def update_ipv6(self, key: str, value: (str, str, str, str)):
        """
        Update IPv6 entry into the proper dictionnary if it exists.
        Raise a GremlinsListIPv6NetworkError exception if key is not an IPv6 CIDR representation and
        a GremlinsListKeyNotFound exception if the IPv6 entry already exists.
        :param key: '<CIDR_IP_RANGE>'.
        :param value: ('<VERSION>', '<SOURCE>', '<MATCHED_KEYWORD>', '<NAME>').
        """
        try:
            # strict=False to force the most corresponding tight network (it could be a host aka /128).
            if isinstance(ipaddress.ip_network(key, strict=False), ipaddress.IPv6Network):
                if self._dict_IPv6.get(key):
                    self._dict_IPv6[key] = value
                else:
                    raise GremlinsListKeyNotFound()
        except GremlinsListKeyNotFound as knf:
            raise knf
        # case should never occurs
        except ValueError as ve:
            raise GremlinsListIPv6NetworkError()
