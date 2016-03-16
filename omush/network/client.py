class OMushConnectedClient(object):
    """A client object that associates a socket connection and a user objec.t

    Handles the messages incomming from the socket.
    """
    def __init__(self):
        self.user_object = None

    def setLoggedInUser(self, user):
        """Set the logged in user object."""
        self.user_object = user

    def notify(self, message):
        """Send a string notification to the connected socket."""
        self.protocolClient.notify(message)

    def handleMessage(self, message):
        """Handle a string message "input" to be executed from this client.

        This will attempt to match a command from the client and execute it
        if possible.

        Note there are three levels of commands:
          - Socket level: Useable by any connected client, does not reqire a
            user object to be logged in. These are executed first.
          - Login Screen level: These commands are useable only when there is
            not a user object associated with the connection. Not yet logged
            in.
          - Connected level: All the commands of the game. These include
            commands built into the server, exits and soft-coded commands.
        """
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
