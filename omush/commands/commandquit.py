from .command import Command

class CommandQuit(Command):
    command = "QUIT"

    @classmethod
    def execute(cls, client=None, obj=None, game=None):
        client.close()
