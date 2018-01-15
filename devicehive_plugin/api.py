from devicehive_plugin.api_request import PluginRequest, TopicRequest


class Api(object):
    def __init__(self, transport, access_token, topic_name):
        self._transport = transport
        self._access_token = access_token
        self._topic_name = topic_name
        self._connected = True

    @property
    def connected(self):
        return self._connected

    @property
    def transport(self):
        return self._transport

    def authenticate(self):
        request = PluginRequest(self)
        request.action('authenticate')
        request.set_payload('token', self._access_token)
        return request.execute()

    def subscribe(self):
        request = TopicRequest(self)
        request.action('subscribe')
        request.set_payload('t', [self._topic_name])
        return request.execute()

    def unsubscribe(self):
        request = TopicRequest(self)
        request.action('unsubscribe')
        request.set_payload('t', [self._topic_name])
        return request.execute()

    def disconnect(self):
        self._connected = False
        if not self._transport.connected:
            return
        self._transport.disconnect()
