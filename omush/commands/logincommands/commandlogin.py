"""Defines commands that can be used from the login screen.
"""
from ..command import Command
import re
from omush.scope import ActionScope

class CommandLogin(Command):
    """Define the connect <name> <password> command

    This command should only be use-able from the login screen. If user is found
    that matches the name and password, the client will be logged in and the
    ActionLogin action will be enacted for that user object.

    Variations of the command:
      - connect <name_with_no_space> <password>
      - connect "<name with spaces>" <password>
      - connect '<name with spaces>' <password>
    """

    from omush.actions.actionlogin import ActionLogin

    command = "connect"
    action = ActionLogin

    @classmethod
    def _get_matchers(cls):
        """Return an array of regular expressions that will match the c ommand.
        """
        return [re.compile('^' + \
                           cls.command + \
                           r'\s+[\'|\"](?P<name>[^\"][^\']+)[\'|\"]*\s+(?P<password>\S+)$'),
                re.compile('^' + \
                           cls.command + \
                           r'\s+(?P<name>\S+)\s+(?P<password>\S+)$')]

    @classmethod
    def match(cls, pattern):
        """Return True if the command matches pattern."""
        # Search for this one negative. It'll match:
        # connect '' password
        # If we don't do this, the next normal form will count this as correct.
        # TODO(msmith): Fix the next regex instead.
        re_pattern = re.compile('^' + \
                                cls.command + \
                                r'\s+[\'|\"][\'|\"]*\s+(\S+)$')
        if re_pattern.match(pattern) is not None:
            return False

        for re_pattern in cls._get_matchers():
            match = re_pattern.match(pattern)
            if match is not None:
                return True

        return False


    def get_args(self, pattern):
        """Return a dictionary of arguments from the command entered.

        Args:
          - name: The name of the user. This can contain spaces.
          - password: The password of the user in plain text.
        """
        matchers = self._get_matchers()
        if matchers is None:
            return []

        for re_pattern in self._get_matchers():
            match = re_pattern.match(pattern)
            if match is not None:
                return match.groupdict()

    def execute(self, scope):
        """Execute the command.

        Executing the command will search the database for a user object that
        matches the full name and hashed password supplied.

        If a player object is found, the client will be logged in and
        ActionLogin will be enacted for the client and object.

        If a player object is not found, the client will be notified with a
        failure message.
        """

        args = self.get_args(scope.command)
        database = scope.game.database
        player = database.find_player_by_name(args['name'])
        if player is not None:
            if player.match_password(args['password']):
                scope.client.set_logged_in_user(player)
                action = self.action()
                action.enact(scope=ActionScope(commandScope=scope))

                return

        scope.client.notify("Username or password not found.")
