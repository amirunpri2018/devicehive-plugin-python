class Api(object):
    def __init__(self, api, credentials, topic_name):
        self._api = api
        self._credentials = credentials
        self._topic_name = topic_name

    def authorize(self):
        data = {
            "t": "plugin",
            "a": "authenticate",
            "p": {"token": self._credentials['auth_token']}
        }
        self._transport.request(data)

    def subscribe(self):
        data = {
            "t": "topic",
            "a": "subscribe",
            "p": {"t": [self._topic_name]}
        }
        self._transport.request(data)
