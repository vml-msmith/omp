class Command(object):
    command = None

    @classmethod
    def match(cls, pattern):
        if pattern == cls.command:
            return True
        return False

    @classmethod
    def execute(cls, client=None, obj=None, game=None):
        pass
