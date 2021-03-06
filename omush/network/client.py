"""Module docstring
"""
from omush.scope import CommandScope

class OMushConnectedClient(object):
    """A client object that associates a socket connection and a user objec.t

    Handles the messages incomming from the socket.
    """
    def __init__(self, protocol_client, connected_client_manager):
        self.protocol_client = protocol_client
        self.connected_client_manager = connected_client_manager
        self.user_object = None
        self.command_list = None

    def set_logged_in_user(self, user):
        """Set the logged in user object."""
        self.user_object = user

    def notify(self, message):
        """Send a string notification to the connected socket."""
        self.protocol_client.notify(message)

    def close(self):
        self.notify("Goodbye.")
        self.protocol_client.sendClose()

    def handle_message(self, message):
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
        command = self._match_command_from_message(message)
        scope = CommandScope(command=message,
                             client=self,
                             game=self.connected_client_manager.game,
                             caller=self.user_object);
        if command is not None:
            import logging
            logging.warning('found it') # will print a message to the console
            command.provision().execute(scope);

        else:
            self._handle_unknown_message()

    def _handle_unknown_message(self):
        """The client sent a message we don't know how to handle."""
        # msmith(ENHANCEMENT): In the future, I think we should log the most
        # common HUH generating commands, including who issues them at what
        # point.
        self.protocol_client.notify("Huh?")

    def _match_command_from_message(self, message):
        """Internal method
        """
        command_list = self.command_list.get_socket_commands()
        if self.user_object is None:
            command_list = command_list + \
                           self.command_list.get_not_logged_in_commands()
        else:
            command_list = command_list + \
                           self.command_list.get_logged_in_commands()

        for value in command_list:
            if value.match(pattern=message):
                return value

        return None
