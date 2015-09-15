from netaddr import IPAddress
from socket import inet_ntoa
from struct import pack


def is_netmask(value):
    try:
        if IPAddress(value).is_netmask():
            return True
        return False
    except:
        return False


def is_prefix(value):
    try:
        prefix = int(value)
        if prefix > 0 and prefix <= 32:
            return True
        return False
    except:
        return False


def range_overlap(range1, range2):
    """
    Checks if two ranges overlap.
    :param: range1::IPRange
    :param: range2::IPRange
    """
    return range1.first <= range2.last and range2.first <= range1.last


def range_in_range(range1, range2):
    """
    Checks if range 1 is within range2
    """
    return range1.first >= range2.first and range1.last <= range2.last


def prefix_to_netmask(prefix):
    if prefix > 32 or prefix <= 0:
        return None
    return inet_ntoa(pack(">I", (0xffffffff << (32 - prefix)) & 0xffffffff))


def netmask_to_prefix(netmask):
    """
    Takes netmask and turns to prefix
    """
    ip = IPAddress(netmask)
    if ip.is_netmask():
        return ip.netmask_bits()
    error_message = 'Param (%s) is not a valid netmask' % netmask
    raise ValueError(error_message)


def netmask_to_hosts(mask):
    """
    Takes prefix and returns number of hosts.
    """
    if is_prefix(mask):
        prefix = int(mask)
    elif is_netmask(mask):
        prefix = netmask_to_prefix(mask)
    else:
        error_message = 'Param (%s) is not a valid prefix or netmask' % mask
        raise ValueError(error_message)
    host_bits = 32 - prefix
    return 2 ** host_bits


def validate_cidr(value):
    error_message = "Address must be in CIDR notation:'127.0.0.0/24'."
    try:
        split = value.split('/')
        prefix = int(split[1])
        address = split[0]
    except (IndexError, ValueError):
        raise ValueError(error_message)
    if prefix > 32 or prefix <= 0:
        raise ValueError("Prefix must be between /1 and /32")
    if len(split) > 2:
        raise ValueError(error_message)
    if is_netmask(address):
        raise ValueError(error_message)


def get_address_range(value):
    """
    Returns tuple of first and last addresses.
    :return: [gateway or network, broadcast]
    /24 or higher will use .1 as the gateway
    """
    validate_cidr(value)
    split = value.split('/')
    first = IPAddress(split[0])
    last = first + (netmask_to_hosts(split[1]) - 1)
    if split[0][-1] == '0':
        first += 1
    return [str(first), str(last)]
