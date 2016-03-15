import unittest
from omush.network.serverprotocol import OMushServerProtocol
from autobahn.asyncio.websocket import WebSocketServerFactory

class MockProtocol(OMushServerProtocol):
    def __init__(self):
        self.factory = None

    def sendMessage(self, payload, isBinary = False):
        self.mock_output = payload;

class MockClientManager(object):
    def provisionClient(self, protocolClient=None):
        return object();

class MockProtocolFactory(WebSocketServerFactory):
    def getClientManager(self):
        return MockClientManager()

class SeverProtocolTest(unittest.TestCase):
    def setUp(self):
        self.protocol = MockProtocol()
        self.protocol.mock_output = None
        self.protocol.factory = MockProtocolFactory()

    def tearDown(self):
        pass

    def test_protocol_has_notify_method(self):
        """Test that OMushServerProtocol has a notify method."""
        self.protocol.notify("Test")
        self.assertTrue(self.protocol.mock_output is not None)
        self.assertEquals(self.protocol.mock_output.decode('utf8'), "Test")

    def test_protocol_has_on_open_method(self):
        self.protocol.onOpen()
        self.assertTrue(self.protocol.client is not None)
        self.assertTrue(self.protocol.clientManager is not None)

if __name__ == '__main__':
    unittest.main()
