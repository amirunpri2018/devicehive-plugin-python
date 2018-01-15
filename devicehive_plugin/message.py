class Message(object):

    ACTION_KEY = 'a'

    AUTHENTICATE_ACTION = 'authenticate'

    def __init__(self, message):
        self._message = message
        self._action = message[self.ACTION_KEY]

    @property
    def is_authenticate(self):
        return self._action == self.AUTHENTICATE_ACTION
