#!/usr/bin/python

# Copyright 2016 Intel corporation
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


import redis
from oslo_config import cfg


redis_opts = [
    cfg.StrOpt('redis_host',
               default='localhost',
               help='Host of redis database'),
    cfg.Opt('redis_port',
            default=6379,
            help='Port redis listens on'),
    cfg.Opt('redis_db',
            default=0,
            help='database number in redis')]


CONF = cfg.CONF
CONF.register_opts(redis_opts)


class ObjectOrphanedException(Exception):
    pass


class RedisDriver(object):
    def __init__(self):
        self.redis = redis.Redis(host=CONF.redis_host,
                                 port=CONF.redis_port,
                                 db=CONF.redis_db)

    def add_reference(self, object_id):
        self.redis.incr(object_id)

    def remove_reference(self, object_id):
        num_refs = self.redis.decr(object_id)
        if not num_refs:
            # if after removal number of refs == 0
            raise ObjectOrphanedException(object_id)
