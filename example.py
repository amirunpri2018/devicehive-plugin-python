from devicehive_plugin.handler import Handler
from devicehive_plugin.plugin import Plugin

access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJwYXlsb2FkIjp7ImEiOlswXSwiZSI6MjA4MzY3NDI1ODc4MiwidCI6MSwidHBjIjoicGx1Z2luX3RvcGljXzgxNTkwNGNmLWU1YzUtNGViYy04NjNkLTUyYjNmOTNmMGNmMCJ9fQ.52qdDOSDWfr-PiI68R-MZjCV1MIOOAaI0AXEThlRyoQ'
url = 'ws://127.0.0.1:3000'
topic = 'plugin_topic_815904cf-e5c5-4ebc-863d-52b3f93f0cf0'


class ExampleHandler(Handler):
    def handle_message(self, message):
        print(message)


def main():
    p = Plugin(ExampleHandler)
    p.connect(url, topic, access_token=access_token)


if __name__ == '__main__':
    main()
