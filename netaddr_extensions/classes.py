from netaddr import IPRange
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
        super(IrregularRange, self).__init__(self.first_addr, self.last_addr)

    def usable_hosts(self):
        for address in self:
            if address.words[3] in (0, 255):
                continue
            yield address
