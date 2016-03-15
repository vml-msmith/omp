from autobahn.asyncio.websocket import WebSocketServerProtocol

class OMushServerProtocol(WebSocketServerProtocol):
    def notify(self, msg):
        payload = msg.encode('utf8')
        self.sendMessage(payload, isBinary = False)

    def onOpen(self):
        """The connection to the client has been opened
        """
        self.clientManager = self.factory.getClientManager()
        self.client = self.clientManager.provisionClient(protocolClient=self)
