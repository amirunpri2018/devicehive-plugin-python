import json
import socket
import threading
import time
import sys
import websocket
from six.moves import queue

from devicehive_plugin.message import Message


class Transport(object):

    REQUEST_ID_KEY = 'id'
    REQUEST_ACTION_KEY = 'a'
    RESPONSE_SUCCESS_STATUS = 0
    RESPONSE_ERROR_STATUS = 1
    RESPONSE_STATUS_KEY = 's'
    RESPONSE_PAYLOAD_KEY = 'p'
    RESPONSE_ERROR_KEY = 'm'

    def __init__(self, api_class, api_options, error_class):
        self._connected = False
        self._websocket = websocket.WebSocket()
        self._response_sleep_time = None
        self._event_queue = queue.Queue()
        self._handler = api_class(self, **api_options)
        self._responses = {}
        self._error_class = error_class

    def _ensure_not_connected(self):
        if not self._connected:
            return
        raise self._error_class('Connection has already created.')

    def _ensure_connected(self):
        if self._connected:
            return
        raise self._error_class('Connection has not created.')

    def _connection(self, url, options):
        try:
            self._connect(url, **options)
            self._receive()
            self._disconnect()
        except:
            self._exception_info = sys.exc_info()

    def connect(self, url, **options):
        self._ensure_not_connected()
        self._connection_thread = threading.Thread(target=self._connection,
                                                   args=(url, options))
        self._connection_thread.name = 'transport-connection'
        self._connection_thread.daemon = True
        self._connection_thread.start()

    def disconnect(self):
        self._ensure_connected()
        self._connected = False

    # def send(self, data):
    #     self._websocket.send(self._encode(data))

    def is_alive(self):
        return self._connection_thread.is_alive()

    def _connect(self, url, **options):
        timeout = options.pop('timeout', None)
        response_sleep_time = options.pop('response_sleep_time', 1e-6)
        pong_timeout = options.pop('pong_timeout', None)
        self._websocket.timeout = timeout
        self._response_sleep_time = response_sleep_time
        self._websocket_call(self._websocket.connect, url, **options)
        self._connected = True
        event_thread = threading.Thread(target=self._event)
        event_thread.name = 'transport-event'
        event_thread.daemon = True
        event_thread.start()

        if pong_timeout:
            ping_thread = threading.Thread(target=self._ping,
                                           args=(pong_timeout,))
            ping_thread.name = 'transport-ping'
            ping_thread.daemon = True
            ping_thread.start()

        # auth_data = {
        #     "t": "plugin",
        #     "a": "authenticate",
        #     "p": {"token": self._access_token}
        # }
        #
        # self._websocket.send(self._encode(auth_data))
        #
        # self._receive()

    def _handle_event(self, event):
        self._handler.handle_event(event)

    def _receive(self):
        while self._connected:
            event = self._event_queue.get()
            self._handle_event(event)
            self._event_queue.task_done()

    def _disconnect(self):
        self._websocket_call(self._websocket.close)
        self._pong_received = False
        self._event_queue = []
        self._responses = {}
        # self._handle_disconnect()

    def _encode(self, value):
        return json.dumps(value)

    def _decode(self, value):
        return json.loads(value)

    def _event(self):
        while self._connected:
            opcode, data = self._websocket_call(self._websocket.recv_data, True)
            if opcode in (websocket.ABNF.OPCODE_TEXT,
                          websocket.ABNF.OPCODE_BINARY):
                if opcode == websocket.ABNF.OPCODE_TEXT:
                    data = data.decode('utf-8')
                event = self._decode(data)
                message = Message(event)
                request_id = event.get(self.REQUEST_ID_KEY)
                if not request_id:
                    self._event_queue.put(message)
                    # self._event_queue.append(event)
                    continue
                self._responses[request_id] = event
                continue

            if opcode == websocket.ABNF.OPCODE_PONG:
                self._pong_received = True
                continue
            if opcode == websocket.ABNF.OPCODE_CLOSE:
                return

    def _ping(self, pong_timeout):
        while self._connected:
            try:
                self._websocket_call(self._websocket.ping)
            except:
                self._connected = False
                return
            self._pong_received = False
            time.sleep(pong_timeout)
            if not self._pong_received:
                self._connected = False
                return

    def _websocket_call(self, websocket_method, *args, **kwargs):
        try:
            return websocket_method(*args, **kwargs)
        except (websocket.WebSocketException, socket.error) as websocket_error:
            error = websocket_error
        raise self._error_class(error)

    def _request(self, request_id, action, request):
        request[self.REQUEST_ID_KEY] = request_id
        request[self.REQUEST_ACTION_KEY] = action
        self._websocket_call(self._websocket.send, self._encode(request))

    def _receive_response(self, request_id, timeout):
        start_time = time.time()
        while time.time() - timeout < start_time:
            response = self._responses.get(request_id)
            if response:
                del self._responses[request_id]
                return response
            time.sleep(self._response_sleep_time)
        raise self._error_class('Response timeout.')

    def async_request(self, request_id, action, request, **params):
        self._ensure_connected()
        self._request(request_id, action, request)

    def request(self, request_id, action, request, **params):
        self._ensure_connected()
        timeout = params.pop('timeout', 30)
        self._request(request_id, action, request)
        return self._receive_response(request_id, timeout)
