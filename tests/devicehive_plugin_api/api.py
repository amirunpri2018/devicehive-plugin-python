# Copyright (C) 2018 DataArt
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================


import requests

from tests.devicehive_plugin_api.token import Token

__all__ = ['PluginApi']


class PluginApi(object):
    """
    Simple wrapper to communicate with API thought REST
    """

    SUCCESS_CODES = [200, 201, 204]

    def __init__(self, url, **credentials):
        if not url.endswith('/'):
            url += '/'
        self._url = url
        self._token = Token(self, credentials)

    def request(self, method, url, params=None, data=None, headers=None):
        url = self._url + url
        response = requests.request(method, url, params=params, json=data,
                                    headers=headers)
        content = response.json()
        if response.status_code in self.SUCCESS_CODES:
            return content

        raise PluginApiError(response.status_code, content['message'])

    def auth_request(self, method, url, params=None, data=None, headers=None):
        if headers is None:
            headers = {}

        headers.update(self._token.auth_header)
        try:
            return self.request(method, url, params, data, headers)
        except PluginApiError as plugin_api_error:
            if plugin_api_error.code != 401:
                raise

        self._token.auth()
        headers.update(self._token.auth_header)
        return self.request(method, url, params, data, headers)

    def create_plugin(self, name, description, parameters=None, device_id=None,
                      device_types_ids=(), network_ids=(), names=(),
                      subscribe_insert_commands=True,
                      subscribe_update_commands=False,
                      subscribe_notifications=False):

        parameters = parameters if parameters is not None else {}

        method = 'POST'
        url = 'plugin'
        params = {
            'deviceId': device_id,
            'deviceTypeIds': device_types_ids,
            'networkIds': network_ids,
            'names': names,
            'returnCommands': subscribe_insert_commands,
            'returnUpdatedCommands': subscribe_update_commands,
            'returnNotifications': subscribe_notifications,
        }
        data = {
            'name': name,
            'description': description,
            'parameters': parameters
        }
        return self.auth_request(method, url, params, data)

    def update_plugin(self, topic, name=None, description=None, parameters=None,
                      device_id=None, device_types_ids=(), network_ids=(),
                      names=(), subscribe_insert_commands=True,
                      subscribe_update_commands=False,
                      subscribe_notifications=False):

        parameters = parameters if parameters is not None else {}

        method = 'PUT'
        url = 'plugin'
        params = {
            'topicName': topic,
            'deviceId': device_id,
            'deviceTypeIds': device_types_ids,
            'networkIds': network_ids,
            'names': names,
            'returnCommands': subscribe_insert_commands,
            'returnUpdatedCommands': subscribe_update_commands,
            'returnNotifications': subscribe_notifications,
            'name': name,
            'description': description,
            'parameters': parameters
        }
        return self.auth_request(method, url, params)

    def remove_plugin(self, topic):
        method = 'DELETE'
        url = 'plugin'
        params = {
            'topicName': topic
        }
        return self.auth_request(method, url, params)

    def list_plugins(self):
        raise NotImplementedError
    

class PluginApiError(IOError):
    def __init__(self, code, message):
        self.code = code
        message = 'Code: %s Message %s' % (code, message)
        super(PluginApiError, self).__init__(message)
