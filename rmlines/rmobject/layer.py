from .base import ByteableList
from .stroke import Stroke


class Layer(ByteableList):
    __slots__ = "name"

    @classmethod
    def child_type(cls):
        return Stroke

    def __init__(self, name=None):
        self.name = name
        super().__init__()

    def __str__(self):
        return f"Layer: nobjs={len(self.objects)}"
