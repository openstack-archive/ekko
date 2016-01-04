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
from six.moves import range


def parse_args():
    parser = argparse.ArgumentParser(description='Backup Block Device')
    parser.add_argument('--backupsize', required=True, type=int,
                        help='Size of backup for manifest gen (size in GB)')
    parser.add_argument('--manifest', required=True,
                        help='manifest file')
    parser.add_argument('--cbt', required=False,
                        help='change block tracking info')
    return parser.parse_args()


def read_segments(segments, size, backup):
    backup.segments = dict()
    backup.hashes = dict()
    Segment = namedtuple(
        'Segment',
        'base incremental compression encryption'
    )

    for segment in segments:
        # Generate manifest info for each object in backup
        backup.segments[segment] = Segment(
            len(backup.metadata['bases']) - 1,
            backup.metadata['info'].incremental,
            0,
            0
        )
        # Random string simulating hash sha
        backup.hashes[segment] = os.urandom(20)


def generate_mem_struct(segments, size, backup):
    b = {
        '96153320-980b-4b5e-958f-ea57812b280d': []
    }

    for seg in segments:
        b['96153320-980b-4b5e-958f-ea57812b280d'].append({
            seg: backup.metadata['info'].incremental
        })

    return b

def check_manifest(manifest_file):
    return os.path.isfile(manifest_file)


def main():
    args = parse_args()
    segment_size = 4 * 1024**2  # 4MiB
    size_of_disk = args.backupsize * 1024**3  # Convert GB to B
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

    #read_segments(range(0, num_of_segments - 1), segment_size, backup)
    t = generate_mem_struct(range(0, num_of_segments - 1), segment_size, backup)

    import pdb; pdb.set_trace()
    #backup.write_manifest()

if __name__ == '__main__':
    sys.exit(main())
