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
        super(OMushServerProtocol, self).onOpen()

    def onClose(self, wasClean, code, reason):
        """The connection to the client has been closed by the server or by the
        client. Drop all references to the client.
        """
        self.client = None
        self.clientManager.releaseClient(connectedClient=self.client)

    def onMessage(self, payload, isBinary):
        """Handle non binary messages from the websocket client.

        Handles non binary messages by simply decoding via utf8 and passing to
        self.client.

        Handles binary messages by silently dropping them.

        TODO(msmith): Log or otherwise handle the binary messages.
        """
        if not isBinary:
            self.client.handleMessage(payload.decode('utf8'))
