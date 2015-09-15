"""exceptions.py: This module defines exceptions that can be raised
within the ts7250v2 python package
"""


class TSError(Exception):
    """A generic error used as a base for other ts7250v2 errors"""
    def __init__(self, message, errno=None):
        self.errno = errno
        super(TSError, self).__init__(message)


class TSDIOError(TSError):
    """Generic error involving the DIO subsystem"""
    pass


class TSDIOArgError(TSDIOError):
    """Problem with function input argument"""
    pass


class TSUARTError(TSError):
    """Generic error involving the UART subsystems"""
    pass


class TSADCError(TSError):
    """Generic error involving the ADC subsystem"""
    pass


class TSSysconError(TSError):
    """Generic error involving the SYStem CONfiguration subsystem"""
    pass


class TSSysconArgError(TSSysconError):
    """Generic error involving arguments for SYStem CONfiguration subsystem functions"""
    pass
