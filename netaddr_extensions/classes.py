from netaddr import IPRange, IPAddress
from netaddr_extensions.funcs import get_address_range


class IrregularRange(IPRange):
    def __init__(self, cidr):
        """
        Takes an irregular cidr and calculates
        first and last IPAddresses for IPRange
        """
        a_range = get_address_range(cidr)
        self.first_addr = a_range[0]
        self.last_addr = a_range[1]
        self.cidr = cidr
        super(IrregularRange, self).__init__(IPAddress(self.first_addr), IPAddress(self.last_addr))

    def __str__(self):
        return self.cidr

    def iter_hosts(self):
        for address in self:
            yield address
