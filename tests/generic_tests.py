import unittest
from omush.network.serverprotocol import OMushServerProtocol

class MockProtocol(OMushServerProtocol):
    def sendMessage(self, payload, isBinary = False):
        self.mock_output = payload;

class GenericTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_protocol_has_notify_method(self):
        """Test that OMushServerProtocol has a notify method."""
        protocol = MockProtocol()
        protocol.mock_output = None
        protocol.notify("Test")
        self.assertTrue(protocol.mock_output is not None)
        self.assertEquals(protocol.mock_output.decode('utf8'), "Test")

if __name__ == '__main__':
    unittest.main()
