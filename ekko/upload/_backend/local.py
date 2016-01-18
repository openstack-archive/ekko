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
# limitations under the License

from distutils.dir_util import mkpath
import os
import uuid

from ekko.upload import backend


class LocalUpload(backend.BaseUpload):

    def put_data(self, data_segment):
        data = data_segment[0]
        segment = data_segment[1]
        file_path = os.path.join(
            self.upload_location,
            str(uuid.UUID(bytes=segment.backupset_id)),
            str(segment.incremental)
        )

        mkpath(file_path)

        file_output = os.path.join(
            file_path,
            str(segment.segment)
        )

        with open(file_output, 'wb') as f:
            f.write(data)

        return segment
