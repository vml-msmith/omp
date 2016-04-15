from autobahn.asyncio.websocket import WebSocketServerFactory
from network.serverprotocol import OMushServerProtocol
from network.clientmanager import OMushConnectedClientManager
from network.client import OMushConnectedClient

from commands.servercommands.commandquit import CommandQuit
from commands.logincommands.commandlogin import CommandLogin
from commands.communicationcommands.commandsay import CommandSay

from database import Database
from database import DatabaseRoom
from database import DatabasePlayer
from notifier import Notifier



class OMushClientCommandList(object):
    def get_socket_commands(self):
        return [CommandQuit]

    def get_not_logged_in_commands(self):
        return [CommandLogin]

    def get_logged_in_commands(self):
        return [CommandSay]

class OMushConnectedClientFactory(object):
    def provision(self, protocol_client, connected_client_manager):
        client = OMushConnectedClient(protocol_client=protocol_client,
                                      connected_client_manager=connected_client_manager)
        client.command_list = OMushClientCommandList()

        return client

class Game(object):
    def __init__(self):
        self.client_manager = OMushConnectedClientManager()
        self.client_manager.factory = OMushConnectedClientFactory()
        self.client_manager.game = self
        self.database = Database()
        self.notifier = Notifier()
        self.setup_database()

    def setup_database(self):
        from database import DatabaseRoom
        from database import DatabasePlayer

        room_zero = DatabaseRoom(name="Room Zero")
        self.database.add_object(room_zero)
        one = DatabasePlayer(name="One")
        one.set_password("pass")
        one._location = 0
        self.database.add_object(one)

        room_zero.register_with_notifier(self.notifier)
        one.register_with_notifier(self.notifier)

class MyWebSocketServerFactory(WebSocketServerFactory):
    """Demo Factory.

    The reason behind this factory is to just demo how the websocket server
    factory works.
    """

    def __init__(self, *args, **kwargs):
        """Define self.clients as a dictionary.
        """
        super().__init__(*args, **kwargs)
        self.game = None

    def get_client_manager(self):
        return self.game.client_manager

if __name__ == '__main__':
    try:
        import asyncio
    except ImportError:
        import trollius as asyncio

    factory = MyWebSocketServerFactory(u"ws://127.0.0.1:8080")
    factory.protocol = OMushServerProtocol
    factory.game = Game()

    loop = asyncio.get_event_loop()
    factory.game.core_loop = loop
    coro = loop.create_server(factory, '0.0.0.0', 8080)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
        import logging
        logging.warning('Watch out!') # will print a message to the console
        logging.info('I told you so') # will not print anything

    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
