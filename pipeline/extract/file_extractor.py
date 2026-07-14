from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import json
import pandas as pd


class EventLoader:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)

    def _read_zip(self, zip_file: ZipFile, events: list):

        for name in zip_file.namelist():

            if name.endswith(".zip"):

                inner_bytes = BytesIO(zip_file.read(name))

                with ZipFile(inner_bytes) as inner_zip:
                    self._read_zip(inner_zip, events)

            elif name.endswith(".json"):

                with zip_file.open(name) as f:
                    events.extend(json.load(f))

    def load(self) -> pd.DataFrame:
        events = []
        for archive in self.data_dir.glob("*.zip"):
            with ZipFile(archive) as zip_file:
                self._read_zip(zip_file, events)
        return pd.DataFrame(events)
    

# loader = EventLoader("data")
# df = loader.load()

# print (df.head())
# print (df.shape)