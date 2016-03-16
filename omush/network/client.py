class OMushConnectedClient(object):
    def __init__(self):
        self.user_object = None

    def setLoggedInUser(self, user):
        self.user_object = user

    def handleMessage(self, message):
        command = self._matchCommandFromMessage(message)
        if command is not None:
            command.execute(client = self,
                            game = self.clientManager.game)

    def _matchCommandFromMessage(self, message):
        command_list = self.command_list.get_socket_commands()
        if self.user_object is None:
            command_list = command_list + self.command_list.get_not_logged_in_commands()
        else:
            command_list = command_list + self.command_list.get_logged_in_commands()

        for value in command_list:
            if value.match(pattern = message):
                return value

        return None
