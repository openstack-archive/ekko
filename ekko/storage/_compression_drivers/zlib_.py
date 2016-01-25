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

import zlib

from ekko.storage import compression_drivers


class ZlibCompression(compression_drivers.BaseCompression):

    @staticmethod
    def compress(data):
        return zlib.compress(data)

    @staticmethod
    def decompress(data):
        return zlib.decompress(data)
