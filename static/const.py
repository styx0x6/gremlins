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


# Constants
STDOUT = 0  # defines stdout within Gremlins
STDERR = 1  # defines stderr within Gremlins
OK = True
NOK = False

# Static strings definition
STR_OK = "OK!"
STR_NOK = "NOK"
STR_ERR = "[ERR]"
STR_DEBUG = "[%s] "  # debug information shall be provided here

STR_UNDEFINED = ''

STR_IPV4_VER = 4
STR_IPV6_VER = 6

DB_TABLE = 'LIST'
DB_COL_CIR = 'CIR'
DB_COL_VERSION = 'VERSION'
DB_COL_SOURCE = 'SOURCE'
DB_COL_MATCHED_KEYWORD = 'MATCHED_KEYWORD'
DB_COL_NAME = 'NAME'
