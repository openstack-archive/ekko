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


from binascii import b2a_hex
from binascii import crc32
from datetime import datetime
from struct import pack
from struct import unpack
from uuid import UUID


class osdk(object):

    def __init__(self, manifest):
        self.manifest = manifest
        self.segments = dict()
        self.metadata = dict()
        self.metadata['signature'] = \
            UUID('d326503ab5ca49adac56c89eb0b8ef08').bytes
        self.metadata['version'] = 0

    def write_manifest(self):
        with open(self.manifest, 'wb') as f:
            self.write_header(f)
            self.write_body(f)

    def build_header(self):
        timestamp = utctimestamp()
        padding = str.encode('\0\0' * 14)

        data = pack(
            '<i2IQH14s',
            timestamp,
            self.metadata['incremental'],
            self.metadata['segment_size'],
            self.metadata['sectors'],
            len(self.metadata['bases']),
            padding
        )

        checksum = crc32(data)

        for i in self.metadata['bases']:
            data += i
            checksum = crc32(i, checksum)

        return data, checksum

    def write_body(self, f):
        checksum = 0

        for segment, meta in self.segments.items():
            data = pack(
                '<2IH2B20s',
                segment,
                meta['incremental'],
                meta['base'],
                meta['encryption'],
                meta['compression'],
                meta['sha1_hash']
            )

            f.write(data)
            checksum = crc32(data, checksum)

        """ Backfill the body_checksum """
        f.seek(24, 0)
        f.write(pack('<I', checksum))

    def write_header(self, f):
        data, checksum = self.build_header()

        f.write(self.metadata['signature'])

        f.write(pack('<3I', self.metadata['version'], checksum, 0))
        f.write(data)

        f.write(self.metadata['signature'])

    def read_signature(self, f):
        if not self.metadata['signature'] == f.read(16):
            raise Exception('File signiture is not valid')

    def read_header(self, f):
        self.read_signature(f)

        data = f.read(12)
        if len(data) != 12:
            raise Exception('Failed to read amount of requested data')

        version, header_checksum, body_checksum = unpack('<3I', data)
        if self.metadata['version'] < version:
            raise Exception(
                'The manifest version is newer than I know how to read'
            )

        data = f.read(36)
        if len(data) != 36:
            raise Exception('Failed to read amount of requested data')

        checksum = crc32(data)

        num_of_bases = ""
        padding = ""

        self.metadata['timestamp'],
        self.metadata['incremental'],
        self.metadata['segment_size'],
        self.metadata['sectors'],
        num_of_bases,
        padding = unpack('<i2IQH14s', data)

        if padding:
            continue

        self.metadata['bases'] = []
        for i in range(0, num_of_bases):
            data = f.read(16)
            if len(data) != 16:
                raise Exception('Failed to read amount of requested data')
            self.metadata['bases'].append(data)
            checksum = crc32(data, checksum)

        if checksum != header_checksum:
            raise Exception('Header checksum does not match')

        self.read_signature(f)

        return body_checksum

    def read_body(self, f, body_checksum):
        checksum = 0

        data = f.read(32)
        while len(data) == 32:
            meta = dict()
            segment = ""

            segment,
            meta['incremental'],
            meta['base'],
            meta['encryption'],
            meta['compression'],
            sha1 = unpack('<2IH2B20s', data)

            meta['sha1_hash'] = b2a_hex(sha1)

            self.segments[segment] = meta
            checksum = crc32(data, checksum)
            data = f.read(32)

        if checksum != body_checksum:
            raise Exception('Body checksum does not match')

    def read_manifest(self, manifest=None):
        if manifest:
            with open(manifest, 'rb') as f:
                body_checksum = self.read_header(f)
                self.read_body(f, body_checksum)
        else:
            with open(self.manifest, 'rb') as f:
                body_checksum = self.read_header(f)
                self.read_body(f, body_checksum)


def utctimestamp():
    ts = datetime.utcnow() - datetime(1970, 1, 1)
    return ts.seconds + ts.days * 24 * 3600
