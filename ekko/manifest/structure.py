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

import time
from uuid import uuid4 as uuid


class Metadata(object):

    def __init__(self, incremental, sectors, segment_size=None,
                 timestamp=None, backupsets=None, backupset_id=None):
        self.timestamp = timestamp if timestamp else time.time()
        self.sectors = sectors
        self.incremental = incremental
        self.segment_size = 4 * 1024 ** 2  # 4MiB
        self.backupset_id = backupset_id if backupset_id else uuid().bytes
        self.backupsets = backupsets if backupsets else [self.backupset_id]


class Segment(object):
    __slots__ = ['backupset_id', 'incremental', 'segment',
                 'compression', 'encryption', 'segment_hash']

    def __init__(self, backupset_id, incremental, segment,
                 compression, encryption, segment_hash):
        self.backupset_id = backupset_id
        self.incremental = incremental
        self.segment = segment
        self.compression = compression
        self.encryption = encryption
        self.segment_hash = segment_hash
