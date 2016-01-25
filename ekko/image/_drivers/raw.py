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

from ekko.image import drivers


class RawImage(drivers.BaseImage):

    def get_data(self, reads):
        with open(self.image_location, 'rb') as f:
            for start, size in reads:
                f.seek(start, 0)
                yield (start, f.read(size))

    def get_size(self):
        with open(self.image_location, 'rb') as f:
            f.seek(0, 2)
            return f.tell()
