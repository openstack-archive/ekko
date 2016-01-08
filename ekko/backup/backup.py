#!/usr/bin/python

# Copyright 2016 Intel corporation

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

import hashlib
import time

from ekko.manifest.manifest import Manifest


def read_sectors(device, segments, segment_size, backupset_id, compression,
                 encryption):
    with open(device, 'r') as dev:
        for segment in segments:
            dev.seek(segment_size * segment)
            data = dev.read(segment_size)
            checksum = hashlib.sha1()
            checksum.update(data)
            # TODO (inc0): encrypt and compress data
            meta = {
                'base': backupset_id,
                'incremental': segment,
                'compression': compression,
                'encryption': encryption,
                'checksum': checksum.hexdigest(),
            }
            yield data, meta


class Backup(object):
    def __init__(self, backupset_id, device, bitmap, incremental):
        self.incremental = incremental
        self.backupset_id = backupset_id
        self.device = device
        self.bitmap = bitmap
        self.segment_size = 4 * 1024 ** 2  # 4MB
        self.compression = 'gzip'
        self.encryption = 'aes'

    def _get_lastest_manifest_file(self, backupset_id):
        # fetch manifest from swift and save it to /dev/shm
        manifest = None
        if not manifest:
            manifest = Manifest.create_manifest(backupset_id)
        return manifest

    def get_segments_from_bitmap(self):
        # TODO(inc0): return iterable with changed segments
        return 3, [1, 3, 5]

    def make_backup(self):
        # turn on backup mode on device to lock up bitmap
        self.segment_count, segments = self.get_segments_from_bitmap()
        self.segments = []

        for data, meta in read_sectors(self, segments, self.segment_size,
                                       self.backupset_id, self.compression,
                                       self.encryption):
            self.segments.append(meta)
            # TODO(inc0): write data to swift
        self.make_manifest()
        # upload manifest to swift
        # remove manifest file from /dev/shm
        # reset bitmap, unlock backup_mode on device

    def prepare_header(self):
        header = {
            'timestamp': time.time(),
            'incremental': self.incremental,
            'segment_size': self.segment_size,
            'segment_count': self.segment_count,
        }
        return header

    def make_manifest(self):
        # copy latest manifest
        manifest_file = self._get_lastest_manifest_file(self.backupset_id)
        manifest = Manifest(manifest_file)
        header = self.prepare_header()
        manifest.write_manifest(header, self.segments)
