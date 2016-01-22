#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from ekko.tests.unit.api import base


class TestImages(base.BaseApiTest):

    def setup(self):
        super(TestImages, self).setUp()

    def test_backup(self):
        data = self.get_json('/images/backup')
        self.assertEqual('backup()', data['called'])

    def test_restore(self):
        data = self.get_json('/images/restore')
        self.assertEqual('restore()', data['called'])
