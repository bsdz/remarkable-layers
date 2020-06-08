from collections import namedtuple
from itertools import product

from rmlines.rmcloud import upload_rm_doc

from rmlines.constants import Pen, Width, Y_MAX
from rmlines import RMLines, Layer
from rmlines.svg import SVGStrokeFont

# TODO:
# loop through pens
#  * loop through width
#  * loop through speed
#  * loop through tilt

# pen_width_space = [float(x) for x in range(0, 100, 10)]
# pen_pressure_space = [x / 100. for x in range(0, 100, 5)]
# pen_tilt_space = [2 * math.pi * x / 100. for x in range(0, 100, 5)]

Pos = namedtuple("Pos", "x y")


def main():

    rm = RMLines()
    layer = Layer()

    svf = SVGStrokeFont()
    pos = Pos(100, 100)
    for pen, width in product(Pen, Width):
        if pen.value >= 12:
            strokes = svf.word_to_strokes(
                f"{pen}, {width}", pos, 40, pen=pen, width=width, segment_width=2.
            )
            layer.extend(strokes)
            pos = Pos(pos[0], pos[1] + 40)
            if pos[1] > Y_MAX:
                break

    rm.append(layer)

    upload_rm_doc("Pen Gallery", [rm])


if __name__ == "__main__":
    main()
