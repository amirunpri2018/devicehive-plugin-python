import uuid

from devicehive_plugin.api_response import ApiResponse
from devicehive_plugin.error import ApiResponseError


__all__ = ['BaseApiRequest', 'PluginRequest', 'TopicRequest']


class BaseApiRequest(object):
    _type = None

    def __init__(self, api):
        self._api = api
        self._action = None
        self._request = {}
        self._payload = {}

    @staticmethod
    def _uuid():
        return str(uuid.uuid4())

    def action(self, action):
        self._action = action

    def set(self, key, value):
        self._request[key] = value

    def set_payload(self, key, value):
        self._payload[key] = value

    def execute(self):
        request_id = self._uuid()
        response = self._api.transport.request(request_id, self._type,
                                               self._action, self._request,
                                               self._payload)
        api_response = ApiResponse(response)

        if api_response.success:
            return api_response.response

        raise ApiResponseError(api_response.error)


class PluginRequest(BaseApiRequest):
    _type = 'plugin'


class TopicRequest(BaseApiRequest):
    _type = 'topic'
