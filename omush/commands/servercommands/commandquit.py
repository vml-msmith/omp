from ..command import Command

class CommandQuit(Command):
    command = "QUIT"

    @classmethod
    def execute(self, scope):
        scope.client.close()
