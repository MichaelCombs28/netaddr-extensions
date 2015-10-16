from netaddr import IPRange, IPAddress
from netaddr_extensions.funcs import get_address_range, prefix_to_netmask


class IrregularRange(IPRange):
    """Takes an irregular cidr and calculates range
    """
    def __init__(self, cidr):
        """Creates range object with Cidr

        cidr -- network_address/prefix eg. 123.0.0.0/24
        """
        a_range = get_address_range(cidr)
        self.first_addr = a_range[0]
        self.last_addr = a_range[1]
        self.network_size = int(IPAddress(self.last_addr) - IPAddress(self.first_addr))
        self.cidr = cidr
        self.netmask = prefix_to_netmask(cidr.split('/')[1])
        super(IrregularRange, self).__init__(self.first_addr, self.last_addr)

    def __str__(self):
        return self.cidr

    @property
    def network_ip(self):
        return self.cidr.split('/')[0]

    @property
    def broadcast(self):
        return self.last_addr

    def iter_hosts(self):
        """Generator for usable host addresses
        """
        if self.netmask >= IPAddress('255.255.255.254'):
            return

        words = IPAddress(self.first_addr).words[3]
        for x, address in enumerate(self):
            if x == 0:
                continue
            if (
                x == self.network_size and
                words == 0 and
                self.netmask <= IPAddress('255.255.255.0')
            ):
                break
            yield address
