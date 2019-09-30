class Error(Exception):
    """Base class for exceptions in this module"""
    pass


class LocationNotFoundError(Error):
    """Exception raised when a location is not found by the Open Weather API.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error

    Methods:
        print_error() -- print a explanation of the error
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    def print_error(self):
        print("Error caused by input '%s'\n%s" % (self.expression, self.message))
