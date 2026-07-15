from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import json
import pandas as pd
from itertools import batched


class EventLoader:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)

    def _read_zip(self, zip_file: ZipFile):
        for name in zip_file.namelist():
            if name.endswith(".zip"):
                inner_bytes = BytesIO(zip_file.read(name))
                with ZipFile(inner_bytes) as inner_zip:
                    inner_read = self._read_zip(inner_zip)
                    yield from inner_read
            elif name.endswith(".json"):
                with zip_file.open(name) as f:
                    yield (json.load(f))

    def read_json(self, batch_size: int = 100):  
        def events():  
            for archive in self.data_dir.glob("*.zip"):
                with ZipFile(archive) as zip_file:
                    yield from self._read_zip(zip_file)

        yield from batched(events(), batch_size) 

    # without batching
    # def read_json(self):
    #     for archive in self.data_dir.glob("*.zip"):
    #         with ZipFile(archive) as zip_file:
    #             outer_read = self._read_zip(zip_file)
    #             yield outer_read
