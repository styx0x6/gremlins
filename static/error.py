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


ERROR_CODE_NORMAL = 0
ERROR_CODE_VERSION = 1
ERROR_CODE_EXCEPTION = 2

# %s: detected version, minimal required version, program name
ERR_CRITICAL_VERSION = "[CRITICAL] Python %s detected. Please use at least Python %s for running %s\n" \
                       "  => For further information, visit 'http://www.python.org/download/'"

# GremlinsDB exceptions messages
ERR_DB_INSTANCE_ALREADY_INIT = "GremlinsList instance is already initiated. \
Use the get_instance static method to get the initiated instance"
ERR_DB_INVALID_CIDR_IPV4_NET = "Invalid CIDR IPv4 network format"
ERR_DB_INVALID_CIDR_IPV6_NET = "Invalid CIDR IPv6 network format"
ERR_DB_KEY_ALREADY_EXISTS = "Primary key already exists"
ERR_DB_KEY_NOT_FOUND = "Primary key not found"
