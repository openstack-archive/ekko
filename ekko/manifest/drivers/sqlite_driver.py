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

import os
import sqlite3


class ManifestSQLite(object):

    def __init__(self, manifest_file):
        self.conn = sqlite3.connect(manifest_file)
        self.cur = self.conn.cursor()

    @staticmethod
    def create_manifest(self, backupset_id):
        empty_manifest = os.path.join("/dev/shm", "{}-0".format(backupset_id))
        conn = sqlite3.connect(empty_manifest)
        conn.execute(
            ("CREATE TABLE objects "
             "(block_id INTEGER PRIMARY KEY NOT NULL, "
             "backup_id INTEGER, "
             "base TEXT, "
             "encryption TEXT, "
             "compression TEXT, "
             "seg_hash TEXT);")
        )
        conn.execute(("CREATE TABLE metadata ("
                      "key text primary key, value text);"))
        conn.commit()
        conn.close()
        return empty_manifest

    def write_manifest(self, header, segments):
        self.write_header(header)
        self.write_body(segments)
        self.conn.commit()
        self.conn.close()

    def write_body(self, segments):
        self.cur.executemany(
            "INSERT OR REPLACE INTO objects VALUES (?, ?, ?, ?, ?, ?)",
            segments)

    def write_header(self, header):
        data = [
            ('timestamp', header['timestamp']),
            ('incremental', header['info'].incremental),
            ('segment_size', header['info'].segment_size),
            ('sectors', header['info'].sectors),
        ]
        for d in data:
            self.cur.execute(
                "INSERT OR UPDATE INTO metadata VALUES ('{}', {})".format(*d))
