class OMushConnectedClientManager(object):
    def __init__(self, *args, **kwargs):
        super(object, self).__init__(*args, **kwargs)
        self.clients = []

    def provisionClient(self, protocolClient):
        client = self.factory.provision(protocolClient=protocolClient,
                                        connectedClientManager=self)
        self.clients.append(client)
        return client

    def releaseClient(self, connectedClient):
        self.clients.remove(connectedClient);
