from struct import unpack, calcsize

from ..constants import HEADER_V5, X_MAX, Y_MAX
from .base import ByteableList
from .layer import Layer


class RMLines(ByteableList):
    __slots__ = "header"

    @classmethod
    def child_type(cls):
        return Layer

    def __init__(self, header=HEADER_V5):
        self.header = header
        super().__init__()

    def __str__(self):
        return f'RMLines: header="{self.header.decode("ascii").strip()}", nobjs={len(self.objects)}'

    def to_bytes(self, buffer):
        buffer.write(self.header)
        super().to_bytes(buffer)

    @classmethod
    def from_bytes(cls, buffer):
        fmt = "<43s"
        (header,) = unpack(fmt, buffer.read(calcsize(fmt)))
        ins = super().from_bytes(buffer)
        ins.header = header
        return ins

    def to_svg(self, buffer):
        buffer.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" height="{Y_MAX}" width="{X_MAX}" '
            'style="background-color:lightblue">'
        )
        super().to_svg(buffer)
        buffer.write("</svg>")

    @classmethod
    def from_svg(cls, buffer):
        from ..svg import svg_to_rmlines
        return svg_to_rmlines(buffer)
