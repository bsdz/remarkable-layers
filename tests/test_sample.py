import unittest
from pathlib import Path
from io import BytesIO

from rmlines import RMLines

SAMPLES_DIR = Path(__file__).parents[1] / "samples"


class SampleTest(unittest.TestCase):
    def test_roundtrip(self):
        # logging.basicConfig(level="INFO")
        # logger.setLevel("DEBUG")
        for p in SAMPLES_DIR.glob("*.rm"):
            with self.subTest(p):
                if p.name == "8d75db7b-7716-4899-9ec5-1f89bcb88e10.rm":
                    # TODO: rubber pen
                    continue
                rm0 = RMLines.from_bytes(p.open("rb"))
                rm0.dump()

                buffer = BytesIO()
                rm0.to_bytes(buffer)
                self.assertEqual(buffer.getvalue(), p.read_bytes())
