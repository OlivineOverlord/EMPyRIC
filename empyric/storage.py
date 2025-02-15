import h5py
import numpy as np
import pandas as pd

class HDF5Storage:
    """Handles geochemical data storage and querying using HDF5."""

    def __init__(self, filename="geochem_data.h5"):
        self.filename = filename

    def save_dataframe(self, df: pd.DataFrame, group: str, dataset: str):
        """Saves a Pandas DataFrame to an HDF5 file."""
        with h5py.File(self.filename, "a") as f:
            group = f.require_group(group)
            if dataset in group:
                del group[dataset]  # Overwrite if exists
            group.create_dataset(dataset, data=df.to_numpy(), compression="gzip")
            group.attrs["columns"] = list(df.columns)

    def load_dataframe(self, group: str, dataset: str) -> pd.DataFrame:
        """Loads a Pandas DataFrame from an HDF5 file."""
        with h5py.File(self.filename, "r") as f:
            data = f[group][dataset][()]
            columns = f[group].attrs["columns"]
        return pd.DataFrame(data, columns=columns)
    
    def query(self, group: str, dataset: str, condition):
        """Queries the dataset using a Pandas-like approach."""
        df = self.load_dataframe(group, dataset)
        return df.query(condition)