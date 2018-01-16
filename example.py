import logging

from devicehive_plugin import Plugin, Handler


handler = logging.StreamHandler()
handler.setLevel('DEBUG')
logger = logging.getLogger('devicehive_plugin')
logger.addHandler(handler)
logger.setLevel('DEBUG')


url = 'ws://playground-dev.devicehive.com/plugin/proxy/'
topic = 'PLUGIN_TOPIC_NAME'
access_token = 'PLUGIN_AUTH_TOKEN'


class ExampleHandler(Handler):
    def handle_message(self, message):
        print(message)


def main():
    p = Plugin(ExampleHandler)
    p.connect(url, topic, access_token=access_token)


if __name__ == '__main__':
    main()
