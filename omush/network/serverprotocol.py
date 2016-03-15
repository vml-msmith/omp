from autobahn.asyncio.websocket import WebSocketServerProtocol

class OMushServerProtocol(WebSocketServerProtocol):
    """WebSocketServerProtocol for use on oMush server.

    A new instance of the protocol is created for each connected client. The
    protocol will contain a "factory" property by default that points to the
    server factory. That factory should contain any information needed to link
    each connection to the overall game.
    """

    def notify(self, msg):
        """Send a String message to the connected websocket.

        The message will be encoded to utf8 before being transmitted.
        """
        payload = msg.encode('utf8')
        self.sendMessage(payload, isBinary = False)

    def onOpen(self):
        """The connection to the websocket has been opened

        Register the connected socket with the game via the clientmanager and
        provision a client object for this connection.
        """
        self.clientManager = self.factory.getClientManager()
        self.client = self.clientManager.provisionClient(protocolClient=self)
