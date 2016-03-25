from .command import Command
import re

import logging

class CommandLogin(Command):
    command = "connect"
    @classmethod
    def _get_matchers(cls):
        return [re.compile('^' + cls.command + '\s+[\'|\"](?P<name>[^\"][^\']+)[\'|\"]*\s+(?P<password>\S+)$'),
                re.compile('^' +  cls.command + '\s+(?P<name>\S+)\s+(?P<password>\S+)$')]

    @classmethod
    def match(cls, pattern):
        # Search for this one negative. It'll match:
        # connect '' password
        # If we don't do this, the next normal form will count this as correct.
        # Todo(msmith): Fix the next regex instead.
        p = re.compile('^' + cls.command + '\s+[\'|\"][\'|\"]*\s+(\S+)$')
        if p.match(pattern) is not None:
            return False

        for p in cls._get_matchers():
            match = p.match(pattern)
            if match is not None:
                return True

        return False

    @classmethod
    def get_args(cls, pattern):
        for p in cls._get_matchers():
            match = p.match(pattern)
            if match is not None:
                return match.groupdict()

    @classmethod
    def execute(cls,
                pattern=None,
                client=None,
                obj=None,
                game=None):
        args = cls.get_args(pattern)
        db = game.database
        player = db.find_player_by_name(args['name'])
        if player is not None:
            if player.match_password(args['password']):
                client.set_logged_in_user(player)
                return
        client.notify("Username or password not found.")
