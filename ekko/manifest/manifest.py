#!/usr/bin/python

# Copyright 2016 Intel corporation
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

# TODO(inc0): change it to stevedore plugins
from ekko.manifest.drivers.sqlite_driver import ManifestSQLite


class Manifest(object):
    def __init__(self, manifest_file):
        self.manifest_file = manifest_file
        self.manifest_driver = ManifestSQLite(manifest_file)

    @staticmethod
    def create_manifest(backupset_id):
        return ManifestSQLite.create(backupset_id)

    def write_manifest(self, header, segments):
        self.manifest_driver.write_manifest(header, segments)
        # TODO(inc0): increase reference count in redis
