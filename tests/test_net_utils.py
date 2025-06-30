import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from scanner import net_utils

class TestNetUtils(unittest.TestCase):

    def test_detect_local_cidr_structure(self):
        """
        Ensure detect_local_cidr returns a dictionary with expected keys.
        """
        info = net_utils.detect_local_cidr()
        self.assertIsInstance(info, dict)
        self.assertIn("interface", info)
        self.assertIn("ip", info)
        self.assertIn("netmask", info)
        self.assertIn("cidr", info)

    def test_get_cidr_range_output(self):
        """
        Test that get_cidr_range returns correct CIDR notation.
        """
        ip = '192.168.0.2'
        netmask = '255.255.255.0'
        cidr = net_utils.get_cidr_range(ip, netmask)
        self.assertEqual(cidr, "192.168.0.0/24")

if __name__ == "__main__":
    unittest.main()