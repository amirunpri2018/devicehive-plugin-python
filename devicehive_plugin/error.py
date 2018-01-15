class TransportError(IOError):
    pass


class ApiResponseError(TransportError):
    pass
