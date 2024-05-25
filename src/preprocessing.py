import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import LineString


def boundary_from_points(points, crs):
    """
    Generates a boundary line from a list of points and saves it in a GeoDataFrame.

    Parameters:
    - points (list of tuples): List of (x, y) coordinate tuples.
    - crs (CRS): Coordinate reference system for the boundary.

    Returns:
    - boundaries_gdf (GeoDataFrame): GeoDataFrame containing the boundary line.
    """

    geometry_points = [Point(x, y) for x, y in points]
    geometry_bounds = LineString(geometry_points)
    boundaries_gdf = gpd.GeoDataFrame([geometry_bounds], columns=['geometry'])
    boundaries_gdf.crs = crs
    return boundaries_gdf
