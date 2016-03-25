import unittest
from omush.commands.logincommands import CommandLogin

class MockClient(object):
    def __init__(self):
        self.output = None
        self.is_closed = False

    def close(self):
        self.is_closed = True

    def notify(self, message):
        self.output = message


class MockClient(object):
    def __init__(self):
        self.user_object = None
        self.output = None

    def set_logged_in_user(self, user):
        self.user_object = user;

    def notify(self, message):
        self.output = message

class MockGame(object):
    def __init__(self):
        self.database = MockDatabase()

class MockPlayerObject(object):

    def __init__(self, name, password):
        self._password = password
        self.name = name

    def match_password(self, password):
        if self._password == password:
            return True
        return False

class MockDatabase(object):
    def __init__(self):
        self.objects = []

    def find_player_by_name(self, name):
        for k in self.objects:
            if k.name == name:
                return k

        return None

class CommandLoginTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_command_login_matches_input(self):
        """Command should match the pattern:

        connect <username> <password>
        connect '<spaced> <username>' <password>

        The command should be case insensitive for the connect portion.
        """

        self.assertTrue(CommandLogin.match("connect michael password"))
        self.assertTrue(CommandLogin.match("connect    michael password"))
        # Require exactly two arguments
        self.assertFalse(CommandLogin.match("login michael smith password"))
        self.assertFalse(CommandLogin.match("connect michael smith password"))
        self.assertFalse(CommandLogin.match("connect"))
        self.assertFalse(CommandLogin.match("connect michael"))
        self.assertTrue(CommandLogin.match('connect "michael smith" password'))
        self.assertFalse(CommandLogin.match('connect "" password'))


    def test_arg_matcher(self):
        """Test the arg matcher returns the correct args"""
        args = CommandLogin.get_args("connect michael password")
        self.assertEquals(args['name'], 'michael')
        self.assertEquals(args['password'], 'password')
        args = CommandLogin.get_args("connect 'michael smith' password")
        self.assertEquals(args['name'], 'michael smith')
        self.assertEquals(args['password'], 'password')

    def test_execute(self):
        client = MockClient()
        client.user_object = None
        game = MockGame()
        game.database.objects.append(MockPlayerObject('michael', 'password'))

        CommandLogin.execute(pattern='connect michael password',
                             client=client,
                             obj=None,
                             game=game)
        self.assertNotEquals(client.user_object, None)
        client.user_object = None
        CommandLogin.execute(pattern='connect michael pass',
                             client=client,
                             obj=None,
                             game=game)
        self.assertEquals(client.user_object, None)
        self.assertEquals(client.output, "Username or password not found.")

        CommandLogin.execute(pattern='connect other password',
                             client=client,
                             obj=None,
                             game=game)
        self.assertEquals(client.user_object, None)

    def test_execute_notifies_user_on_fail(self):
        client = MockClient()
        client.user_object = None
        game = MockGame()
        game.database.objects.append(MockPlayerObject('michael', 'blahblah'))

        CommandLogin.execute(pattern='connect michael password',
                             client=client,
                             obj=None,
                             game=game)
        self.assertEquals(client.output, "Username or password not found.")

if __name__ == '__main__':
    unittest.main()
