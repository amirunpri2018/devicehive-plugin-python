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


import threading
import pytest
import time
import six
from devicehive import DeviceHive, DeviceHiveApi
from six.moves import range as six_range
from six.moves.urllib import parse as url_parse
from collections import defaultdict

from devicehive_plugin import Handler, Plugin
from tests.devicehive_plugin_api import PluginApi

if six.PY2:
    class TimeoutError(OSError):
        pass


class TestHandler(Handler):
    """Test handler class."""

    def __init__(self, api, handle_connect, handle_notification):
        super(TestHandler, self).__init__(api)
        self._handle_connect = handle_connect
        self._handle_notification = handle_notification
        self.data = {}

    def handle_connect(self):
        self._handle_connect(self)
        if not self._handle_notification:
            self.disconnect()

    def handle_notification(self, notification):
        if not self._handle_notification:
            return
        self._handle_notification(self, notification)

    def disconnect(self):
        self.api.disconnect()


class Test(object):
    """Test class."""

    # entity types
    USER_ENTITY = 'user'
    DEVICE_ENTITY = 'device'
    NETWORK_ENTITY = 'network'
    DEVICE_TYPE_ENTITY = 'device_type'

    def __init__(self, transport_url, user_role, credentials):
        self._transport_url = transport_url
        self._user_role = user_role
        self._credentials = credentials
        self._transport_name = DeviceHive.transport_name(self._transport_url)
        self._entity_ids = defaultdict(list)
        self._is_handle_timeout = False

        assert self.http_transport, 'Plugin API available only by HTTP'

    def _generate_id(self, key=None):
        time_key = repr(time.time()).replace('.', '')
        if not key:
            return '%s-%s-%s' % (self._transport_name, self._user_role,
                                 time_key)
        return '%s-%s-%s-%s' % (self._transport_name, key, self._user_role,
                                time_key)

    def generate_id(self, key=None, entity_type=None):
        entity_id = self._generate_id(key=key)
        self._entity_ids[entity_type].append(entity_id)
        return entity_id

    def generate_ids(self, key=None, entity_type=None, count=1):
        base_entity_id = self._generate_id(key=key)
        entity_ids = ['%s-%s' % (base_entity_id, i) for i in six_range(count)]
        self._entity_ids[entity_type].extend(entity_ids)
        return base_entity_id, entity_ids

    @property
    def entity_ids(self):
        return self._entity_ids

    @property
    def transport_name(self):
        return self._transport_name

    @property
    def http_transport(self):
        return self._transport_name == 'http'

    @property
    def is_user_client(self):
        return self._user_role == 'client'

    @property
    def is_user_admin(self):
        return self._user_role == 'admin'

    def only_client_implementation(self):
        if self.is_user_client:
            return
        pytest.skip('Implemented only for "client" user role.')

    def only_admin_implementation(self):
        if self.is_user_admin:
            return
        pytest.skip('Implemented only for "admin" user role.')

    def _on_handle_timeout(self, plugin):
        plugin.handler.api.disconnect()
        self._is_handle_timeout = True

    def device_hive_api(self):
        return DeviceHiveApi(self._transport_url, **self._credentials)

    def plugin_api(self):
        return PluginApi(self._transport_url, **self._credentials)

    def run(self, proxy_endpoint, topic_name, handle_connect,
            handle_notification=None, handle_timeout=60):
        handler_kwargs = {'handle_connect': handle_connect,
                          'handle_notification': handle_notification}
        plugin = Plugin(TestHandler, **handler_kwargs)
        timeout_timer = threading.Timer(handle_timeout, self._on_handle_timeout,
                                        args=(plugin,))
        timeout_timer.setDaemon(True)
        timeout_timer.start()
        credentials = dict(self._credentials, auth_url=self._transport_url)
        plugin.connect(proxy_endpoint, topic_name, **credentials)
        timeout_timer.cancel()

        if self._is_handle_timeout:
            raise TimeoutError('Waited too long for handle.')
