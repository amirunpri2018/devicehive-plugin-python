import json
import threading
import time
import websocket
from six.moves import queue


class Handler(object):
    def handle_connect(self):
        pass

    def handle_event(self, event):
        print(event)


class Plugin(object):
    def __init__(self, handler_class, access_token):
        self._connected = False
        self._websocket = websocket.WebSocket()
        self._event_queue = queue.Queue()
        self._handler = handler_class()
        self._access_token = access_token

    def connect(self, url, **options):
        self._websocket.connect(url, **options)
        self._connected = True
        event_thread = threading.Thread(target=self._event)
        event_thread.name = 'transport-event'
        event_thread.daemon = True
        event_thread.start()

        pong_timeout = 0.2

        ping_thread = threading.Thread(target=self._ping, args=(pong_timeout,))
        ping_thread.name = 'transport-ping'
        ping_thread.daemon = True
        ping_thread.start()

        auth_data = {
            "t": "plugin",
            "a": "authenticate",
            "p": {"token": self._access_token}
        }

        self._websocket.send(self._encode(auth_data))

        self._receive()

    def _handle_event(self, event):
        self._handler.handle_event(event)

    def _receive(self):
        while self._connected:
            event = self._event_queue.get()
            self._handle_event(event)
            self._event_queue.task_done()

    def _encode(self, value):
        return json.dumps(value)

    def _decode(self, value):
        return json.loads(value)

    def _event(self):
        while self._connected:
            opcode, data = self._websocket.recv_data(True)
            if opcode in (websocket.ABNF.OPCODE_TEXT,
                          websocket.ABNF.OPCODE_BINARY):
                if opcode == websocket.ABNF.OPCODE_TEXT:
                    data = data.decode('utf-8')
                event = self._decode(data)
                self._event_queue.put(event)
            if opcode == websocket.ABNF.OPCODE_PONG:
                self._pong_received = True
                continue
            if opcode == websocket.ABNF.OPCODE_CLOSE:
                return

    def _ping(self, pong_timeout):
        while self._connected:
            try:
                self._websocket.ping()
            except:
                self._connected = False
                return
            self._pong_received = False
            time.sleep(pong_timeout)
            if not self._pong_received:
                self._connected = False
                return
