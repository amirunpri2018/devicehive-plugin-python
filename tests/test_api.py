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


import six

from tests.devicehive_plugin_api.api import PluginApiError


def test_create_plugin(test):
    plugin_api = test.plugin_api()
    name = test.generate_id('c-p')
    description = '%s-description' % name
    plugin = plugin_api.create_plugin(name, description)

    topic_name = plugin['topicName']

    assert isinstance(topic_name, six.string_types)

    # TODO: uncomment after "plugin/delete" will be fixed
    # plugin_api.remove_plugin(topic_name)


def test_update_plugin(test):
    plugin_api = test.plugin_api()
    name = test.generate_id('u-p')
    description = '%s-description' % name
    plugin = plugin_api.create_plugin(name, description)

    topic_name = plugin['topicName']

    name = test.generate_id('u-p')
    description = '%s-description' % name
    parameters = {'parameters-key': 'parameters-value'}
    # TODO: uncomment after "plugin/update" will be fixed
    # plugin = plugin_api.update_plugin(topic_name, name, description, parameters)

    assert plugin['name'] == name
    assert plugin['description'] == description
    assert plugin['parameters'] == parameters

    # TODO: uncomment after "plugin/delete" will be fixed
    # plugin_api.remove_plugin(topic_name)
    try:
        plugin_api.update_plugin(topic_name, name)
        assert False
    except PluginApiError as plugin_api_error:
        if test.is_user_admin:
            assert plugin_api_error.code == 404
        else:
            assert plugin_api_error.code == 403


def test_remove_plugin(test):
    plugin_api = test.plugin_api()
    name = test.generate_id('r-p')
    description = '%s-description' % name
    plugin = plugin_api.create_plugin(name, description)

    topic_name = plugin['topicName']

    # TODO: uncomment after "plugin/delete" will be fixed
    # plugin_api.remove_plugin(topic_name)
    # try:
    #     plugin_api.remove_plugin(topic_name)
    #     assert False
    # except PluginApiError as plugin_api_error:
    #     if test.is_user_admin:
    #         assert plugin_api_error.code == 404
    #     else:
    #         assert plugin_api_error.code == 403


def test_list_plugin(test):
    plugin_api = test.plugin_api()
    test_id, plugin_names = test.generate_ids('l-p', test.PLUGIN_ENTITY, 2)
    options = [{'name': name, 'description': '%s-description' % name}
               for name in plugin_names]
    test_plugins = [plugin_api.create_plugin(**option) for option in options]
    plugins = plugin_api.list_plugins()
    assert len(plugins) >= len(options)
    name = options[0]['name']
    plugin, = plugin_api.list_plugins(name=name)
    assert plugin['name'] == name
    name_pattern = test.generate_id('l-p-n-e')
    assert not plugin_api.list_plugins(name_pattern=name_pattern)
    name_pattern = test_id + '%'
    plugins = plugin_api.list_plugins(name_pattern=name_pattern)
    assert len(plugins) == len(options)
    plugin_0, plugin_1 = plugin_api.list_plugins(name_pattern=name_pattern,
                                                 sort_field='name',
                                                 sort_order='ASC')
    assert plugin_0['name'] == options[0]['name']
    assert plugin_1['name'] == options[1]['name']
    plugin_0, plugin_1 = plugin_api.list_plugins(name_pattern=name_pattern,
                                                 sort_field='name',
                                                 sort_order='DESC')
    assert plugin_0['name'] == options[1]['name']
    assert plugin_1['name'] == options[0]['name']
    plugin, = plugin_api.list_plugins(name_pattern=name_pattern,
                                      sort_field='name', sort_order='ASC',
                                      take=1)
    assert plugin['name'] == options[0]['name']
    plugin, = plugin_api.list_plugins(name_pattern=name_pattern,
                                      sort_field='name', sort_order='ASC',
                                      take=1, skip=1)
    assert plugin['name'] == options[1]['name']
    [plugin_api.remove_plugin(test_plugin['topicName'])
     for test_plugin in test_plugins]
