import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
import netifaces
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

    @patch('netifaces.interfaces')
    @patch('netifaces.ifaddresses')
    def test_get_active_interface(self, mock_ifaddresses, mock_interfaces):
        """
        Test that get_active_interface correctly finds a usable interface.
        """
        # Simulate interfaces list
        mock_interfaces.return_value = ['lo0', 'en0']

        # Simulate ifaddresses for 'lo0' and 'en0'
        def fake_ifaddresses(interface):
            if interface == 'lo0':
                return {netifaces.AF_INET: [{'addr': '127.0.0.1'}]}
            elif interface == 'en0':
                return {netifaces.AF_INET: [{'addr': '192.168.0.2'}]}
            return {}
        
        mock_ifaddresses.side_effect = fake_ifaddresses

        result = net_utils.get_active_interface()
        self.assertEqual(result, 'en0')
    
    @patch('netifaces.ifaddresses')
    def test_get_interface_info(self, mock_ifaddresses):
        """
        Test get_interface_info returns expected IP and netmask.
        """
        mock_ifaddresses.return_value = {
            netifaces.AF_INET: [{
                    'addr': '192.168.0.2',
                    'netmask': '255.255.255.0'
            }]
        }

        ip, mask = net_utils.get_interface_info('en0')
        self.assertEqual(ip, '192.168.0.2')
        self.assertEqual(mask, '255.255.255.0')

    @patch('scanner.net_utils.netifaces.interfaces', return_value=[])
    def test_detect_local_cidr_raises_on_no_interface(self, mock_interface):
        """
        Test that detect_local_cidr raises RuntimeError if no active interface is found.
        """
        with self.assertRaises(RuntimeError) as context:
            net_utils.detect_local_cidr()

        self.assertIn("No active network interface", str(context.exception))

if __name__ == "__main__":
    unittest.main(verbosity=2)