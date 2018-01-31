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


import json
import logging
import requests

from tests.devicehive_plugin_api.token import Token


__all__ = ['PluginApi', 'PluginApiError']
logger = logging.getLogger(__name__)


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
        logger.debug('Request: method=%s url=%s params=%s data=%s',
                     method, url, params, data)
        response = requests.request(method, url, params=params, json=data,
                                    headers=headers)
        content = response.content
        logger.debug('Response: code=%s content=%s', response.status_code,
                     response.content)
        if content:
            content = json.loads(content)

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
                      device_type_ids=(), network_ids=(), names=(),
                      subscribe_insert_commands=True,
                      subscribe_update_commands=False,
                      subscribe_notifications=False):

        parameters = parameters if parameters is not None else {}

        method = 'POST'
        url = 'plugin'
        params = {
            'deviceId': device_id,
            'deviceTypeIds': device_type_ids,
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

    def update_plugin(self, topic_name, name=None, description=None,
                      parameters=None, device_id=None, device_type_ids=None,
                      network_ids=None, names=None,
                      subscribe_insert_commands=None,
                      subscribe_update_commands=None,
                      subscribe_notifications=None):

        method = 'PUT'
        url = 'plugin'
        params = {
            'topicName': topic_name,
        }
        if name is not None:
            params['name'] = name
        if description is not None:
            params['description'] = description
        if parameters is not None:
            params['parameters'] = json.dumps(parameters)
        if device_id is not None:
            params['deviceId'] = device_id
        if device_type_ids is not None:
            params['deviceTypeIds'] = device_type_ids
        if network_ids is not None:
            params['networkIds'] = network_ids
        if names is not None:
            params['names'] = names
        if subscribe_insert_commands is not None:
            params['returnCommands'] = subscribe_insert_commands
        if subscribe_update_commands is not None:
            params['returnUpdatedCommands'] = subscribe_update_commands
        if subscribe_notifications is not None:
            params['returnNotifications'] = subscribe_notifications

        return self.auth_request(method, url, params)

    def remove_plugin(self, topic_name):
        method = 'DELETE'
        url = 'plugin'
        params = {
            'topicName': topic_name
        }
        return self.auth_request(method, url, params)

    def list_plugins(self, name=None, name_pattern=None, topic_name=None,
                     status=None, user_id=None, sort_field=None,
                     sort_order=None, take=None, skip=None):
        method = 'GET'
        url = 'plugin'
        params = {
            'name': name,
            'namePattern': name_pattern,
            'topicName': topic_name,
            'status': status,
            'userId': user_id,
            'sortField': sort_field,
            'sortOrder': sort_order,
            'take': take,
            'skip': skip
        }
        return self.auth_request(method, url, params)
    

class PluginApiError(IOError):
    def __init__(self, code, message):
        self.code = code
        message = 'Code: %s Message %s' % (code, message)
        super(PluginApiError, self).__init__(message)
