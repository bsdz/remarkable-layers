from pathlib import Path

from rmlines.rmcloud import upload_rm_doc
from rmlines import RMLines

SAMPLES_DIR = Path(__file__).parents[1] / "samples"


def main():

    rms = []
    for p in SAMPLES_DIR.glob("*.rm"):
        rm = RMLines.from_bytes(p.open("rb"))
        for i, layer in enumerate(rm.objects):
            layer.name = f"Layer {i+1}"
        rms.append(rm)

    upload_rm_doc("Samples", rms)


if __name__ == "__main__":
    main()
