

class ObjectOrphanedException(Exception):
    pass


class RedisDriver(object):
    def __init__(self):
        pass

    def create_object(self, object_id):
        pass

    def add_reference(self, object_id):
        pass

    def remove_reference(self, object_id):
        # if after removal number of refs == 0
        raise ObjectOrphanedException(object_id)
