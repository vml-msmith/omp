"""Handles all things related to an object being logged into"""

from .action import Action

class ActionLogin(Action):
    """Action that is enacted when a player logs in.

    This action should never be enacted on a non Player object."""

    def enact(self):
        # Check for bad enactor.
        # Trigger aconnect on object.
        # Trigger acconnect on location
        # Trigger aconnect on global.
        # Notify user that he's logged in.
        # Notify surroundings that a user has logged in.
        #  Location
        #  Objects in location
        # Notify pub/sub system? That might be a better idea for triggers!
        # Do Look
        pass
