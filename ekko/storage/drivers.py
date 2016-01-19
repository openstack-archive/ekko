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

import abc

import six
from stevedore import driver


@six.add_metaclass(abc.ABCMeta)
class BaseStorage(object):
    """Base class for storage drivers

    :params storage_location: Location to store data
    """

    def __init__(self, storage_location):
        self.storage_location = storage_location

     @abc.abstractmethod
    def put_data(self, data_segment):
        """Write data to backing location

        :params data_segment: A tuple with a raw chunk of data to write out and
            An object of type manifest.structure.Segment with the metadata
            to pair with the raw chunk of data
        :returns: A generator with the segment objects
        """
        raise NotImplementedError()

    @staticmethod
    def unwrap_data(data, segment):
        # NOTE(SamYaple): Unimplemented selection of compression/encryption
        compression = driver.DriverManager(
            namespace='ekko.storage.compression_drivers',
            name='zlib',
            invoke_on_load=True
        ).driver

        encryption = driver.DriverManager(
            namespace='ekko.storage.encryption_drivers',
            name='noop',
            invoke_on_load=True
        ).driver

        return encryption.decrypt(compression.uncompress(data))

    @staticmethod
    def wrap_data(data, segment):
        # NOTE(SamYaple): Unimplemented selection of compression/encryption
        compression = driver.DriverManager(
            namespace='ekko.storage.compression_drivers',
            name='zlib',
            invoke_on_load=True
        ).driver

        encryption = driver.DriverManager(
            namespace='ekko.storage.encryption_drivers',
            name='noop',
            invoke_on_load=True
        ).driver

        return encryption.encrypt(compression.compress(data))
