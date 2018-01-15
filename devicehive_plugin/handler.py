class Handler(object):
    def __init__(self, api):
        self._api = api

    @property
    def api(self):
        return self._api

    def handle_connect(self):
        pass

    def handle_message(self, message):
        pass
