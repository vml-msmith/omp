import unittest
from omush.network.clientmanager import OMushConnectedClientManager
#from autobahn.asyncio.websocket import WebSocketServerFactory

class MockProtocolClient(object):
    pass

class MockConnectedClient(object):
    def __init__(self, protocolClient, connectedClientManager):
        self.protocolClient = protocolClient;
        self.connectedClientManager = connectedClientManager;

class MockConnectedClientFactory(object):
    def provision(self, protocolClient, connectedClientManager):
        return MockConnectedClient(protocolClient=protocolClient,
                                   connectedClientManager=connectedClientManager)

class SeverProtocolTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_provison_method(self):
        manager = OMushConnectedClientManager()
        manager.factory = MockConnectedClientFactory()

        self.assertFalse(manager.clients)
        protocol = MockProtocolClient()
        client = manager.provisionClient(protocolClient = protocol)
        self.assertTrue(client in manager.clients)
        self.assertEquals(client.protocolClient, protocol)
        self.assertEquals(client.connectedClientManager, manager)

    def test_release_method(self):
        import gc
        manager = OMushConnectedClientManager()
        manager.factory = MockConnectedClientFactory()

        protocol = MockProtocolClient()
        client = manager.provisionClient(protocolClient = protocol)
        manager.releaseClient(connectedClient=client)
        # There should only be two reference to the client now, the one held in
        # local scope in the client variable of this method. All other
        # references should be killed.
        self.assertEquals(len(gc.get_referrers(client)), 1)



if __name__ == '__main__':
    unittest.main()
