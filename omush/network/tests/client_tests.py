import unittest
from omush.network.client import OMushConnectedClient

class MockSocketCommand(object):
    command = "none"

    @classmethod
    def match(cls, pattern, obj=None):
        if pattern == cls.command:
            return True
        return False

    @classmethod
    def provision(cls):
        return cls()

    def execute(self, scope):
        scope.client.notify(self.command)

class MockSocketCommandConnected(MockSocketCommand):
    command = "connected"

class MockSocketCommandLogin(MockSocketCommand):
    command = "login"

class MockSocketCommandQuit(MockSocketCommand):
    command = "QUIT"


class MockSocketCommandQuitTwo(MockSocketCommand):
    command = "QUIT"

    def execute(self, client=None, obj=None, game=None):
        client.notify("QUIT2")

class MockCommandTest(MockSocketCommand):
    command = "test"

class MockProtocolClient(object):
    def __init__(self):
        self.output = None
        self.has_quit = False

    def notify(self, msg):
        self.output = msg

    def sendClose(self):
        self.has_quit = True


class MockCommandList(object):
    def get_socket_commands(self):
        return [MockCommandTest,
                MockSocketCommandQuit,
                MockSocketCommandQuitTwo]

    def get_not_logged_in_commands(self):
        return [MockCommandTest, MockSocketCommandLogin, MockCommandTest]

    def get_logged_in_commands(self):
        return [MockCommandTest, MockSocketCommandConnected, MockCommandTest]

class MockClientManager(object):
    def __init__(self):
        self.game = object()


class ClientTest(unittest.TestCase):
    def setUp(self):
        """Create a default mock protocol"""
        self._protocol_client = MockProtocolClient()

    def _create_connected_client(self):
        """Internal: Create a connected client with a new manager."""
        client_manager = MockClientManager()
        client = OMushConnectedClient(protocol_client=self._protocol_client,
                                      connected_client_manager=client_manager)
        return client


    def test_client_quit(self):
        """Client object should have a quit and send quit to the protocol."""
        client = self._create_connected_client()
        self.assertFalse(self._protocol_client.has_quit)
        client.close()
        self.assertTrue(self._protocol_client.has_quit)

    def test_handle_message_socket_level(self):
        """Socket level commands should be checked and executed before any other
        command pareser gets a hold of the command. These should be executable
        no matter if a client is logged in or not."""
        client = self._create_connected_client()
        # We need to pass in a command to the socket level.
        client.command_list = MockCommandList()
        client.handle_message("QUIT")

        self.assertEquals(self._protocol_client.output, "QUIT")
        # The commands should no longer try to execute once a result has been
        # found. Command2 should never be hit because QUIT is found first.
        self.assertNotEquals(self._protocol_client.output, "QUIT2")


    def test_handle_message_login_level(self):
        """Should only use login level commandsfor non logged in clients."""
        # Login commands should only be executed if the client is in a
        # "Login Screen" state. Once the user has logged in, these commands
        # should no longer be availble.
        client = self._create_connected_client()
        # We need to pass in a command to the socket level.
        client.command_list = MockCommandList()

        client.handle_message("login")

        self.assertEquals(self._protocol_client.output, "login")

        user_object = object()
        client.set_logged_in_user(user_object)
        client.handle_message("login")
        self.assertNotEquals(self._protocol_client.output, "login")

    def test_handle_message_connected_level(self):
        """Should only use connected commands for logged in client."""
        # Connected commands should only work when a user is connected.
        client = self._create_connected_client()

        # We need to pass in a command to the socket level.
        client.command_list = MockCommandList()
        client.handle_message("connected")

        self.assertNotEquals(self._protocol_client.output, "connected")

        user_object = object()
        client.set_logged_in_user(user_object)
        client.handle_message("connected")
        self.assertEquals(self._protocol_client.output, "connected")

    def test_notify(self):
        """Notify method will call notify on the protocol."""
        client = self._create_connected_client()
        client.notify("This is a test")
        self.assertEquals(self._protocol_client.output, "This is a test")


if __name__ == '__main__':
    unittest.main()
