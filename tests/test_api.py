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


# TODO: fix this when server response will be fixed
proxy_endpoint = 'ws://playground-dev.devicehive.com/plugin/proxy/'


def test_create_plugin(test):
    plugin_api = test.plugin_api()
    name = test.generate_id('c-p')
    description = '%s-description' % name
    response = plugin_api.create_plugin(name, description)

    topic_name = response['topicName']

    assert isinstance(topic_name, six.string_types)

    # plugin_api.remove_plugin(topic_name)


def test_update_plugin(test):
    plugin_api = test.plugin_api()
    name = test.generate_id('u-p')
    description = '%s-description' % name
    response = plugin_api.create_plugin(name, description)

    topic_name = response['topicName']

    assert isinstance(topic_name, six.string_types)

    name = test.generate_id('c-p')
    description = '%s-description' % name

    # response = plugin_api.update_plugin(topic_name, name, description)

    print(response)

    # plugin_api.remove_plugin(topic_name)


def test_subscribe_command_insert(test):
    plugin_api = test.plugin_api()
    device_hive_api = test.device_hive_api()

    device_id = test.generate_id('s-c-i')
    device = device_hive_api.put_device(device_id)

    name = test.generate_id('s-c-i')
    description = '%s-description' % name

    response = plugin_api.create_plugin(name, description)

    topic_name = response['topicName']

    commands = []

    def handle_connect(handler):
        command_name = '%s-command' % device_id
        command = device.send_command(command_name)
        commands.append(command.id)

    def handle_notification(handler, notification):
        command_id = notification.content['command']['id']
        assert command_id in commands
        commands.remove(command_id)
        if commands:
            return
        device.remove()
        # plugin_api.remove_plugin(topic_name)
        handler.disconnect()

    test.run(proxy_endpoint, topic_name, handle_connect, handle_notification)
