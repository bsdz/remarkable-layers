from struct import pack, unpack, calcsize

from ..constants import Pen, Colour, Width
from .base import ByteableList
from .segment import Segment


class Stroke(ByteableList):
    __slots__ = ("pen", "colour", "width")

    @classmethod
    def child_type(cls):
        return Segment

    def __init__(
        self,
        pen: Pen = Pen.DEFAULT,
        colour: Colour = Colour.BLACK,
        width: Width = Width.MEDIUM,
    ):
        self.pen = pen
        self.colour = colour
        self.width = width
        super().__init__()

    def __str__(self):
        return f"Stroke: pen={self.pen.name}, colour={self.colour.name}, "
        f"width={self.width.name}, nobjs={len(self.objects)}"

    def to_bytes(self, buffer):
        buffer.write(
            pack("<IIIfI", self.pen.value, self.colour.value, 0, self.width.value, 0)
        )
        super().to_bytes(buffer)

    @classmethod
    def from_bytes(cls, buffer):
        fmt = "<IIIfI"
        pen, colour, _, width, _ = unpack(fmt, buffer.read(calcsize(fmt)))
        ins = super().from_bytes(buffer)
        ins.pen = Pen(pen)
        ins.colour = Colour(colour)
        ins.width = Width(width)
        return ins

    def to_svg(self, buffer):
        width = self.width.value
        if self.pen == Pen.RUBBER:
            width = width * 20
        elif self.pen != Pen.HIGHLIGHTER:
            width = 18 * width - 32

        buffer.write(
            f'<polyline fill="none" stroke="{self.colour.name.lower()}" '
            f'stroke-width="{width}" points="'
        )
        super().to_svg(buffer)
        buffer.write('"></polyline>')
