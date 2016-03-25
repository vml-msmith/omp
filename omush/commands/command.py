class Command(object):
    command = None

    @classmethod
    def match(cls, pattern):
        if pattern == cls.command:
            return True
        return False

    @classmethod
    def provision(cls):
        return cls()

    def execute(self, pattern=None, client=None, obj=None, game=None):
        pass
