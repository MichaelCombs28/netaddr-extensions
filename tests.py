import unittest

from netaddr import IPRange
from netaddr_extensions import funcs
from netaddr_extensions import classes


class FuncsTestCase(unittest.TestCase):
    def test_bool_funcs(self):
        self.assertTrue(funcs.is_netmask('255.255.255.0'))
        self.assertFalse(funcs.is_netmask('127.0.0.1'))

        self.assertTrue(funcs.is_prefix('24'))
        self.assertFalse(funcs.is_prefix('33'))

        range1 = IPRange('127.0.0.1', '127.0.0.100')
        range2 = IPRange('127.0.0.99', '127.0.0.200')

        range3 = IPRange('127.0.2.1', '127.0.2.100')
        range4 = IPRange('127.0.2.101', '127.0.2.200')

        range5 = IPRange('127.0.0.3', '127.0.0.99')

        self.assertTrue(funcs.range_overlap(range1, range2))
        self.assertFalse(funcs.range_overlap(range3, range4))

        self.assertTrue(funcs.range_in_range(range5, range1))
        self.assertFalse(funcs.range_in_range(range2, range1))

    def test_conversions(self):
        self.assertEqual(funcs.prefix_to_netmask(24), '255.255.255.0')
        self.assertRaises(ValueError, funcs.prefix_to_netmask(33))

        self.assertEqual(funcs.netmask_to_prefix('255.255.255.224'), 27)

        self.assertEqual(funcs.netmask_to_hosts(24), 256)
        self.assertEqual(funcs.netmask_to_hosts('255.255.255.224'), 32)

    def test_validate(self):
        self.assertIsNone(funcs.validate_cidr('127.0.0.1/27'))
        self.assertRaises(ValueError, funcs.validate_cidr, '255.255.255.0/24')
        self.assertRaises(ValueError, funcs.validate_cidr, 'random text')

    def test_range(self):
        self.assertRaises(ValueError, funcs.get_address_range, '127.0.0.1')
        self.assertEqual(funcs.get_address_range(
            '127.0.0.0/23'),
            ['127.0.0.1', '127.0.1.255']
        )

        self.assertEqual(funcs.get_address_range(
            '127.0.0.65/27'),
            ['127.0.0.65', '127.0.0.96'])


class IrregularClassTest(unittest.TestCase):
    def setUp(self):
        # Enter the gateway address and prefix / netmask
        self.irreg = classes.IrregularRange('202.69.250.65/27')

    def test_properties(self):
        irreg = self.irreg
        self.assertIn('202.69.250.67', irreg)
        self.assertEqual('202.69.250.65', irreg.first_addr)
        self.assertEqual('202.69.250.96', irreg.last_addr)


if __name__ == '__main__':
    unittest.main()
