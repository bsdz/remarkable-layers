from itertools import count
from pathlib import Path
from io import BytesIO
from uuid import uuid4

from rmapy.api import Client
from rmapy.document import ZipDocument, RmPage


def upload_rm_doc(name, rms):

    empty_jpg = Path(__file__).parent / "empty.jpg"
    empty_jpg_bytes = empty_jpg.read_bytes()

    rmapy = Client()
    if not rmapy.is_auth():
        raise Exception("Not authenticated")
    rmapy.renew_token()

    rmps = []
    for rm in rms:

        layer_counter = count(1)

        buffer = BytesIO()
        rm.to_bytes(buffer)
        buffer.seek(0)

        uuid = str(uuid4())

        rmp = RmPage(
            buffer,
            metadata={
                "layers": [
                    {
                        "name": layer.name
                        if layer.name
                        else f"Layer {next(layer_counter)}"
                    }
                    for layer in rm.objects
                ]
            },
            thumbnail=BytesIO(empty_jpg_bytes),
            order=uuid,
        )

        rmps.append(rmp)

    zd = ZipDocument()
    zd.content["fileType"] = "notebook"
    zd.content["pages"] = [rmp.order for rmp in rmps]
    zd.content["pageCount"] = len(rmps)
    zd.metadata["VissibleName"] = name
    zd.pagedata = "\n".join(["Blank"] * len(rmps))
    zd.rm.extend(rmps)

    rmapy.upload(zd)
