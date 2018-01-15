class ApiResponse(object):
    SUCCESS_STATUS = 0
    ID_KEY = 'id'
    TYPE_KEY = 't'
    ACTION_KEY = 'a'
    STATUS_KEY = 's'
    PAYLOAD_KEY = 'p'
    ERROR_KEY = 'm'

    def __init__(self, response):
        self._id = response.pop(self.ID_KEY)
        self._code = response.pop(self.TYPE_KEY)
        self._action = response.pop(self.ACTION_KEY)
        self._success = response.pop(self.STATUS_KEY) == self.SUCCESS_STATUS
        self._response = response.get(self.PAYLOAD_KEY)
        self._error = self._response.pop(self.ERROR_KEY, None)

    @property
    def id(self):
        return self._id

    @property
    def action(self):
        return self._action

    @property
    def success(self):
        return self._success

    @property
    def code(self):
        return self._code

    @property
    def error(self):
        return self._error

    @property
    def response(self):
        return self._response
