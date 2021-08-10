class WEmulateError(Exception):
    """Generic errors."""

    pass


class WEmulateValidationError(WEmulateError):
    def __init__(self, message="A validation error occured"):
        self.message = message
        super().__init__(self.message)


class WEmulateExecutionError(WEmulateError):
    def __init__(self, message="An unknown execution error occured"):
        self.message = message
        super().__init__(self.message)


class WEmulateConfigNotFoundError(WEmulateError):
    def __init__(self, message="No configuration file was found"):
        self.message = message
        super().__init__(self.message)


class WEmulateFileError(WEmulateError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
