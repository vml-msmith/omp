"""Defines commands that can be used from the login screen.
"""
from ..command import Command
import re


class CommandSay(Command):
    """
    """
    from ...actions.actionlogin import ActionSay

    command = "say"
    action = ActionSay

    @classmethod
    def _get_matchers(cls):
        """Return an array of regular expressions that will match the c ommand.
        """
        return [re.compile('^' + \
                           cls.command + \
                           r'\s+(?P<say>.+)$'),
                re.compile(r'^\"\s+(?P<say>.+)$'),
                re.compile(r'^\"(?P<say>.+)$')
        ]


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

        action = self.action()
        action.enact(scope)
