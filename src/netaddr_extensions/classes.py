from netaddr import IPRange, IPAddress
from netaddr_extensions.funcs import get_address_range, prefix_to_netmask


class IrregularRange(IPRange):
    """

    Takes an irregular cidr and calculates range
    Most python modules don't support irregular range calculation without
    needing to know the network and broadcast addresses.

    This class allows you to input network/prefix and allow you
    to correctly iterate through hosts in the range.

    """
    def __init__(self, cidr):
        """
        Creates range object with Cidr

        :param cidr: network_address/prefix eg. 123.0.0.0/24

        """
        a_range = get_address_range(cidr)
        self.first_addr = a_range[0]
        self.last_addr = a_range[1]
        self._network_size = int(IPAddress(self.last_addr) - IPAddress(self.first_addr))
        self.cidr = cidr
        self.netmask = prefix_to_netmask(cidr.split('/')[1])
        super(IrregularRange, self).__init__(self.first_addr, self.last_addr)

    def __str__(self):
        return self.cidr

    def __len__(self):
        return self._network_size

    @property
    def network_ip(self):
        """Network IP"""
        return self.cidr.split('/')[0]

    @property
    def broadcast(self):
        """Broadcast IP"""
        return self.last_addr

    def iter_hosts(self):
        """:return: Generator for usable host addresses"""
        if self.netmask >= IPAddress('255.255.255.254'):
            return

        words = IPAddress(self.first_addr).words[3]
        for x, address in enumerate(self):
            if x == 0:
                continue
            if (
                x == self._network_size and
                words == 0 and
                self.netmask <= IPAddress('255.255.255.0')
            ):
                break
            yield address
