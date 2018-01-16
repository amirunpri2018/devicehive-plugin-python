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


class ApiResponse(object):
    SUCCESS_STATUS = 0
    ID_KEY = 'id'
    TYPE_KEY = 't'
    ACTION_KEY = 'a'
    STATUS_KEY = 's'
    PAYLOAD_KEY = 'p'
    ERROR_KEY = 'm'

    def __init__(self, response):
        self._id = response.pop(self.ID_KEY)
        self._code = response.pop(self.TYPE_KEY)
        self._action = response.pop(self.ACTION_KEY)
        self._success = response.pop(self.STATUS_KEY) == self.SUCCESS_STATUS
        self._response = response.get(self.PAYLOAD_KEY)
        self._error = self._response.pop(self.ERROR_KEY, None)

    @property
    def id(self):
        return self._id

    @property
    def action(self):
        return self._action

    @property
    def success(self):
        return self._success

    @property
    def code(self):
        return self._code

    @property
    def error(self):
        return self._error

    @property
    def response(self):
        return self._response
