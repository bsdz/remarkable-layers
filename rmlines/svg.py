import re
import math
from pathlib import Path

from lxml import etree as ET
import numpy as np
from numpy.linalg import multi_dot

from .constants import Pen, Colour, Width
from .rmobject.stroke import Stroke
from .rmobject.segment import Segment
from .rmobject.layer import Layer
from .rmobject.lines import RMLines

LOCAL_FONTS_DIR = Path(__file__).parents[1] / "fonts"


def apply_transform(transform, points):
    points = np.c_[points, np.ones(points.shape[0])].T
    return np.dot(transform, points).T[:, :-1]


def svg_path_d_to_points(d):
    points = []
    res = re.split("([MLZHV])", d)
    for com, args in zip(res[1::2], res[2::2]):
        args = args.replace(",", " ").strip()
        if com in ["M", "L"]:
            point = [float(f) for f in args.split(" ")]
        elif com == "H":
            point = [float(args), point[1]]
        elif com == "V":
            point = [point[0], float(args)]
        elif com == "Z":
            point = points[0]
        else:
            raise RuntimeError(f"Unsupported SVG path command: {com}{args}")
        points.append(point)
    return np.array(points)


def svg_path_to_strokes(
    path_d,
    pen=Pen.DEFAULT,
    colour=Colour.BLACK,
    width=Width.SMALL,
    segment_speed=100.0,
    segment_tilt=1 * math.pi - 0.5,
    segment_width=1.0,
    segment_pressure=1.0,
    transform=None,
):
    # split into separate strokes
    strokes = []
    move_frags = [d for d in re.split("([M][^M]*)", path_d) if d]

    for d in move_frags:
        points = svg_path_d_to_points(d)
        if transform is not None:
            points = apply_transform(transform, points)
        stroke = Stroke(pen, colour, width)
        for x, y in points:
            stroke.append(
                Segment(
                    x,
                    y,
                    speed=segment_speed,
                    tilt=segment_tilt,
                    width=segment_width,
                    pressure=segment_pressure,
                )
            )
        strokes.append(stroke)
    return strokes


def svg_to_rmlines(buffer):
    """Creates remarkable file from simple svg.

    The svg data cannot have groups or references
    and it must have all beziers converted into
    line segments.

    TODO: check above before processing.
    """
    p = ET.XMLParser(huge_tree=True)
    root = ET.fromstring(buffer.read(), parser=p)

    ins = RMLines()
    layer = Layer()
    for path in root.findall("path", root.nsmap):
        layer.extend(svg_path_to_strokes(path.attrib["d"]))
    ins.append(layer)
    return ins


class SVGStrokeFont:
    # encapsulate hershey text fonts
    # https://gitlab.com/oskay/svg-fonts
    def __init__(
        self, path=str((LOCAL_FONTS_DIR / "HersheySans1.svg"))
    ):
        tree = ET.parse(path)
        self.root = tree.getroot()
        font = self.root.find(".//font", self.root.nsmap)
        font_face = self.root.find(".//font-face", self.root.nsmap)
        self.default_horiz_adv_x = float(font.attrib["horiz-adv-x"])
        self.units_per_em = float(font_face.attrib["units-per-em"])

    def word_to_strokes(
        self,
        word,
        pos,
        height,
        pen=Pen.DEFAULT,
        colour=Colour.BLACK,
        width=Width.SMALL,
        segment_width=1.,
    ):
        strokes = []
        scale = height / self.units_per_em
        transforms = [
            np.array([[1.0, 0, pos[0]], [0, 1.0, pos[1]], [0, 0, 1.0]]),  # translate
            np.diag([1.0, -1.0, 1.0]),  # reflect in x-axis
            np.diag([scale, scale, 1.0]),  # scale
        ]
        transform = multi_dot(transforms)
        horiz_adv_x = 0.0
        for char in word:
            glyph = self.root.find(f".//glyph[@unicode='{char}']", self.root.nsmap)
            hadv = np.array([[1.0, 0, horiz_adv_x], [0, 1.0, 0.0], [0, 0, 1.0]])
            if "d" in glyph.attrib:
                char_transform = np.dot(
                    transform, hadv
                )  # advance (TODO: do this before char?)
                char_strokes = svg_path_to_strokes(
                    glyph.attrib["d"],
                    transform=char_transform,
                    pen=pen,
                    colour=colour,
                    width=width,
                    segment_width=segment_width,
                )
                strokes.extend(char_strokes)
            horiz_adv_x += float(glyph.attrib["horiz-adv-x"])
        return strokes
