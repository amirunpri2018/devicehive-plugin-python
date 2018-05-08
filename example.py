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


url = 'ws://playground.devicehive.com/plugin/proxy/'
topic_name = 'PLUGIN_TOPIC_NAME'
plugin_access_token = 'PLUGIN_ACCESS_TOKEN'


class SimpleHandler(Handler):

    def handle_event(self, event):
        print(event.data)


def main():
    p = Plugin(SimpleHandler)
    p.connect(url, topic_name, plugin_access_token=plugin_access_token)


if __name__ == '__main__':
    main()
