#!/usr/bin/env python

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

# Copied and licensed from https://github.com/SamYaple/osdk


import argparse
from hashlib import sha1
import math
import os
import sys

from ekko.manifest import structure as manifest_structure
from six.moves import range
from stevedore import driver


def parse_args():
    parser = argparse.ArgumentParser(description='Backup Block Device')
    parser.add_argument('--backup', required=True,
                        help='Path to backup file or device')
    parser.add_argument('--manifest', required=True,
                        help='manifest file')
    parser.add_argument('--cbt', required=False,
                        help='change block tracking info')
    parser.add_argument('--backend', required=False, default='raw',
                        choices=['raw'], help='backend driver')
    parser.add_argument('--driver', required=False, default='sqlite',
                        choices=['osdk', 'sqlite'], help='manifest driver')
    return parser.parse_args()


def read_segments(segments, metadata, backend):
    size = metadata.segment_size
    reads = [(segment * size, size) for segment in segments[:-1]]

    # NOTE(SamYaple): If are reading the last segment on the disk and the
    # normal read size is greater than the disk, shrink the read size to the
    # appropriate size.
    if segments[-1] * size > metadata.size_of_disk:
        reads.append((segments[-1] * size, metadata.size_of_disk % size))
    else:
        reads.append((segments[-1] * size, size))

    # NOTE(SamYaple): One of the few optimizations we may ever need to do is
    # the dropping of segments that are 100% full of zero bytes. This can
    # potentially greatly reduce the size of a manifest but more importantantly
    # it reduces the number of objects we will need to track
    with open('/dev/zero', 'rb') as f:
        zero_blob = f.read(size)

    for start, data in backend.get_data(reads):
        if data == zero_blob:
            continue
        yield manifest_structure.Segment(
            metadata.backupset_id,
            metadata.incremental,
            start / size,
            0,
            0,
            sha1(data).digest()
        )


def check_manifest(manifest_file):
    return os.path.isfile(manifest_file)


def main():
    args = parse_args()
    if check_manifest(args.manifest):
        print('manifest exists; exiting')
        return

    manifest = driver.DriverManager(
        namespace='ekko.manifest.drivers',
        name=args.driver,
        invoke_on_load=True,
        invoke_args=[args.manifest]
    ).driver

    backend = driver.DriverManager(
        namespace='ekko.backup.backend',
        name=args.backend,
        invoke_on_load=True,
        invoke_args=[args.backup]
    ).driver

    size_of_disk = backend.get_size()
    incremental = 0
    metadata = manifest_structure.Metadata(incremental, size_of_disk)

    manifest.initialize()
    manifest.put_metadata(metadata)

    segments_list = list(range(0, int(math.ceil(
        float(size_of_disk)/metadata.segment_size))))
    segments = read_segments(segments_list, metadata, backend)

    manifest.put_segments(segments, metadata)

if __name__ == '__main__':
    sys.exit(main())
