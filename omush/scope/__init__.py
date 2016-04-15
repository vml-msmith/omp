class Scope(object):
    def __init__(object):
        self.game = None
        self.enactor = None
        self.executor = None
        self.caller = None


class CommandScope(Scope):
    def __init__(self, command, game, caller=None, client=None):
        super().__init__;
        self.command = command
        self.client = client
        self.game = game

        self.enactor = caller
        self.executor = caller
        self.caller = caller

class ActionScope(object):
    def __init__(self, commandScope=None):
        self.commandScope = commandScope
