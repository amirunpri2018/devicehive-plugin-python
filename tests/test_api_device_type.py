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


from six.moves import range


# TODO: remove this after server response will be fixed
proxy_endpoint = 'ws://playground-dev.devicehive.com/plugin/proxy/'


def test_subscribe_insert_commands(test):
    test.only_admin_implementation()

    plugin_api = test.plugin_api()
    device_hive_api = test.device_hive_api()

    def init_data():
        dt_name = test.generate_id('dt-s-i-c', test.DEVICE_TYPE_ENTITY)
        dt_description = '%s-description' % dt_name
        device_type = device_hive_api.create_device_type(dt_name,
                                                         dt_description)

        device_id = test.generate_id('dt-s-i-c', test.DEVICE_ENTITY)
        device = device_hive_api.put_device(device_id,
                                            device_type_id=device_type.id)
        command_names = ['%s-name-%s' % (device_id, i) for i in range(2)]

        return {'device': device,
                'device_type': device_type,
                'command_names': command_names}

    def send_data(device, command_names):
        return [device.send_command(name).id for name in command_names]

    def handle_connect(handler):
        handler.data['command_ids'] = send_data(handler.data['device'],
                                                handler.data['command_names'])

    def handle_notification(handler, notification):
        command_id = notification.content['command']['id']
        assert command_id in handler.data['command_ids']
        handler.data['command_ids'].remove(command_id)
        if handler.data['command_ids']:
            return
        handler.data['device'].remove()
        handler.data['device_type'].remove()
        handler.disconnect()

    data = init_data()
    name = test.generate_id('dt-s-i-c')
    description = '%s-description' % name
    response = plugin_api.create_plugin(
        name, description, device_type_ids=[data['device_type'].id])
    topic_name = response['topicName']
    test.run(proxy_endpoint, topic_name, handle_connect, handle_notification,
             data)
    # TODO: uncomment after "plugin/delete" will be fixed
    # plugin_api.remove_plugin(topic_name)

    # =========================================================================
    def handle_connect(handler):
        handler.data['command_ids'] = send_data(handler.data['device'],
                                                handler.data['command_names'])

    def handle_notification(handler, notification):
        command_id = notification.content['command']['id']
        assert command_id in handler.data['command_ids']
        handler.data['command_ids'].remove(command_id)
        if handler.data['command_ids']:
            return
        handler.data['device'].remove()
        handler.data['device_type'].remove()
        handler.disconnect()

    data = init_data()
    name = test.generate_id('dt-s-i-c')
    description = '%s-description' % name
    response = plugin_api.create_plugin(
        name, description, device_type_ids=[data['device_type'].id],
        names=data['command_names'][:1])
    topic_name = response['topicName']
    test.run(proxy_endpoint, topic_name, handle_connect, handle_notification,
             data)
    # TODO: uncomment after "plugin/delete" will be fixed
    # plugin_api.remove_plugin(topic_name)


def test_subscribe_update_commands(test):
    test.only_admin_implementation()

    plugin_api = test.plugin_api()
    device_hive_api = test.device_hive_api()

    def init_data():
        dt_name = test.generate_id('dt-s-u-c', test.DEVICE_TYPE_ENTITY)
        dt_description = '%s-description' % dt_name
        device_type = device_hive_api.create_device_type(dt_name,
                                                         dt_description)

        device_id = test.generate_id('dt-s-u-c', test.DEVICE_ENTITY)
        device = device_hive_api.put_device(device_id,
                                            device_type_id=device_type.id)
        command_names = ['%s-name-%s' % (device_id, i) for i in range(2)]

        return {'device': device,
                'device_type': device_type,
                'command_names': command_names}

    def send_data(device, command_names):
        command_ids = []
        for name in command_names:
            command = device.send_command(name)
            command.status = 'status'
            command.save()
            command_ids.append(command.id)

        return command_ids

    def handle_connect(handler):
        handler.data['command_ids'] = send_data(handler.data['device'],
                                                handler.data['command_names'])

    def handle_notification(handler, notification):
        command_id = notification.content['command']['id']
        assert command_id in handler.data['command_ids']
        assert notification.content['command']['status'] == 'status'
        handler.data['command_ids'].remove(command_id)
        if handler.data['command_ids']:
            return
        handler.data['device'].remove()
        handler.data['device_type'].remove()
        handler.disconnect()

    data = init_data()
    name = test.generate_id('dt-s-u-c')
    description = '%s-description' % name
    response = plugin_api.create_plugin(
        name, description, device_type_ids=[data['device_type'].id],
        subscribe_insert_commands=False, subscribe_update_commands=True)
    topic_name = response['topicName']
    test.run(proxy_endpoint, topic_name, handle_connect, handle_notification,
             data)
    # TODO: uncomment after "plugin/delete" will be fixed
    # plugin_api.remove_plugin(topic_name)

    # =========================================================================
    def handle_connect(handler):
        handler.data['command_ids'] = send_data(handler.data['device'],
                                                handler.data['command_names'])

    def handle_notification(handler, notification):
        command_id = notification.content['command']['id']
        assert command_id in handler.data['command_ids']
        assert notification.content['command']['status'] == 'status'
        handler.data['command_ids'].remove(command_id)
        if handler.data['command_ids']:
            return
        handler.data['device'].remove()
        handler.data['device_type'].remove()
        handler.disconnect()

    data = init_data()
    name = test.generate_id('dt-s-u-c')
    description = '%s-description' % name
    response = plugin_api.create_plugin(
        name, description, device_type_ids=[data['device_type'].id],
        names=data['command_names'][:1], subscribe_insert_commands=False,
        subscribe_update_commands=True)
    topic_name = response['topicName']
    test.run(proxy_endpoint, topic_name, handle_connect, handle_notification,
             data)
    # TODO: uncomment after "plugin/delete" will be fixed
    # plugin_api.remove_plugin(topic_name)


def test_subscribe_notifications(test):
    test.only_admin_implementation()

    plugin_api = test.plugin_api()
    device_hive_api = test.device_hive_api()

    def init_data():
        dt_name = test.generate_id('dt-s-n', test.DEVICE_TYPE_ENTITY)
        dt_description = '%s-description' % dt_name
        device_type = device_hive_api.create_device_type(dt_name,
                                                         dt_description)

        device_id = test.generate_id('dt-s-n', test.DEVICE_ENTITY)
        device = device_hive_api.put_device(device_id,
                                            device_type_id=device_type.id)
        notification_names = ['%s-name-%s' % (device_id, i) for i in range(2)]

        return {'device': device,
                'device_type': device_type,
                'notification_names': notification_names}

    def send_data(device, notification_names):
        return [device.send_notification(name).id for name in
                notification_names]

    def handle_connect(handler):
        handler.data['notification_ids'] = send_data(
            handler.data['device'], handler.data['notification_names'])

    def handle_notification(handler, notification):
        notification_id = notification.content['notification']['id']
        assert notification_id in handler.data['notification_ids']
        handler.data['notification_ids'].remove(notification_id)
        if handler.data['notification_ids']:
            return
        handler.data['device'].remove()
        handler.data['device_type'].remove()
        handler.disconnect()

    data = init_data()
    name = test.generate_id('dt-s-n')
    description = '%s-description' % name
    response = plugin_api.create_plugin(
        name, description, device_type_ids=[data['device_type'].id],
        subscribe_insert_commands=False,
        subscribe_notifications=True)
    topic_name = response['topicName']
    test.run(proxy_endpoint, topic_name, handle_connect, handle_notification,
             data)
    # TODO: uncomment after "plugin/delete" will be fixed
    # plugin_api.remove_plugin(topic_name)

    # =========================================================================
    def handle_connect(handler):
        handler.data['notification_ids'] = send_data(
            handler.data['device'], handler.data['notification_names'])

    def handle_notification(handler, notification):
        notification_id = notification.content['notification']['id']
        assert notification_id in handler.data['notification_ids']
        handler.data['notification_ids'].remove(notification_id)
        if handler.data['notification_ids']:
            return
        handler.data['device'].remove()
        handler.data['device_type'].remove()
        handler.disconnect()

    data = init_data()
    name = test.generate_id('dt-s-n')
    description = '%s-description' % name
    response = plugin_api.create_plugin(
        name, description, device_type_ids=[data['device_type'].id],
        names=data['notification_names'][:1], subscribe_insert_commands=False,
        subscribe_notifications=True)
    topic_name = response['topicName']
    test.run(proxy_endpoint, topic_name, handle_connect, handle_notification,
             data)
    # TODO: uncomment after "plugin/delete" will be fixed
    # plugin_api.remove_plugin(topic_name)