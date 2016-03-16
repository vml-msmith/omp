import unittest
from omush.network.client import OMushConnectedClient

executed_command = None

class MockSocketCommand(object):
    @classmethod
    def match(cls, pattern, obj=None):
        if pattern == cls.command:
            return True
        return False

    @classmethod
    def execute(cls, client=None, obj=None, game=None):
        global executed_command
        executed_command = cls.command

class MockSocketCommandConnected(MockSocketCommand):
    command = "connected"

class MockSocketCommandLogin(MockSocketCommand):
    command = "login"

class MockSocketCommandQuit(MockSocketCommand):
    command = "QUIT"


class MockSocketCommandQuitTwo(MockSocketCommand):
    command = "QUIT"

    def execute(client=None, obj=None, game=None):
        global executed_command
        executed_command = "QUIT2"

class MockCommandTest(MockSocketCommand):
    command = "test"

class MockProtocolClient(object):
    def notify(self, msg):
        self.output = msg


class MockCommandList(object):
    def get_socket_commands(self):
        return [MockCommandTest, MockSocketCommandQuit, MockSocketCommandQuitTwo]

    def get_not_logged_in_commands(self):
        return [MockCommandTest, MockSocketCommandLogin, MockCommandTest]

    def get_logged_in_commands(self):
        return [MockCommandTest, MockSocketCommandConnected, MockCommandTest]

class MockClientManager(object):
    def __init__(self):
        self.game = object()

class ClientTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_handle_message(self):
        client = OMushConnectedClient()
        client.command_list = MockCommandList()
        client.handleMessage(message="Test")

    def test_handle_message_socket_level(self):
        """Socket level commands should be checked and executed before any other
        command pareser gets a hold of the command. These should be executable
        no matter if a client is logged in or not."""

        client = OMushConnectedClient()
        # We need to pass in a command to the socket level.
        client.command_list = MockCommandList()
        client.clientManager = MockClientManager()
        client.handleMessage("QUIT")

        global executed_command
        self.assertEquals(executed_command, "QUIT")
        # The commands should no longer try to execute once a result has been
        # found. Command2 should never be hit because QUIT is found first.
        self.assertNotEquals(executed_command, "QUIT2")


    def test_handle_message_login_level(self):
        # Login commands should only be executed if the client is in a
        # "Login Screen" state. Once the user has logged in, these commands
        # should no longer be availble.
        client = OMushConnectedClient()
        # We need to pass in a command to the socket level.
        client.command_list = MockCommandList()
        client.clientManager = MockClientManager()
        client.handleMessage("login")

        global executed_command
        self.assertEquals(executed_command, "login")

        executed_command = None
        user_object = object()
        client.setLoggedInUser(user_object)
        client.handleMessage("login")
        self.assertNotEquals(executed_command, "login")

    def test_handle_message_connected_level(self):
        # Connected commands should only work when a user is connected.
        client = OMushConnectedClient()
        # We need to pass in a command to the socket level.
        client.command_list = MockCommandList()
        client.clientManager = MockClientManager()
        client.handleMessage("connected")

        global executed_command
        self.assertNotEquals(executed_command, "connected")

        executed_command = None
        user_object = object()
        client.setLoggedInUser(user_object)
        client.handleMessage("connected")
        self.assertEquals(executed_command, "connected")

    def test_notify(self):
        client = OMushConnectedClient()
        client.protocolClient = MockProtocolClient()
        client.notify("This is a test")
        self.assertEquals(client.protocolClient.output, "This is a test")


if __name__ == '__main__':
    unittest.main()
