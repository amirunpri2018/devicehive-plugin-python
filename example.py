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
