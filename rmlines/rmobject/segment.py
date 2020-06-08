import logging
from struct import pack, unpack, calcsize
import math

from ..constants import X_MAX, Y_MAX

logger = logging.getLogger(__name__)


class Segment:
    __slots__ = ("x", "y", "speed", "tilt", "width", "pressure")

    def __init__(self, x, y, speed=1.0, tilt=math.pi, width=10.0, pressure=1.0):
        assert 0.0 <= x <= X_MAX
        assert 0.0 <= y <= Y_MAX
        assert 0.0 <= tilt <= 2 * math.pi
        assert 0.0 <= pressure <= 1.0
        self.x, self.y = x, y
        self.speed, self.tilt, self.width, self.pressure = speed, tilt, width, pressure

    def __str__(self):
        return f"Segment: x={self.x:.2f}, y={self.y:.2f}, speed={self.speed:.2f}, tilt={self.tilt:.2f}, width={self.width:.2f}, pressure={self.pressure:.2f}"

    def dump(self):
        logger.debug(self)

    def to_bytes(self, buffer):
        buffer.write(
            pack(
                "ffffff",
                self.x,
                self.y,
                self.speed,
                self.tilt,
                self.width,
                self.pressure,
            )
        )

    @classmethod
    def from_bytes(cls, buffer):
        fmt = "ffffff"
        seg = cls(*unpack(fmt, buffer.read(calcsize(fmt))))
        return seg

    def to_svg(self, buffer):
        buffer.write(f"{self.x},{self.y} ")
