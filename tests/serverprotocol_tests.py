import unittest
from omush.network.serverprotocol import OMushServerProtocol
from autobahn.asyncio.websocket import WebSocketServerFactory

class MockProtocol(OMushServerProtocol):
    def __init__(self):
        self.factory = None

    def sendMessage(self, payload, isBinary = False):
        self.mock_output = payload;

class MockClient(object):
    def __init__(self):
        pass

    def handleMessage(self, msg):
        self.message = msg


class MockClientManager(object):
    def provisionClient(self, protocolClient=None):
        # save the client somewhere.. in a list.
        self.client = MockClient()
        return self.client

    def releaseClient(self, connectedClient):
        self.client = None

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
        self.assertEquals(self.protocol.client, self.protocol.clientManager.client)

    def test_protocol_has_on_close_method(self):
        import gc

        self.protocol.onOpen()
        client = self.protocol.client
        self.protocol.onClose(wasClean = True,
                              code = 1000,
                              reason = "Because")
        self.assertTrue(self.protocol.client is None)

        # There should only be two reference to the client now, the one held in
        # local scope in the client variable of this method. All other
        # references should be killed.
        self.assertEquals(len(gc.get_referrers(client)), 1)

    def test_protocol_has_on_message_method(self):
        self.protocol.onOpen()
        # Not binary messages should be passed along to the connectedClient
        # after being decoded.
        message = "test".encode('utf8')
        self.protocol.onMessage(payload=message, isBinary=False)
        self.assertEquals(self.protocol.client.message, message.decode('utf8'))

        # Binary messages should not be passed to the connectedClient.
        message = "Another".encode('utf8')
        self.protocol.onMessage(payload=message, isBinary=True)
        self.assertNotEquals(self.protocol.client.message, message.decode('utf8'))

if __name__ == '__main__':
    unittest.main()
