# Copyright 2016 Intel corporation
# Copyright 2016 Sam Yaple
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

from oslo_utils import importutils


def load_manifest_driver(manifest_location, manifest_driver=None):
    if not manifest_driver:
        manifest_driver = 'sqlite.SQLiteDriver'

    return importutils.import_object_ns('ekko.manifest',
                                        manifest_driver,
                                        manifest_location)


class ManifestDriver(object):
    """Base class for manifest drivers

    """

    def __init__(self, manifest_file):
        self.conn = None
        self.manifest_file = manifest_file

    def get_metadata(self):
        raise NotImplementedError()

    def get_segments(self):
        raise NotImplementedError()

    def put_metadata(self, metadata):
        raise NotImplementedError()

    def put_segments(self, segments, metadata):
        raise NotImplementedError()
