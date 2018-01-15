from devicehive_plugin.api import Api


class ApiHandler(object):
    def __init__(self, transport, credentials, topic_name, handler_class,
                 handler_args, handler_kwargs, api_init=True):
        self._transport = transport
        self._api = Api(self._transport, credentials, topic_name)
        self._handler = handler_class(self._api, *handler_args,
                                      **handler_kwargs)
        self._api_init = api_init
        self._handle_connect = False

    def handle_message(self, message):
        self._handler.handle_message(message)

    def handle_connect(self):
        if self._api_init:
            self.authorize()
            self.subscribe()

        if not self._handle_connect:
            self._handle_connect = True
            self._handler.handle_connect()

    def handle_disconnect(self):
        self._handler.handle_disconnect()

