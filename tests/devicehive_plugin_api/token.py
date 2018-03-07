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


class Token(object):

    AUTH_HEADER_NAME = 'Authorization'
    AUTH_HEADER_VALUE_PREFIX = 'Bearer '

    def __init__(self, api, credentials):
        self._api = api
        self._login = credentials.get('login')
        self._password = credentials.get('password')
        self._refresh_token = credentials.get('refresh_token')
        self._access_token = credentials.get('access_token')

    def _tokens(self):
        method = 'POST'
        url = 'token'
        data = {
            'login': self._login,
            'password': self._password,
        }
        tokens = self._api.request(method, url, data=data)
        self._refresh_token = tokens['refreshToken']
        self._access_token = tokens['accessToken']

    @property
    def access_token(self):
        return self._access_token

    @property
    def auth_header(self):
        auth_header_name = self.AUTH_HEADER_NAME
        auth_header_value = self.AUTH_HEADER_VALUE_PREFIX + self._access_token
        return {auth_header_name: auth_header_value}

    def refresh(self):
        if not self._refresh_token:
            raise TokenError('Can\'t refresh token without "refresh_token"')
        method = 'POST'
        url = 'token/refresh'
        data = {
            'refreshToken': self._refresh_token
        }
        tokens = self._api.request(method, url, data=data)
        self._access_token = tokens['accessToken']

    def auth(self):
        if self._refresh_token:
            self.refresh()
        elif self._login and self._password:
            self._tokens()
        elif self._login:
            raise TokenError('Password required.')
        elif self._password:
            raise TokenError('Login required.')


class TokenError(IOError):
    pass
