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


import pytest
import six

from tests.devicehive_plugin_api.api import PluginApiError


def test_create_plugin(test):
    plugin_api = test.plugin_api()
    name = test.generate_id('c-p')
    description = '%s-description' % name
    response = plugin_api.create_plugin(name, description)

    topic_name = response['topicName']

    assert isinstance(topic_name, six.string_types)

    # TODO: uncomment after "plugin/delete" will be fixed
    # plugin_api.remove_plugin(topic_name)
    #
    # try:
    #     plugin_api.remove_plugin(topic_name)
    #     assert False
    # except PluginApiError as plugin_api_error:
    #     if test.is_user_admin:
    #         assert plugin_api_error.code == 404
    #     else:
    #         assert plugin_api_error.code == 403


def test_update_plugin(test):
    plugin_api = test.plugin_api()
    name = test.generate_id('u-p')
    description = '%s-description' % name
    response = plugin_api.create_plugin(name, description)

    topic_name = response['topicName']

    assert isinstance(topic_name, six.string_types)

    name = test.generate_id('c-p')
    description = '%s-description' % name
    # TODO: uncomment after "plugin/update" will be fixed
    # response = plugin_api.update_plugin(topic_name, name, description)

    # TODO: add some assertion

    # TODO: uncomment after "plugin/delete" will be fixed
    # plugin_api.remove_plugin(topic_name)


def test_list_plugin(test):
    # TODO: Write test after "plugin/list" will be added
    pytest.skip('Test is not implemented yet')
