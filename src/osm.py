import requests
import rasterio
from rasterio.mask import mask
import numpy as np


def boundaries_download(place):
    """
       Downloads boundary coordinates for a specified place using the Nominatim API.

       Parameters:
       - place (str): The name of the place for which boundary coordinates are to be downloaded.

       Returns:
       - coords (list): List of coordinate tuples representing the boundary of the specified place.
         Returns None if no boundary data is found or if there's an error in fetching the data.
       """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    base_url = "https://nominatim.openstreetmap.org/search"

    place_name = place
    params = {"q": place_name,
              "format": "json",
              "polygon_geojson": 1}
    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        #print(data)
        if place == "Amsterdam centrum":
            coords = data[0]["geojson"]["coordinates"]
        else:
            coords = data[0]["geojson"]["coordinates"][0][0]
        return coords
    return None


def fetch_green_areas(boundary_coords):
    """
    Fetches green areas within the specified boundary using the Overpass API.

    Parameters:
    - boundary_coords (dpg.DataFrame): dataframe containing linestring with coordinates representing the boundary of the specified place.

    Returns:
    - green_areas (list): List of green areas with their coordinates.
      Returns None if no data is found or if there's an error in fetching the data.
    """
    coords = boundary_coords.loc[0, "geometry"].coords
    polygon_str = ' '.join(f"{lat} {lon}" for lon, lat in coords)

    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      way["leisure"="park"](poly:"{polygon_str}");
      way["leisure"="garden"](poly:"{polygon_str}");
      way["leisure"="recreation_ground"](poly:"{polygon_str}");
      way["landuse"="grass"](poly:"{polygon_str}");
      way["landuse"="forest"](poly:"{polygon_str}");
      way["natural"="wood"](poly:"{polygon_str}");
    );
    out body;
    >;
    out skel qt;
    """
    response = requests.post(overpass_url, data={"data": overpass_query})
    if response.status_code == 200:
        data = response.json()
        green_areas = []
        for element in data['elements']:
            if element["type"] == "node":
                coords = (element["lat"], element["lon"])
                green_areas.append(coords)
        return green_areas
    return None


def fetch_buildings(boundary_coords):
    """
    Fetches buildings within the specified boundary using the Overpass API.

    Parameters:
    - boundary_coords (gpd.GeoDataFrame): GeoDataFrame containing a single polygon with coordinates representing the boundary of the specified place.

    Returns:
    - buildings (list): List of buildings with their coordinates.
      Returns None if no data is found or if there's an error in fetching the data.
    """
    # Extract the coordinates of the polygon boundary
    coords = boundary_coords.loc[0, "geometry"].coords
    polygon_str = ' '.join(f"{lat} {lon}" for lon, lat in coords)

    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      way["building"](poly:"{polygon_str}");
      relation["building"](poly:"{polygon_str}");
    );
    out body;
    >;
    out skel qt;
    """

    response = requests.post(overpass_url, data={"data": overpass_query})
    if response.status_code == 200:
        data = response.json()
        buildings = []
        for element in data['elements']:
            if element["type"] == "node":
                coords = (element["lat"], element["lon"])
                buildings.append(coords)
        return buildings
    return None


def fetch_population_data_worldpop(boundary_coords, worldpop_tiff_path):
    """
    Fetches population data within the specified polygons using WorldPop raster data.

    Parameters:
    - worldpop_tiff_path (str): Path to the WorldPop raster TIFF file.
    - boundary_coords (GeoDataFrame): GeoDataFrame containing polygons representing areas of interest.

    Returns:
    - population (list): Population within each specified polygon.
    """
    population = [None] * len(boundary_coords)

    with rasterio.open(worldpop_tiff_path) as src:
        for i in range(len(boundary_coords)):
            boundary_geojson = [boundary_coords.loc[i, 'geometry'].__geo_interface__]
            out_image, out_transform = mask(src, boundary_geojson, crop=True, nodata=np.nan)
            population[i] = np.nansum(out_image)

    return population


def fetch_recreational_areas(boundary_coords):
    """
    Fetches recreational_ares within the specified boundary using the Overpass API.

    Parameters:
    - boundary_coords (gpd.GeoDataFrame): GeoDataFrame containing a single polygon with coordinates representing the boundary of the specified place.

    Returns:
    - amenities (list): List of amenities with their coordinates.
      Returns None if no data is found or if there's an error in fetching the data.
    """
    # Extract the coordinates of the polygon boundary
    coords = boundary_coords.loc[0, "geometry"].coords
    polygon_str = ' '.join(f"{lat} {lon}" for lon, lat in coords)

    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      way["leisure"="sports_centre"](poly:"{polygon_str}");
      node["leisure"="sports_centre"](poly:"{polygon_str}");
      way["shop"](poly:"{polygon_str}");
      node["shop"](poly:"{polygon_str}");
      way["amenity"="school"](poly:"{polygon_str}");
      node["amenity"="school"](poly:"{polygon_str}");
    );
    out body;
    >;
    out skel qt;
    """

    response = requests.post(overpass_url, data={"data": overpass_query})
    if response.status_code == 200:
        data = response.json()
        amenities = []
        for element in data['elements']:
            if element["type"] == "node":
                coords = (element["lat"], element["lon"])
                amenities.append(coords)
        return amenities
    return None
