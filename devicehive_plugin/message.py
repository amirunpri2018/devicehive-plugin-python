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


class Message(object):

    TYPE_KEY = 't'

    ACTION_KEY = 'a'

    PAYLOAD_KEY = 'p'

    SUCCESS_KEY = 's'

    AUTHENTICATE_ACTION = 'authenticate'

    SUBSCRIBE_ACTION = 'subscribe'

    UNSUBSCRIBE_ACTION = 'unsubscribe'

    SUCCESS = 1

    def __init__(self, message=None):
        if not message:
            return
        self.type = message[self.TYPE_KEY]
        self.action = message[self.ACTION_KEY]
        self.payload = message[self.PAYLOAD_KEY]
        self.success = message.get(self.SUCCESS_KEY)

    @property
    def is_authenticate(self):
        return self.action == self.AUTHENTICATE_ACTION

    @property
    def is_subscribe(self):
        return self.action == self.SUBSCRIBE_ACTION

    @property
    def is_unsubscribe(self):
        return self.action == self.UNSUBSCRIBE_ACTION

    @property
    def is_success(self):
        return self.success == self.SUCCESS
