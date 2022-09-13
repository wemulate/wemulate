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

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class WEmulateDatabaseError(WEmulateError):
    """Error during database operation"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class WemulateMgmtInterfaceError(WEmulateError):
    """Management Interface not found error"""

    def __init__(self, interface_name: str = "", message=""):
        if not message:
            if interface_name:
                self.message = f"The interface {interface_name} is not present on this device. Please provide a valid interface name"
            else:
                self.message = "There is no management interface configured. Please configure at least one with the wemulate config command before using other commands"
        super().__init__(self.message)
