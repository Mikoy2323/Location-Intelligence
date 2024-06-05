import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import LineString
import h3
from shapely.geometry import Polygon
from collections import Counter


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


def get_h3_indices(geometry, resolution):
    """
    Generates a list of H3 indices covering the area represented by the input geometry.

    Parameters:
    - geometry (LineString): Geometry object representing a path.
    - resolution (int): H3 resolution level for indexing.

    Returns:
    - h3_indices (list): List of unique H3 indices covering the area.
    """
    h3_indices = set()
    for point in geometry.coords:
        h3_index = h3.geo_to_h3(point[1], point[0], resolution)  # lat, lng
        h3_indices.add(h3_index)
    return list(h3_indices)


def h3_to_polygon(h3_index):
    """
    Converts an H3 index to a polygon geometry.

    Parameters:
    - h3_index (str): H3 index representing a hexagonal cell.

    Returns:
    - polygon_geo_series (GeoSeries): GeoSeries containing a Polygon geometry representing the hexagonal cell.
    """
    boundary = h3.h3_to_geo_boundary(h3_index, geo_json=True)
    return gpd.GeoSeries([Polygon(boundary)])


def dataframe_to_h3_dataframe(df):
    """
    Converts a DataFrame with H3 indices into a GeoDataFrame containing aggregated H3 hexagons.

    Parameters:
    - df (DataFrame): DataFrame containing H3 indices in a column named 'h3_indices'.

    Returns:
    - h3_df (GeoDataFrame): GeoDataFrame containing aggregated H3 hexagons with counts and geometries.
    """
    all_h3_indices = [h3_index for indices in df['h3_indices'] for h3_index in indices]
    h3_counts = Counter(all_h3_indices)
    h3_df = gpd.GeoDataFrame({
        'h3_index': list(h3_counts.keys()),
        'count': list(h3_counts.values())
    })

    h3_df['geometry'] = h3_df['h3_index'].apply(lambda x: h3_to_polygon(x).iloc[0])
    h3_df.crs = df.crs
    return h3_df
