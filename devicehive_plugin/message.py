class Message(object):

    TYPE_KEY = 't'

    ACTION_KEY = 'a'

    PAYLOAD_KEY = 'p'

    SUCCESS_KEY = 's'

    AUTHENTICATE_ACTION = 'authenticate'

    SUBSCRIBE_ACTION = 'subscribe'

    UNSUBSCRIBE_ACTION = 'unsubscribe'

    SUCCESS = 1

    def __init__(self, message=None):
        if not message:
            return
        self.type = message[self.TYPE_KEY]
        self.action = message[self.ACTION_KEY]
        self.payload = message[self.PAYLOAD_KEY]
        self.success = message.get(self.SUCCESS_KEY)

    @property
    def is_authenticate(self):
        return self.action == self.AUTHENTICATE_ACTION

    @property
    def is_subscribe(self):
        return self.action == self.SUBSCRIBE_ACTION

    @property
    def is_unsubscribe(self):
        return self.action == self.UNSUBSCRIBE_ACTION

    @property
    def is_success(self):
        return self.success == self.SUCCESS
