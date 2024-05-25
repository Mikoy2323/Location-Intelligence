import geopandas as gpd
from pathlib import Path
import src.plots as plots
import src.osm as osm
import src.preprocessing as preprocessing
import sys

if __name__ == "__main__":
    data_path = Path.cwd() / "DATA"
    results_path = Path.cwd() / "RESULTS" / "PLOTS"

    amsterdam_bikes = gpd.read_parquet(data_path / "amsterdam_bike_paths_extended.parquet")

    # create boundary points of Amsterdam for plots
    amsterdam_boundary_cords = osm.boundaries_download("Amsterdam")
    if amsterdam_boundary_cords is None:
        sys.exit()

    # create boundary line from points
    amsterdam_boundaries = preprocessing.boundary_from_points(amsterdam_boundary_cords, amsterdam_bikes.crs)

    # plot bike paths and city boundaries in amsterdam
    plots.paths_plotter(amsterdam_bikes, amsterdam_boundaries, results_path)
