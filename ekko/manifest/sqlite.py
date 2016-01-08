# Copyright 2016 Intel corporation
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

from contextlib import closing
from contextlib import contextmanager
import sqlite3

from ekko.manifest import driver


class SQLiteDriver(driver.ManifestDriver):

    def initialize(self):
        with self.get_conn() as conn:
            with closing(conn.cursor()) as cur:
                cur.executescript("""
                    CREATE TABLE metadata (
                        key TEXT PRIMARY KEY,
                        value TEXT
                    );
                    CREATE TABLE segments (
                        backupset_id BLOB,
                        incremental INTEGER,
                        segment INTEGER PRIMARY KEY,
                        compression TINYINT,
                        encryption TINYINT,
                        segment_hash BLOB
                    );
                """)
            conn.commit()

    @contextmanager
    def get_conn(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.manifest_file)

        conn = self.conn
        self.conn = None

        yield conn
        conn.rollback()
        self.conn = conn

    def put_segments(self, segments):
        with self.get_conn() as conn:
            with closing(conn.cursor()) as cur:
                cur.executemany(
                    "INSERT INTO segments VALUES (?, ?, ?, ?, ?, ?)",
                    segments
                )
            conn.commit()

    def put_metadata(self, metadata):
        with self.get_conn() as conn:
            with closing(conn.cursor()) as cur:
                cur.executemany(
                    "INSERT OR REPLACE INTO metadata VALUES (?, ?)",
                    [
                        ('incremental', metadata.incremental),
                        ('segment_size', metadata.segment_size),
                        ('sectors', metadata.sectors),
                        ('timestamp', metadata.timestamp)
                    ]
                )

            conn.commit()
