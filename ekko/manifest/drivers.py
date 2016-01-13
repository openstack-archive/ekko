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

import abc

from oslo_utils import importutils
import six


@six.add_metaclass(abc.ABCMeta)
class BaseManifest(object):
    """Base class for Manifest drivers

    :params manifest_file: File location for manifest
    """

    def __init__(self, manifest_file):
        self.conn = None
        self.manifest_file = manifest_file

    @abc.abstractmethod
    def get_metadata(self):
        """Get segments from manifest

        :returns: An object of class manifest.structure.Metadata
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_segments(self):
        """Get segments from manifest

        :returns: A generator of with objects of class
          manifest.structure.Segment
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def put_metadata(self, metadata):
        """Puts given metadata into manifest

        :params metadata: An object of class manifest.structure.Metadata
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def put_segments(self, segments, metadata):
        """Puts given segment information into manifest

        :params segments: An interable with objects of class
          manifest.structure.Segment
        :params metadata: An object of class manifest.structure.Metadata
        """
        raise NotImplementedError()
