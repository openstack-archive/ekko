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

# NOTE(SamYaple): This driver is an expiremental driver used for testing. It is
# an optimized file used to compare to and optimized the sqlite driver. This
# driver may fall in and out of maintenance and will only be used as a sanity
# check for the sqlite driver for as long as this NOTE is present.

import os
from struct import pack

from ekko.manifest import drivers


class OSDKManifest(drivers.BaseManifest):

    def initialize(self):
        with open(self.manifest_file, 'wb', 4096) as f:
            f.write(os.urandom(20))

    def put_segments(self, segments, metadata):
        with open(self.manifest_file, 'ab', 4096) as f:
            for segment in segments:
                f.write(pack(
                    '<2I2B20sI',
                    segment.incremental,
                    segment.segment,
                    segment.compression,
                    segment.encryption,
                    segment.segment_hash,
                    metadata.backupsets.index(segment.backupset_id)
                ))

    def put_metadata(self, metadata):
        with open(self.manifest_file, 'ab', 4096) as f:
            f.write(pack(
                '<2IQ24s',
                metadata.incremental,
                metadata.segment_size,
                metadata.size_of_disk,
                metadata.timestamp
            ))
            for backupset in metadata.backupsets:
                f.write(pack('<16s', backupset))
