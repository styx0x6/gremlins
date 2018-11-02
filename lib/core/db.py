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
import sqlite3

from enum import IntEnum

# Import constants
from static.const import STR_UNDEFINED
from static.const import IPV4_VER
from static.const import IPV6_VER

# Import error messages
from static.error import ERR_DB_INSTANCE_ALREADY_INIT
from static.error import ERR_DB_INVALID_CIDR_IPV4_NET
from static.error import ERR_DB_INVALID_CIDR_IPV6_NET
from static.error import ERR_DB_KEY_ALREADY_EXISTS
from static.error import ERR_DB_KEY_NOT_FOUND


class GremlinsDBError(Exception):
    def __init__(self, message):
        super(GremlinsDBError, self).__init__(message)


class GremlinsDBInstanceInitError(GremlinsDBError):
    def __init__(self):
        super(GremlinsDBInstanceInitError, self).__init__(ERR_DB_INSTANCE_ALREADY_INIT)


class GremlinsDBIPv4NetworkError(GremlinsDBError):
    def __init__(self):
        super(GremlinsDBIPv4NetworkError, self).__init__(ERR_DB_INVALID_CIDR_IPV4_NET)


class GremlinsDBIPv6NetworkError(GremlinsDBError):
    def __init__(self):
        super(GremlinsDBIPv6NetworkError, self).__init__(ERR_DB_INVALID_CIDR_IPV6_NET)


class GremlinsDBKeyAlreadyExists(GremlinsDBError):
    def __init__(self):
        super(GremlinsDBKeyAlreadyExists, self).__init__(ERR_DB_KEY_ALREADY_EXISTS)


class GremlinsDBKeyNotFound(GremlinsDBError):
    def __init__(self):
        super(GremlinsDBKeyNotFound, self).__init__(ERR_DB_KEY_NOT_FOUND)


class GDBConst(IntEnum):
    LIST = 666
    CIR = 0
    VERSION = 1
    SOURCE = 2
    MATCHED_KEYWORD = 3
    NAME = 4


class GremlinsDB:
    """
    Defines a database that contains the list of IPv4 & IPv6 entries.
    GremlinsDB is a Singleton.
    Database schema is defined as below, with CIDR_IP_RANGE (0) as primary key:
        TABLE:      LIST (666)
            COLUMNS:    CIDR_IP_RANGE (0)   VERSION (1)   SOURCE (2)   MATCHED_KEYWORD (3)   NAME (4)
            TYPE:       str                 str           str          str                   str
            EXAMPLE:    '1.2.3.192/27'      4             'RIPE'       'world company'       'WLD CPY LTD'
                        '2001:db00::0/64'   6             'RIPE'       'world company'       'WLD CPY LTD'
    """

    __PRE_TAB = 'TABLE_'
    __PRE_COL = 'COL_'

    __T_LIST = __PRE_TAB + str(GDBConst.LIST.value)
    __C_CIR = __PRE_COL + str(GDBConst.CIR.value)
    __C_VERSION = __PRE_COL + str(GDBConst.VERSION.value)
    __C_SOURCE = __PRE_COL + str(GDBConst.SOURCE.value)
    __C_MATCHED_KEYWORD = __PRE_COL + str(GDBConst.MATCHED_KEYWORD.value)
    __C_NAME = __PRE_COL + str(GDBConst.NAME.value)

    __instance = None

    @staticmethod
    def get_instance():
        if not isinstance(GremlinsDB.__instance, GremlinsDB):
            GremlinsDB()
        return GremlinsDB.__instance

    def __init__(self):
        if isinstance(GremlinsDB.__instance, GremlinsDB):
            raise GremlinsDBInstanceInitError()
        else:
            self.__db = sqlite3.connect(':memory:')
            self.__db.execute('''CREATE TABLE %s
                                (%s TEXT   PRIMARY KEY NOT NULL,
                                 %s INT    NOT NULL,
                                 %s TEXT   NOT NULL,
                                 %s TEXT   NOT NULL,
                                 %s TEXT   NOT NULL);'''
                              % (self.__T_LIST, self.__C_CIR, self.__C_VERSION, self.__C_SOURCE,
                                 self.__C_MATCHED_KEYWORD, self.__C_NAME))
            GremlinsDB.__instance = self

    def __len__(self):
        return self.__db.execute('SELECT Count(*) FROM %s' % self.__T_LIST)

    def __str__(self):
        return 'GremlinsDB entries number: %i' % len(self)

    def __repr__(self):
        return str(self)

    def reset(self):
        """
        Reset the table in database.
        """
        self.__db.execute('DELETE * FROM %s' % self.__T_LIST)

    def get_all_ipv4(self) -> {str: [str, str, str, str, str]}:
        """
        Get all IPv4 entries as a dictionary in the following format:
            {<CIDR_IP_RANGE>: [<CIDR_IP_RANGE>, <VERSION>, <SOURCE>, <MATCHED_KEYWORD>, <NAME>]}
        :return: A dictionary with all IPv4 entries.
        """
        dic = dict()
        cursor = self.__db.execute('SELECT * FROM %s WHERE %s=? ORDER BY %s' % (self.__T_LIST, self.__C_VERSION,
                                                                                self.__C_CIR),
                                   (IPV4_VER,))
        for row in cursor:
            dic.update({row[int(GDBConst.CIR)]: row})
        return dic

    def get_all_ipv6(self) -> {str: [str, str, str, str, str]}:
        """
        Get all IPv6 entries as a dictionary in the following format:
            {<CIDR_IP_RANGE>: [<CIDR_IP_RANGE>, <VERSION>, <SOURCE>, <MATCHED_KEYWORD>, <NAME>]}
        :return: A dictionary with all IPv6 entries.
        """
        dic = dict()
        cursor = self.__db.execute('SELECT * FROM %s WHERE %s=? ORDER BY %s' % (self.__T_LIST, self.__C_VERSION,
                                                                                self.__C_CIR),
                                   (IPV6_VER,))
        for row in cursor:
            dic.update({row[int(GDBConst.CIR)]: row})
        return dic

    def add_ipv4(self, cir: str, source: str = STR_UNDEFINED, matched_keyword: str = STR_UNDEFINED,
                 name: str = STR_UNDEFINED):
        """
        Add an IPv4 entry into the database if not already exists.
        :param cir: '<CIDR_IP_RANGE>'.
        :param source: '<SOURCE>'.
        :param matched_keyword: '<MATCHED_KEYWORD>'.
        :param name: '<NAME>'.
        :raise GremlinsDBIPv4NetworkError exception if key is not an IPv4 CIDR representation.
        :raise GremlinsDBKeyAlreadyExists exception if the IPv4 entry already exists.
        """
        try:
            # strict=False to force the most corresponding tight network (it could be a host aka /32).
            if isinstance(ipaddress.ip_network(cir, strict=False), ipaddress.IPv4Network):
                cursor = self.__db.cursor()
                cursor.execute('SELECT * FROM %s WHERE %s=?' % (self.__T_LIST, self.__C_CIR), (cir,))
                if cursor.fetchone() is None:
                    cursor.execute('INSERT INTO %s VALUES (?, ?, ?, ?, ?)'
                                   % self.__T_LIST, (cir, IPV4_VER, source, matched_keyword, name))
                    self.__db.commit()
                    cursor.close()
                else:
                    cursor.close()
                    raise GremlinsDBKeyAlreadyExists()
        except GremlinsDBKeyAlreadyExists as kae:
            raise kae
        # case should never occurs
        except ValueError:
            raise GremlinsDBIPv4NetworkError()

    def add_ipv6(self, cir: str, source: str = STR_UNDEFINED, matched_keyword: str = STR_UNDEFINED,
                 name: str = STR_UNDEFINED):
        """
        Add an IPv6 entry into the database if not already exists.
        :param cir: '<CIDR_IP_RANGE>'.
        :param source: '<SOURCE>'.
        :param matched_keyword: '<MATCHED_KEYWORD>'.
        :param name: '<NAME>'.
        :raise GremlinsDBIPv6NetworkError exception if key is not an IPv6 CIDR representation.
        :raise GremlinsDBKeyAlreadyExists exception if the IPv6 entry already exists.
        """
        try:
            # strict=False to force the most corresponding tight network (it could be a host aka /128).
            if isinstance(ipaddress.ip_network(cir, strict=False), ipaddress.IPv6Network):
                cursor = self.__db.cursor()
                cursor.execute('SELECT * FROM %s WHERE %s=?' % (self.__T_LIST, self.__C_CIR), (cir,))
                if cursor.fetchone() is None:
                    cursor.execute('INSERT INTO %s VALUES (?, ?, ?, ?, ?)'
                                   % self.__T_LIST, (cir, IPV6_VER, source, matched_keyword, name))
                    self.__db.commit()
                    cursor.close()
                else:
                    cursor.close()
                    raise GremlinsDBKeyAlreadyExists()
        except GremlinsDBKeyAlreadyExists as kae:
            raise kae
        # case should never occurs
        except ValueError:
            raise GremlinsDBIPv6NetworkError()

    def update_ipv4(self, cir: str, source: str = STR_UNDEFINED, matched_keyword: str = STR_UNDEFINED,
                    name: str = STR_UNDEFINED):
        """
        Update an IPv4 entry into the database if it exists.
        :param cir: '<CIDR_IP_RANGE>'.
        :param source: '<SOURCE>'.
        :param matched_keyword: '<MATCHED_KEYWORD>'.
        :param name: '<NAME>'.
        :raise GremlinsDBIPv4NetworkError exception if key is not an IPv4 CIDR representation.
        :raise GremlinsDBKeyNotFound exception if the IPv4 entry doesn't exist.
        """
        try:
            # strict=False to force the most corresponding tight network (it could be a host aka /32).
            if isinstance(ipaddress.ip_network(cir, strict=False), ipaddress.IPv4Network):
                cursor = self.__db.cursor()
                cursor.execute('SELECT * FROM %s WHERE %s=?' % (self.__T_LIST, self.__C_CIR), (cir,))
                if cursor.fetchone() is not None:
                    cursor.execute('UPDATE %s SET %s=?, %s=?, %s=?, %s=?) WHERE %s=?'
                                   % (self.__T_LIST, self.__C_VERSION, self.__C_SOURCE, self.__C_MATCHED_KEYWORD,
                                      self.__C_NAME, self.__C_CIR),
                                   (IPV4_VER, source, matched_keyword, name, cir))
                    self.__db.commit()
                    cursor.close()
                else:
                    cursor.close()
                    raise GremlinsDBKeyNotFound()
        except GremlinsDBKeyNotFound as knf:
            raise knf
        # case should never occurs
        except ValueError:
            raise GremlinsDBIPv4NetworkError()

    def update_ipv6(self, cir: str, source: str = STR_UNDEFINED, matched_keyword: str = STR_UNDEFINED,
                    name: str = STR_UNDEFINED):
        """
        Update an IPv6 entry into the database if it exists.
        :param cir: '<CIDR_IP_RANGE>'.
        :param source: '<SOURCE>'.
        :param matched_keyword: '<MATCHED_KEYWORD>'.
        :param name: '<NAME>'.
        :raise GremlinsDBIPv6NetworkError exception if key is not an IPv6 CIDR representation.
        :raise GremlinsDBKeyNotFound exception if the IPv6 entry doesn't exist.
        """
        try:
            # strict=False to force the most corresponding tight network (it could be a host aka /128).
            if isinstance(ipaddress.ip_network(cir, strict=False), ipaddress.IPv6Network):
                cursor = self.__db.cursor()
                cursor.execute('SELECT * FROM %s WHERE %s=?' % (self.__T_LIST, self.__C_CIR), (cir,))
                if cursor.fetchone() is not None:
                    cursor.execute('UPDATE %s SET %s=?, %s=?, %s=?, %s=?) WHERE %s=?'
                                   % (self.__T_LIST, self.__C_VERSION, self.__C_SOURCE, self.__C_MATCHED_KEYWORD,
                                      self.__C_NAME, self.__C_CIR),
                                   (IPV6_VER, source, matched_keyword, name, cir))
                    self.__db.commit()
                    cursor.close()
                else:
                    cursor.close()
                    raise GremlinsDBKeyNotFound()
        except GremlinsDBKeyNotFound as knf:
            raise knf
        # case should never occurs
        except ValueError:
            raise GremlinsDBIPv6NetworkError()

    def delete(self, cir: str):
        """
        Delete an entry in the database if it exists.
        :param cir: '<CIDR_IP_RANGE>'.
        :raise GremlinsDBKeyNotFound exception if the entry doesn't exist.
        """
        try:
            cursor = self.__db.cursor()
            cursor.execute('SELECT * FROM %s WHERE %s=?' % (self.__T_LIST, self.__C_CIR), (cir,))
            if cursor.fetchone() is not None:
                cursor.execute('DELETE FROM %s WHERE %s=?'
                               % (self.__T_LIST, self.__C_CIR), (cir,))
                self.__db.commit()
                cursor.close()
            else:
                cursor.close()
                raise GremlinsDBKeyNotFound()
        except GremlinsDBKeyNotFound as knf:
            raise knf
