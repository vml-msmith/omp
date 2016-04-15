class Command(object):
    command = None

    @classmethod
    def match(cls, pattern):
        if pattern == cls.command:
            return True
        return False
    @classmethod
    def _get_matchers(cls):
        pass

    @classmethod
    def match(cls, pattern):
        """Return True if the command matches pattern."""
        if pattern == cls.command:
            return True
        matchers = cls._get_matchers()
        if matchers is not None:
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
        for re_pattern in self._get_matchers():
            match = re_pattern.match(pattern)
            if match is not None:
                return match.groupdict()


    @classmethod
    def provision(cls):
        return cls()

    def execute(self, scope):
        pass
