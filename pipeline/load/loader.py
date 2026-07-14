from pathlib import Path
import pandas as pd


class Loader:
    def __init__(self, output_path: str ):
        self.output_path = Path(output_path)


    def save(self, df: pd.DataFrame) -> None:
        df.to_csv(self.output_path, index=False)