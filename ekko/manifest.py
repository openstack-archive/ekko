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

from binascii import crc32
from collections import namedtuple
from datetime import datetime
# from struct import pack
from struct import unpack
from uuid import UUID

import six

SIGNATURE = 'd326503ab5ca49adac56c89eb0b8ef08d326503ab5ca49adac56c89eb0b8ef08'


class EkkoShortReadError(Exception):

    def __init__(self, size_read, size_requested):
        self.size_read = size_read
        self.size_requested = size_requested


class EkkoManifestTooNewError(Exception):
    pass


class EkkoChecksumError(Exception):
    pass


class EkkoInvalidSignatureError(Exception):
    pass


class manifest(object):

    def __init__(self, manifest):
        self.manifest = manifest
        self.segments = dict()
        self.metadata = {'version': 0}

    def read_data(self, f, size_requested):
        data = f.read(size_requested)
        size_read = len(data)
        if size_read != size_requested:
            raise EkkoShortReadError(
                'Failed to read amount of requested data',
                size_read,
                size_requested
            )
        self.checksum = crc32(data)
        return data

    def read_signature(self, f):
        if not UUID(SIGNATURE).bytes == self.read_data(f, 32):
            raise EkkoInvalidSignatureError('File signiture is not valid')

    def read_header(self, f):
        self.checksum = 0
        Info = namedtuple(
            'Info',
            'timestamp incremental segment_size sectors'
        )

        self.read_signature(f)

        version, header_checksum, body_checksum = unpack(
            '<3I', self.read_data(f, 12)
        )

        if self.metadata['version'] < version:
            raise EkkoManifestTooNewError(
                'The manifest version is newer than I know how to read'
            )

        self.metadata['info'] = Info._make(
            unpack('<i2IQ', self.read_data(f, 20))
        )

        num_of_bases, _ = unpack('<H14s', self.read_data(f, 16))

        self.metadata['bases'] = [
            self.read_data(f, 16) for x in six.moves.range(0, num_of_bases)
        ]

        if self.checksum != header_checksum:
            raise EkkoChecksumError('Header checksum does not match')

        return body_checksum

    def read_body(self, f, body_checksum):
        self.checksum = 0
        Segment = namedtuple(
            'Segment',
            'base incremental compression encryption hash'
        )

        try:
            while True:
                processing_segment = True

                segment, base = unpack('<IH', self.read_data(f, 6))

                self.segments[segment] = Segment(
                    self.metadata['bases'][base],
                    unpack('<I2B20s', self.read_data(f, 26))
                )

                processing_segment = False
        except EkkoShortReadError as e:
            if processing_segment or e.size_of_read != 0:
                raise

        if self.checksum != body_checksum:
            raise EkkoChecksumError('Body checksum does not match')

    def read_manifest(self):
        with open(self.manifest, 'rb') as f:
            self.read_body(f, self.read_header(f))


def utctimestamp():
    ts = datetime.utcnow() - datetime(1970, 1, 1)
    return ts.seconds + ts.days * 24 * 3600
