import unittest

class GenericTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_protocol(self):
        """Test that OMushServerProtocol exists"""
        from omush.network.serverprotocol import OMushServerProtocol
        protocol = OMushServerProtocol()

if __name__ == '__main__':
    unittest.main()
