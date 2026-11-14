"""Loaders of data"""

import pandas as pd
import geopandas as gpd

def load_ushcn_stations(**kwargs) -> gpd.GeoDataframe:
    """Loads the US Historical Climatology Network stations file as a Geopandas.GeoDataframe

    Arguments:
      **kwargs : keyword arguments for pandas.read_fwf
      
    Returns:
      Geopandas.GeoDataFrame containing station locations

    Notes:
      The station file is loaded from the NCEI HTTPS filestore
    """

    URL="https://www.ncei.noaa.gov/pub/data/ushcn/v2.5/ushcn-v2.5-stations.txt"

    FORMAT = {
        "colspecs": [(0,11),(12,20),(21,30),(32,37),(38,40),
                     (41,71),(72,78),(79,85),(86,92),(93,95)],
        "names": [
            "ushcn_id", 
            "latitude",
            "longitude",
            "elevation",
            "state",
            "name",
            "component_1",
            "component_2",
            "component_3",
            "utc_offset",
            ],
    }

    df = pd.read_fwf(
        URL, 
        colspecs=FORMAT["colspecs"],
        header=None, 
        names=FORMAT["names"],
        index_col="ushcn_id",
        usecols=["ushcn_id", "latitude", "longitude", "elevation", "state", "name"],
        )

    gdf = gpd.GeoDataFrame(
        df, 
        geometry=gpd.points_from_xy(df.longitude, df.latitude, crs="EPSG:4326"),
        )

    return gdf
    