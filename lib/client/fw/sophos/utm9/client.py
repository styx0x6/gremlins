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

from .settings import CHARSET, UTM_DEFAULT_IP, UTM_DEFAULT_PORT

from lib.thirdparty import requests


class UTM9RESTClient:
    def __init__(self, ip=UTM_DEFAULT_IP, port=UTM_DEFAULT_PORT):
        self.__ip = ip
        self.__port = port

    @property
    def ip(self):
        return self.__ip

    @property
    def port(self):
        return self.__port

    @ip.setter
    def ip(self, ip):
        self.__ip = ip

    @port.setter
    def port(self, port):
        self.__port = port
