class OMushConnectedClientManager(object):
    """Manager to keep track of connected clients."""

    def __init__(self):
        self.factory = None
        self.clients = []

    def provision_client(self, protocol_client):
        """Create a new client, store it and return the new object."""
        client = self.factory.provision(protocol_client=protocol_client,
                                        connected_client_manager=self)
        self.clients.append(client)
        return client

    def release_client(self, connected_client):
        """Drop the connecte_client from the managed list of clients."""
        self.clients.remove(connected_client)
