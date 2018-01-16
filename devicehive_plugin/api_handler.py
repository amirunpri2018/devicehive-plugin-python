from devicehive_plugin.api import Api
from devicehive_plugin.message import Message


__all__ = ['ApiHandler']


class ApiHandler(object):
    def __init__(self, transport, credentials, topic_name, handler_class,
                 handler_args, handler_kwargs, api_init=True):
        self._transport = transport
        # TODO: add logic to renew access_token
        self._credentials = credentials
        access_token = self._credentials.pop('access_token')
        self._api = Api(self._transport, access_token, topic_name)
        self._handler = handler_class(self._api, *handler_args,
                                      **handler_kwargs)
        self._api_init = api_init
        self._handle_connect = False

    @property
    def handler(self):
        return self._handler

    def handle_event(self, event):
        self._handler.handle_message(Message(event))

    def handle_connect(self):
        if self._api_init:
            self._api.authenticate()
            self._api.subscribe()

        if not self._handle_connect:
            self._handle_connect = True
            self._handler.handle_connect()

    def handle_disconnect(self):
        self._handler.handle_disconnect()
