import logging
from struct import pack, unpack

logger = logging.getLogger(__name__)


class ByteableList:
    __slots__ = "objects"

    @classmethod
    def child_type(cls):
        raise NotImplementedError("Must specify child type for reading byte data")

    def __init__(self):
        self.objects = []

    def append(self, obj):
        self.objects.append(obj)

    def extend(self, objs):
        self.objects.extend(objs)

    def dump(self):
        logger.debug(self)
        for obj in self.objects:
            obj.dump()

    def to_bytes(self, buffer):
        buffer.write(pack("<I", len(self.objects)))
        for obj in self.objects:
            obj.to_bytes(buffer)

    @classmethod
    def from_bytes(cls, buffer):
        (n_objs,) = unpack("<I", buffer.read(4))
        ins = cls()
        ins.objects = [cls.child_type().from_bytes(buffer) for i in range(n_objs)]
        return ins

    def to_svg(self, buffer):
        for obj in self.objects:
            obj.to_svg(buffer)
