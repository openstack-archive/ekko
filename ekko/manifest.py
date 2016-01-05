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
import os
import sqlite3
from struct import pack
from struct import unpack
from uuid import UUID
import time

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


class Manifest(object):

    def __init__(self, manifest):
        self.manifest = manifest
        self.metadata = {'version': 0}
        self.conn = sqlite3.connect(manifest)
        self.cur = self.conn.cursor()

    def write_manifest(self):
        print "START"
        start = time.time()
        self.write_header()
        print "{} HEADER WRITTEN".format(time.time() - start)
        self.write_body()
        self.conn.commit()
        self.conn.close()
        print "{} BODY WRITTEN".format(time.time() - start)
        print "FILE SIZE {}".format(os.path.getsize(self.manifest))

    def write_body(self):
        self.cur.execute(
            ("CREATE TABLE objects "
             "(block_id INTEGER PRIMARY KEY NOT NULL, "
             "backup_id INTEGER, "
             "base_id INTEGER, "
             "seg_hash BLOB, "
             "FOREIGN KEY(base_id) REFERENCES bases(id));")
        )
        self.cur.executemany("INSERT INTO objects (block_id, backup_id, base_id, seg_hash) VALUES (?, ?, ?, ?)", self.segments)
            # f.write(data)

        # Backfill the body_checksum
        # f.seek(24, 0)
        # f.write(pack('<i', checksum))

    def write_header(self):
        self.cur.execute("CREATE TABLE metadata (key text, value integer);")
        data = [
            ('timestamp', utctimestamp()),
            ('incremental', self.metadata['info'].incremental),
            ('segment_size', self.metadata['info'].segment_size),
            ('sectors', self.metadata['info'].sectors),
        ]
        for d in data:
            self.cur.execute(
                "INSERT INTO metadata VALUES ('{}', {})".format(*d))
        self.cur.execute(
            ("CREATE TABLE bases "
             "(id INTEGER PRIMARY KEY NOT NULL,"
             "base_uuid TEXT);")
        )
        self.bases = {}
        for base_id, base in enumerate(self.metadata['bases']):
            self.bases[base] = base_id
            self.cur.execute(
                "INSERT INTO bases VALUES ({}, '{}')".format(base_id, base))

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
            '<I2i', self.read_data(f, 12)
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
        self.segments = dict()
        self.hashes = dict()
        Segment = namedtuple(
            'Segment',
            'base incremental compression encryption'
        )

        try:
            while True:
                processing_segment = True

                segment, base = unpack('<IH', self.read_data(f, 6))

                self.segments[segment] = Segment(
                    self.metadata['bases'][base],
                    unpack('<I2B', self.read_data(f, 6))
                )

                self.hashes[segment] = unpack('<20s', self.read_data(f, 20))

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
