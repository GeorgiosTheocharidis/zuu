"""Defines zuul exceptions"""


class ZuulException(Exception):
    """Generic Zuul Exception."""


class RoomAlreadyExists(ZuulException):
    """Room already exists."""


class RoomDoesNotExist(ZuulException):
    """Room does not exist."""


class UnsupportedCommand(ZuulException):
    """Unsupported command."""


class FailedToExecuteAction(ZuulException):
    """Failed to execute action."""


class CommandCannotBeExecuted(ZuulException):
    """Command cannot be executed."""


class ThePlayerWonTheGame(ZuulException):
    """The player won the game."""
