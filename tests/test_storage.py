import pytest
import pandas as pd
from empyric.storage import HDF5Storage

def test_hdf5_storage():
    storage = HDF5Storage("test.h5")

    df = pd.DataFrame({"SiO2": [50, 55], "MgO": [4, 6]})
    storage.save_dataframe(df, "geochem", "samples")

    loaded_df = storage.load_dataframe("geochem", "samples")
    assert loaded_df.equals(df)