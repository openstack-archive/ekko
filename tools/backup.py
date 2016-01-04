#!/usr/bin/python

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
from collections import namedtuple
# from hashlib import sha1
import os
import sys
from uuid import uuid4 as uuid

from ekko import manifest
import six


def parse_args():
    parser = argparse.ArgumentParser(description='Backup Block Device')
    parser.add_argument('--blockdev', required=True,
                        help='Block device to backup')
    parser.add_argument('--manifest', required=True,
                        help='manifest file')
    parser.add_argument('--cbt', required=True,
                        help='change block tracking info')
    return parser.parse_args()


def get_disk_size(device):
    f = os.open(device, os.O_RDONLY)
    try:
        return os.lseek(f, 0, os.SEEK_END)
    finally:
        os.close(f)


def read_segments(f, lst, size, backup):
    backup.segments = dict()
    backup.hashes = dict()
    Segment = namedtuple(
        'Segment',
        'base incremental compression encryption'
    )

    for segment in lst:
        # Do not actually do the backup

        # f.seek(segment * size, 0)
        # data = f.read(size)
        # if not data:
        #     raise Exception('Failed to read data')

        backup.segments[segment] = Segment(
            len(backup.metadata['bases']) - 1,
            backup.metadata['info'].incremental,
            0,
            0
        )
        # backup.hashes[segment] = sha1(data).digest()
        # Empty sha
        backup.hashes[segment] = str.encode('\0\0' * 20)


def check_manifest(manifest_file):
    return os.path.isfile(manifest_file)


def main():
    args = parse_args()
    segment_size = 4 * 1024**2  # 4MiB
    size_of_disk = get_disk_size(args.blockdev)
    num_of_sectors = int(size_of_disk / 512)
    num_of_segments = int(size_of_disk / segment_size)
    incremental = 0

    Info = namedtuple(
        'Info',
        'timestamp incremental segment_size sectors'
    )

    if check_manifest(args.manifest):
        print('manifest exists; exiting')
        return

    backup = manifest.Manifest(args.manifest)

    backup.metadata['info'] = Info(
        manifest.utctimestamp(),
        incremental,
        segment_size,
        num_of_sectors,
    )

    backup.metadata['bases'] = [uuid().bytes]
    segments_to_read = six.moves.range(0, num_of_segments - 1)

    with open(args.blockdev, 'rb+') as f:
        read_segments(f, segments_to_read, segment_size, backup)
    backup.write_manifest()

if __name__ == '__main__':
    sys.exit(main())
