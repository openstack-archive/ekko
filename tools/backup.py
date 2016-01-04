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


from hashlib import sha1
from osdk import osdk
from uuid import uuid4 as uuid


def get_disk_size(device):
    with open(device, 'rb') as f:
        return f.seek(0, 2)


def read_segments(f, lst, size, o):
    zero_hash = sha1(bytes([0] * size)).hexdigest()

    for segment in lst:
        f.seek(segment * size, 0)
        data = f.read(size)
        if not data:
            raise Exception('Failed to read data')

        sha1_hash = sha1(data)
        if sha1_hash.hexdigest() != zero_hash:
            meta = dict()
            meta['incremental'] = o.metadata['incremental']
            meta['base'] = len(o.metadata['bases']) - 1
            meta['encryption'] = 0
            meta['compression'] = 0
            meta['sha1_hash'] = sha1_hash.digest()
            o.segments[segment] = meta
        else:
            try:
                del o.segments[segment]
            except KeyError:
                pass


def main():
    device = '/dev/loop0'
    old_manifest = 'manifest0.osdk'
    manifest = 'manifest0.osdk'
    manifest = 'manifest1.osdk'
    segment_size = 4 * 1024**2  # 4MiB
    size_of_disk = get_disk_size(device)
    num_of_sectors = int(size_of_disk / 512)
    num_of_segments = int(size_of_disk / segment_size)

    o = osdk(manifest)
    o.metadata['sectors'] = num_of_sectors

    new = True
    new = False
    existing = True
    existing_full = True
    existing_full = False

    if new:
        o.metadata['incremental'] = 0
        o.metadata['segment_size'] = segment_size
        o.metadata['bases'] = [uuid().bytes]
        segments_to_read = range(0, num_of_segments - 1)
    elif existing:
        o.read_manifest(old_manifest)
        o.metadata['incremental'] += 1
        segments_to_read = range(1, num_of_segments - 1)
    elif existing_full:
        o.read_manifest(old_manifest)
        o.metadata['incremental'] += 1
        segments_to_read = range(0, num_of_segments - 1)

    with open(device, 'rb+') as f:
        read_segments(f, segments_to_read, segment_size, o)

    o.write_manifest()

if __name__ == '__main__':
    main()
