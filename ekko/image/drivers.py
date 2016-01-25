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


@six.add_metaclass(abc.ABCMeta)
class BaseImage(object):
    """Base class for Image drivers

    :params image_location: Location of device or file to image
    """

    def __init__(self, image_location):
        self.image_location = image_location

    @abc.abstractmethod
    def get_data(self, reads):
        """Get data from backing device or file

        :params reads: A list of tuples with the start sector and size of read
        :returns: An interable of tuples with start sector and data
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_size(self):
        """Get size of disk to backup

        :returns: Size of disk in bytes
        """
        raise NotImplementedError()
