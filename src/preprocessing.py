import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import LineString
import h3
from shapely.geometry import Polygon
from collections import Counter
from geopy.distance import geodesic


def geodataframe_from_points(points, crs):
    """
    Generates a GeoDataFrame from a list of (latitude, longitude) coordinate tuples.

    Parameters:
    - points (list of tuples): List of (latitude, longitude) coordinate tuples.
    - crs (str or dict): Coordinate reference system for the GeoDataFrame.

    Returns:
    - gdf (GeoDataFrame): GeoDataFrame containing the points and their geometries.
    """
    # Create Point geometries from latitude and longitude tuples
    geometry_points = [Point(lon, lat) for lat, lon in points]

    # Create a GeoDataFrame with the points
    gdf = gpd.GeoDataFrame(geometry=geometry_points)
    gdf.crs = crs  # Set the coordinate reference system

    return gdf


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


def dataframe_to_h3_dataframe(df, count_name):
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
        count_name: list(h3_counts.values())
    })

    h3_df['geometry'] = h3_df['h3_index'].apply(lambda x: h3_to_polygon(x).iloc[0])
    h3_df.crs = df.crs
    return h3_df


def get_distance_to_centrum(bikes_gdf, centrum_cords):
    """
        Calculates the distance from the centroid of each H3 hexagon area to the city center (centrum).

        This function performs the following steps:
        1. Calculates the centroid of each H3 hexagon area.
        2. Computes the distance from each centroid to the city center coordinates.
        3. Adds the calculated distances to the DataFrame.
        4. Removes the centroid column from the DataFrame.

        Parameters:
        - bikes_gdf (GeoDataFrame): GeoDataFrame containing H3 hexagon areas and their geometries.
        - centrum_cords (tuple): Tuple containing the coordinates of the city center (centrum) as (longitude, latitude).

        Returns:
        - bikes_gdf (GeoDataFrame): Updated GeoDataFrame with the distance to the city center added:
            - distance_to_centrum: Distance from the centroid of each H3 hexagon area to the city center.
        """
    # calculated centroid variable for each h3 area
    bikes_gdf["centroid"] = (
        bikes_gdf['geometry'].apply(lambda x: x.centroid))

    # calculating distance from centroid of each h3 area to
    bikes_gdf["distance_to_centrum"] = (
        bikes_gdf['centroid'].apply(lambda point: calculate_distance(
            (point.x, point.y), centrum_cords)))

    bikes_gdf.drop(columns=['centroid'], inplace=True)
    return bikes_gdf


def calculate_distance(coord1, coord2):
    """
        Calculates the geodesic distance between two geographical coordinates.

        This function uses the `geopy` library to calculate the geodesic distance
        (the shortest distance between two points on the surface of an ellipsoidal model of the Earth)
        between two sets of coordinates.

        Parameters:
        - coord1 (tuple): A tuple representing the first coordinate (longitude, latitude).
        - coord2 (tuple): A tuple representing the second coordinate (longitude, latitude).

        Returns:
        - distance (float): The distance between the two coordinates in meters.
        """
    return geodesic(coord1, coord2).meters