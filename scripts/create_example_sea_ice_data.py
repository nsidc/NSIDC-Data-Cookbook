'''Creates two example sea ice data netcdf files.

These are used in how-to-add-coordinates-to-xarray.ipynb and
how-to-add-crs-to-xarray.ipynb.
'''

from pathlib import Path

import xarray as xr

EXAMPLE_DATA_PATH = Path("./example_data")
EXAMPLE_FILE_PATH = EXAMPLE_DATA_PATH / "NSIDC0081_SEAICE_PS_N25km_20230627_v2.0.nc"

def create_example_with_no_coordinates():
    '''Create sea ice concentration file with no coordinates'''
    ds = xr.open_dataset(
        EXAMPLE_FILE_PATH, 
        drop_variables=[
            "time","x","y","crs", "F16_ICECON","F17_ICECON"
        ]
    )
    ds.to_netcdf(EXAMPLE_DATA_PATH / EXAMPLE_FILE_PATH.name.replace(".nc", ".no_coords.nc"))


def create_example_with_no_crs():
    '''Create sea ice concentration file with no coordinates'''
    ds = xr.open_dataset(
        EXAMPLE_FILE_PATH, 
        drop_variables=[
            "crs", "F16_ICECON","F17_ICECON"
        ]
    )
    ds.to_netcdf(EXAMPLE_DATA_PATH / EXAMPLE_FILE_PATH.name.replace(".nc", ".no_crs.nc"))


if __name__ == "__main__":
    create_example_with_no_coordinates()
    create_example_with_no_crs()
