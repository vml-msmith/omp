import unittest
from omush.commands.servercommands.commandquit import CommandQuit

class MockClient(object):
    def __init__(self):
        self.output = None
        self.is_closed = False

    def close(self):
        self.is_closed = True

    def notify(self, message):
        self.output = message


class CommandQuitTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_command_quit_matches_input(self):
        self.assertTrue(CommandQuit.match("QUIT"))
        self.assertFalse(CommandQuit.match("quit"))

    def test_command_quit_sends_quit_to_client(self):
        client = MockClient()
        client.is_closed = False
        CommandQuit.execute(client=client,
                            obj=None,
                            game=None)
        self.assertTrue(client.is_closed)

    def test_command_quit_says_goodbye(self):
        pass


if __name__ == '__main__':
    unittest.main()
