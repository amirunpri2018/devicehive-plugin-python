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


def test_subscribe_events(test):
    plugin_api = test.plugin_api()
    device_hive_api = test.device_hive_api()

    def init_data():
        device_id = test.generate_id('d-s-e', test.DEVICE_ENTITY)
        device = device_hive_api.put_device(device_id)
        command_name = '%s-command' % device_id
        notification_name = '%s-notification' % device_id

        return {'device': device,
                'command_name': command_name,
                'notification_name': notification_name}

    def send_data(device, command_name, notification_name):
        command = device.send_command(command_name)
        command.status = 'status'
        command.save()
        notification = device.send_notification(notification_name)
        return command.id, command.id, notification.id

    def handle_connect(handler):
        event_ids = send_data(handler.data['device'],
                              handler.data['command_name'],
                              handler.data['notification_name'])
        command_insert_id, command_update_id, notification_id = event_ids
        handler.data['event_ids'] = [command_insert_id, command_update_id,
                                     notification_id]

    def handle_event(handler, event):
        assert event.data.id in handler.data['event_ids']
        handler.data['event_ids'].remove(event.data.id)
        if handler.data['event_ids']:
            return
        handler.data['device'].remove()
        handler.disconnect()

    data = init_data()
    name = test.generate_id('d-s-e', test.PLUGIN_ENTITY)
    description = '%s-description' % name
    plugin = plugin_api.create_plugin(name, description,
                                      device_id=data['device'].id,
                                      subscribe_insert_commands=True,
                                      subscribe_update_commands=True,
                                      subscribe_notifications=True)
    topic_name = plugin['topicName']
    test.run(proxy_endpoint, topic_name, handle_connect, handle_event,
             data=data)
    plugin_api.remove_plugin(topic_name)

    # =========================================================================
    def handle_connect(handler):
        event_ids = send_data(handler.data['device'],
                              handler.data['command_name'],
                              handler.data['notification_name'])
        command_insert_id, command_update_id, notification_id = event_ids
        handler.data['event_ids'] = [command_insert_id, command_update_id]

    data = init_data()
    name = test.generate_id('d-s-e', test.PLUGIN_ENTITY)
    description = '%s-description' % name
    plugin = plugin_api.create_plugin(name, description,
                                      device_id=data['device'].id,
                                      subscribe_insert_commands=True,
                                      subscribe_update_commands=True,
                                      subscribe_notifications=False)
    topic_name = plugin['topicName']
    test.run(proxy_endpoint, topic_name, handle_connect, handle_event,
             data=data)
    plugin_api.remove_plugin(topic_name)

    # =========================================================================
    def handle_connect(handler):
        event_ids = send_data(handler.data['device'],
                              handler.data['command_name'],
                              handler.data['notification_name'])
        command_insert_id, command_update_id, notification_id = event_ids
        handler.data['event_ids'] = [command_insert_id, notification_id]

    data = init_data()
    name = test.generate_id('d-s-e', test.PLUGIN_ENTITY)
    description = '%s-description' % name
    plugin = plugin_api.create_plugin(name, description,
                                      device_id=data['device'].id,
                                      subscribe_insert_commands=True,
                                      subscribe_update_commands=False,
                                      subscribe_notifications=True)
    topic_name = plugin['topicName']
    test.run(proxy_endpoint, topic_name, handle_connect, handle_event,
             data=data)
    plugin_api.remove_plugin(topic_name)


def test_subscribe_insert_commands(test):
    plugin_api = test.plugin_api()
    device_hive_api = test.device_hive_api()

    def init_data():
        device_id = test.generate_id('d-s-i-c', test.DEVICE_ENTITY)
        device = device_hive_api.put_device(device_id)
        command_names = ['%s-name-%s' % (device_id, i) for i in range(2)]

        return {'device': device, 'command_names': command_names}

    def send_data(device, command_names):
        return [device.send_command(name).id for name in command_names]

    def handle_connect(handler):
        handler.data['command_ids'] = send_data(handler.data['device'],
                                                handler.data['command_names'])

    def handle_command_insert(handler, command):
        assert command.id in handler.data['command_ids']
        handler.data['command_ids'].remove(command.id)
        if handler.data['command_ids']:
            return
        handler.data['device'].remove()
        handler.disconnect()

    data = init_data()
    name = test.generate_id('d-s-i-c', test.PLUGIN_ENTITY)
    description = '%s-description' % name
    plugin = plugin_api.create_plugin(name, description,
                                      device_id=data['device'].id)
    topic_name = plugin['topicName']
    test.run(proxy_endpoint, topic_name, handle_connect,
             handle_command_insert=handle_command_insert, data=data)
    plugin_api.remove_plugin(topic_name)

    # =========================================================================
    data = init_data()
    name = test.generate_id('d-s-i-c', test.PLUGIN_ENTITY)
    description = '%s-description' % name
    plugin = plugin_api.create_plugin(name, description,
                                      device_id=data['device'].id,
                                      names=data['command_names'][:1])
    topic_name = plugin['topicName']
    test.run(proxy_endpoint, topic_name, handle_connect,
             handle_command_insert=handle_command_insert, data=data)
    plugin_api.remove_plugin(topic_name)


def test_subscribe_update_commands(test):
    plugin_api = test.plugin_api()
    device_hive_api = test.device_hive_api()

    def init_data():
        device_id = test.generate_id('d-s-u-c', test.DEVICE_ENTITY)
        device = device_hive_api.put_device(device_id)
        command_names = ['%s-name-%s' % (device_id, i) for i in range(2)]

        return {'device': device, 'command_names': command_names}

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

    def handle_command_update(handler, command):
        assert command.id in handler.data['command_ids']
        assert command.status == 'status'
        handler.data['command_ids'].remove(command.id)
        if handler.data['command_ids']:
            return
        handler.data['device'].remove()
        handler.disconnect()

    data = init_data()
    name = test.generate_id('d-s-u-c', test.PLUGIN_ENTITY)
    description = '%s-description' % name
    plugin = plugin_api.create_plugin(name, description,
                                      device_id=data['device'].id,
                                      subscribe_insert_commands=False,
                                      subscribe_update_commands=True)
    topic_name = plugin['topicName']
    test.run(proxy_endpoint, topic_name, handle_connect,
             handle_command_update=handle_command_update, data=data)
    plugin_api.remove_plugin(topic_name)

    # =========================================================================
    data = init_data()
    name = test.generate_id('d-s-u-c', test.PLUGIN_ENTITY)
    description = '%s-description' % name
    plugin = plugin_api.create_plugin(name, description,
                                      device_id=data['device'].id,
                                      names=data['command_names'][:1],
                                      subscribe_insert_commands=False,
                                      subscribe_update_commands=True)
    topic_name = plugin['topicName']
    test.run(proxy_endpoint, topic_name, handle_connect,
             handle_command_update=handle_command_update, data=data)
    plugin_api.remove_plugin(topic_name)


def test_subscribe_insert_notifications(test):
    plugin_api = test.plugin_api()
    device_hive_api = test.device_hive_api()

    def init_data():
        device_id = test.generate_id('d-s-n', test.DEVICE_ENTITY)
        device = device_hive_api.put_device(device_id)
        notification_names = ['%s-name-%s' % (device_id, i) for i in range(2)]

        return {'device': device, 'notification_names': notification_names}

    def send_data(device, notification_names):
        return [device.send_notification(name).id for name in
                notification_names]

    def handle_connect(handler):
        handler.data['notification_ids'] = send_data(
            handler.data['device'], handler.data['notification_names'])

    def handle_notification(handler, notification):
        assert notification.id in handler.data['notification_ids']
        handler.data['notification_ids'].remove(notification.id)
        if handler.data['notification_ids']:
            return
        handler.data['device'].remove()
        handler.disconnect()

    data = init_data()
    name = test.generate_id('d-s-n', test.PLUGIN_ENTITY)
    description = '%s-description' % name
    plugin = plugin_api.create_plugin(name, description,
                                      device_id=data['device'].id,
                                      subscribe_insert_commands=False,
                                      subscribe_notifications=True)
    topic_name = plugin['topicName']
    test.run(proxy_endpoint, topic_name, handle_connect,
             handle_notification=handle_notification, data=data)
    plugin_api.remove_plugin(topic_name)

    # =========================================================================
    data = init_data()
    name = test.generate_id('d-s-n', test.PLUGIN_ENTITY)
    description = '%s-description' % name
    plugin = plugin_api.create_plugin(name, description,
                                      device_id=data['device'].id,
                                      names=data['notification_names'][:1],
                                      subscribe_insert_commands=False,
                                      subscribe_notifications=True)
    topic_name = plugin['topicName']
    test.run(proxy_endpoint, topic_name, handle_connect,
             handle_notification=handle_notification, data=data)
    plugin_api.remove_plugin(topic_name)
