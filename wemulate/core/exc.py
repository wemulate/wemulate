class WEmulateError(Exception):
    """Generic errors."""

    pass


class WEmulateValidationError(WEmulateError):
    """Validation errors"""

    def __init__(self, message="A validation error occured"):
        self.message = message
        super().__init__(self.message)


class WEmulateExecutionError(WEmulateError):
    """Execution errors"""

    def __init__(self, message="An unknown execution error occured"):
        self.message = message
        super().__init__(self.message)


class WEmulateConfigNotFoundError(WEmulateError):
    """Config file not found error"""

    def __init__(self, message="No configuration file was found"):
        self.message = message
        super().__init__(self.message)


class WEmulateFileError(WEmulateError):
    """Error during writing/reading files"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class WEmulateDatabaseError(WEmulateError):
    """Error during database operation"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
