import unittest
from omush.network.clientmanager import OMushConnectedClientManager

class MockProtocolClient(object):
    pass

class MockConnectedClient(object):
    def __init__(self, protocol_client, connected_client_manager):
        self.protocol_client = protocol_client;
        self.connected_client_manager = connected_client_manager;

class MockConnectedClientFactory(object):
    def provision(self, protocol_client, connected_client_manager):
        return MockConnectedClient(protocol_client=protocol_client,
                                   connected_client_manager=connected_client_manager)

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
        client = manager.provision_client(protocol_client = protocol)
        self.assertTrue(client in manager.clients)
        self.assertEquals(client.protocol_client, protocol)
        self.assertEquals(client.connected_client_manager, manager)

    def test_release_method(self):
        import gc
        manager = OMushConnectedClientManager()
        manager.factory = MockConnectedClientFactory()

        protocol = MockProtocolClient()
        client = manager.provision_client(protocol_client = protocol)
        manager.release_client(connected_client=client)
        # There should only be two reference to the client now, the one held in
        # local scope in the client variable of this method. All other
        # references should be killed.
        self.assertEquals(len(gc.get_referrers(client)), 1)



if __name__ == '__main__':
    unittest.main()
