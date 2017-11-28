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


def iprange_to_cidr(ip_range: str = None) -> [str]:
    """
    Format an IP range addresses string given as "start to end" format ('x.x.x.x-y.y.y.y')
    to its corresponding CIDR list.
    :param ip_range: IP range addresses string given as "start to end" format ('x.x.x.x-y.y.y.y').
    :return: IP range addresses string as its corresponding CIDR string list.
    :raises ipaddress.AddressValueError: Raised by the ipaddress library when address is incorrect.
    :raises ipaddress.NetmaskValueError: Raised by the ipaddress library when netmask is incorrect.
    :raises ValueError: Raised by the ipaddress library when values are incorrect.
    :raises TypeError: Raised by the ipaddress library when given objects types are incorrect.
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
