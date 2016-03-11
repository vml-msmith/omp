from autobahn.asyncio.websocket import WebSocketServerProtocol

class OMushServerProtocol(WebSocketServerProtocol):
    def notify(self, msg):
        payload = msg.encode('utf8')
        self.sendMessage(payload, isBinary = False)
