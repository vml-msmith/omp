from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory


class Command(object):
    def match(pattern, obj=None):
        return False

    def execute(client=None, obj=None, game=None):
        pass

class WhoCommand(Command):
    def match(pattern, obj=None):
        if (pattern == 'WHO'):
            return True
        return False

    def execute(client=None, obj=None, game=None):
        if client is None:
            return
        if game is None:
            # Log
            return
        output = ""
        count = 0

        for value in game.clientManager.clients:
            if value.hasPlayerObject():
                count += 1
                output += "name\n"
        output += "---\n"
        output += "Players: " + str(count) + "\n"

        client.notify(output)

class QuitCommand(Command):
    def match(pattern, obj=None):
        if pattern == 'QUIT':
            return True
        return False

    def execute(client=None, obj=None, game=None):
        if client is not None:
            client.quit()

class ShutdownCommand(Command):
    def match(pattern, obj=None):
        if pattern == '@SHUTDOWN':
            return True
        return False

    def execute(client=None, obj=None, game=None):
        for value in game.clientManager.clients:
            value.close()
        game.core_loop.stop()

class LoginCommand(Command):
    def match(pattern, obj=None):
        if pattern == 'connect':
            return True
        return False

    def execute(client=None, obj=None, game=None):
        pass

class CreatePlayerCommand(Command):
    def match(pattern, obj=None):
        if pattern == 'create':
            return True
        return False

    def matcherRegex():
        pass

    def execute(client=None, obj=None, game=None):
        pass


def get_socket_commands():
    return [WhoCommand, QuitCommand, ShutdownCommand]

def get_login_commands():
    return [LoginCommand, CreatePlayerCommand]

class Game(object):
    def __init__(self):
        self.clientManager = ConnectedClientManager()
        self.clientManager.game = self

class ConnectedClientManager(object):
    def __init__(self, *args, **kwargs):
        super(object, self).__init__(*args, **kwargs)
        self.clients = []
        self.game = None

    def provisionClient(self, protocolClient):
        client = ConnectedClient(protocolClient=protocolClient, connectedClientManager=self)
        self.clients.append(client)
        return client


class ConnectedClient(object):
    def __init__(self, protocolClient, connectedClientManager):
        super(object, self).__init__()
        self.protocolClient = protocolClient
        self.clientManager = connectedClientManager
        self.state = None

    def hasPlayerObject(self):
        return False

    def handleMessage(self, message):
        handled = False;
        handled = self.handleSocketCommands(message)
        if handled == False:
            if self.hasPlayerObject():
                handled = self.handlePlayerCommands(message)
            else:
                handled = self.handleLoginCommands(message)

        if handled == False:
            self.handleBadCommand(message)

    def handleSocketCommands(self, message):
        for value in get_socket_commands():
            if value.match(pattern=message) == True:
                value.execute(client=self, game=self.clientManager.game)
                return True
        return False

    def handlePlayerCommands(self, message):
        return False

    def handleLoginCommands(self, message):
        return False

    def handleBadCommand(self, message):
        self.notify("Huh? Unknown command.")

    def close(self):
        self.protocolClient.sendClose()

    def quit(self):
        self.close()

    def notify(self, message):
        if self.protocolClient != None:
            self.protocolClient.notify(msg = message);


class MyServerProtocol(WebSocketServerProtocol):
    """Demo ServerProtocol

    The reason behind this protocol is just to demo how the websocket server
    protocols work. It is not intended to be a final version.

    Key things:
      - self.factory contains the factory that created this object. Useful!
    """
    def notify(self, msg):
        payload = msg.encode('utf8')
        self.sendMessage(payload, isBinary = False)


    def onConnect(self, request):
        """A user is connecting to the server.
        """
        print("Client connecting: {0}".format(request.peer))


    def onOpen(self):
        """The connection to the client has been opened
        """
        self.clientManager = self.factory.getClientManager()
        self.client = self.clientManager.provisionClient(protocolClient=self)

    def onMessage(self, payload, isBinary):
        """Callback for when the client has sent a message to the server.
        """
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            self.client.handleMessage(payload.decode('utf8'))

    def onClose(self, wasClean, code, reason):
        """Callback when the connection is closed.

        This is called when self.sendClose() is called.
        """
        print("WebSocket connection closed: {0}".format(reason))

    def connectionLost(self, reason):
        """Callback when connection has been dropped from server.

        This is called everytime the connection is dropped. Be that from
        quitting or otherwise.
        """

    def getUniqueId(self):
        """Get a unique ID for this connection.

        Will return the port of the connection. That should be unique.
        """
        parts = self.peer.split(':')
        unique_id = parts[2]
        return unique_id


class MyWebSocketServerFactory(WebSocketServerFactory):
    """Demo Factory.

    The reason behind this factory is to just demo how the websocket server
    factory works.
    """

    def __init__(self, *args, **kwargs):
        """Define self.clients as a dictionary.
        """b
        super(MyWebSocketServerFactory, self).__init__(*args, **kwargs)
        self.game = None

    def getClientManager(self):
        return self.game.clientManager

if __name__ == '__main__':
    try:
        import asyncio
    except ImportError:
        # Trollius >= 0.3 was renamed
        import trollius as asyncio

    factory = MyWebSocketServerFactory(u"ws://127.0.0.1:8080", debug=False)
    factory.protocol = MyServerProtocol
    factory.game = Game()

    loop = asyncio.get_event_loop()
    factory.game.core_loop = loop
    coro = loop.create_server(factory, '0.0.0.0', 8080)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
