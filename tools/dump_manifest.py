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
import binascii
import os
import sys

from stevedore import driver


def parse_args():
    parser = argparse.ArgumentParser(description='Backup Block Device')
    parser.add_argument('--manifest', required=True,
                        help='manifest file')
    parser.add_argument('--driver', required=False, default='sqlite',
                        choices=['osdk', 'sqlite'], help='manifest driver')
    return parser.parse_args()


def check_manifest(manifest_file):
    return os.path.isfile(manifest_file)


def main():
    args = parse_args()
    manifest = driver.DriverManager(
        namespace='ekko.manifest.drivers',
        name=args.driver,
        invoke_on_load=True,
        invoke_args=[args.manifest]
    ).driver

    for segment in manifest.get_segments(manifest.get_metadata()):
        print(binascii.b2a_hex(segment.segment_hash))

if __name__ == '__main__':
    sys.exit(main())
