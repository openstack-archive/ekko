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


from datetime import datetime
from osdk import osdk
from uuid import UUID


def get_timestamp(o):
    return datetime.fromtimestamp(
        o.metadata['timestamp']).strftime('%Y-%m-%d %H:%M:%S')


def convert_size(size_in_bytes):
    sizes = {4: " TiB", 3: " GiB", 2: " MiB", 1: "KiB", 0: "B"}

    for i in range(len(sizes), 1, -1):
        size = int(size_in_bytes / 1024**i)
        if size > 0:
            break

    return str(size) + sizes[i]


def print_header(o):
    formated_out = """Version:\t%(version)s
Creation Date:\t%(timestamp)s
Incremental:\t%(incremental)s
Volume Size:\t%(volume_size)s
Segment Size:\t%(segment_size)s
Backup Set:\t%(backup_set)s"""

    dict_out = dict()
    dict_out['backup_set'] = UUID(bytes=o.metadata['bases'][-1])
    dict_out['version'] = o.metadata['version']
    dict_out['incremental'] = o.metadata['incremental']
    dict_out['timestamp'] = get_timestamp(o)
    dict_out['volume_size'] = convert_size(o.metadata['sectors'] * 512)
    dict_out['segment_size'] = convert_size(o.metadata['segment_size'])

    print(formated_out % dict_out)


def main():
    manifest = 'manifest1.osdk'
    o = osdk(manifest)
    o.read_manifest()

    print_header(o)

if __name__ == '__main__':
    main()
