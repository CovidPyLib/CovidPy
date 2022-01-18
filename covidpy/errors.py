
class InvalidDCC(Exception):
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details

class DCCError(Exception):
    pass