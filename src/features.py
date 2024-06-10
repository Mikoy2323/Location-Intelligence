import src.plots as plots
from pathlib import Path
import src.preprocessing as preprocessing
import src.osm as osm

data_path = Path.cwd() / "DATA"
results_path = Path.cwd() / "RESULTS" / "PLOTS"

# resolution for h3 function to ensure, that all h3 indexes are created the same
h3_resolution = 7


def bike_paths_function(amsterdam_bikes, amsterdam_boundaries):
    """
        Processes bike path data to create a DataFrame of H3 hexagon areas with the count of bike paths in Amsterdam.

        This function performs the following steps:
        1. Plots bike paths and city boundaries in Amsterdam.
        2. Creates H3 indices for the bike path geometries.
        3. Aggregates the data to create a new DataFrame with the count of bike paths for each H3 hexagon.
        4. Plots the number of bike paths in each H3 area.

        Parameters:
        - amsterdam_bikes (gpd.GeoDataFrame): GeoDataFrame containing the bike path geometries in Amsterdam.
        - amsterdam_boundaries (gpd.GeoDataFrame): GeoDataFrame containing the boundary of Amsterdam.

        Returns:
        - h3_amsterdam_bikes (pd.DataFrame): A DataFrame containing the following columns:
            - h3_index: H3 hexagon index.
            - bike_paths_count: Count of bike paths within each H3 area.
            - geometry: Polygon geometry of each H3 hexagon.
        """

    # plot bike paths and city boundaries in amsterdam
    plots.paths_plotter(amsterdam_bikes, amsterdam_boundaries, results_path, "Amsterdam")

    # creating h3_indices for dataframe
    amsterdam_bikes['h3_indices'] = (
        amsterdam_bikes['geometry'].apply(lambda x: preprocessing.get_h3_indices(x, h3_resolution)))

    # creating new dataframe with number of bike paths as 'count' parameter and new geometry as h3 polygon
    h3_amsterdam_bikes = preprocessing.dataframe_to_h3_dataframe(amsterdam_bikes, "bike_paths_count")

    # plotting number of bike paths in each h3 area
    plots.h3_count_bike_path_plotter(amsterdam_bikes, h3_amsterdam_bikes, results_path, "Amsterdam")

    return h3_amsterdam_bikes


def green_areas_function(amsterdam_boundaries, crs):
    """
        Processes green area data to create a DataFrame of H3 hexagon areas with the count of green areas in Amsterdam.

        This function performs the following steps:
        1. Fetches the coordinates of green areas within the specified city boundaries.
        2. Creates a GeoDataFrame from the green area coordinates.
        3. Plots the green areas and city boundaries.
        4. Creates H3 indices for the green area geometries.
        5. Aggregates the data to create a new DataFrame with the count of green areas for each H3 hexagon.
        6. Plots the number of green areas in each H3 area.

        Parameters:
        - amsterdam_boundaries (gpd.GeoDataFrame): GeoDataFrame containing the boundary of Amsterdam.
        - crs (str): Coordinate reference system for the GeoDataFrame.

        Returns:
        - h3_green_areas (pd.DataFrame): A DataFrame containing the following columns:
            - h3_index: H3 hexagon index.
            - green_areas_count: Count of green areas within each H3 area.
            - geometry: Polygon geometry of each H3 hexagon.
        """
    # fetching number of green_area points inside city_boundaries
    green_areas_coords = osm.fetch_green_areas(amsterdam_boundaries)

    # creating geodataframe from green_area_coords variable
    green_areas_dataframe = preprocessing.geodataframe_from_points(green_areas_coords, crs)

    # plotting points of green areas in city
    plots.green_areas_plotter(green_areas_dataframe, amsterdam_boundaries, results_path, "Amsterdam")

    # creating h3_indices for green_areas_dataframe
    green_areas_dataframe['h3_indices'] = (
        green_areas_dataframe['geometry'].apply(lambda x: preprocessing.get_h3_indices(x, h3_resolution)))

    # creating new dataframe with number of green area points as 'count' parameter and new geometry as h3 polygon
    h3_green_areas = preprocessing.dataframe_to_h3_dataframe(green_areas_dataframe, "green_areas_count")

    # plotting number of green area points in each h3 area
    plots.h3_count_green_areas_plotter(green_areas_dataframe, h3_green_areas, results_path, "Amsterdam")

    return h3_green_areas


def buildings_function(amsterdam_boundaries, crs):
    """
        Processes building data to create a DataFrame of H3 hexagon areas with the count of buildings in Amsterdam.

        This function performs the following steps:
        1. Fetches the coordinates of buildings within the specified city boundaries.
        2. Creates a GeoDataFrame from the building coordinates.
        3. Plots the building points and city boundaries.
        4. Creates H3 indices for the building geometries.
        5. Aggregates the data to create a new DataFrame with the count of buildings for each H3 hexagon.
        6. Plots the number of buildings in each H3 area.

        Parameters:
        - amsterdam_boundaries (gpd.GeoDataFrame): GeoDataFrame containing the boundary of Amsterdam.
        - crs (str): Coordinate reference system for the GeoDataFrame.

        Returns:
        - h3_buildings (pd.DataFrame): A DataFrame containing the following columns:
            - h3_index: H3 hexagon index.
            - buildings_count: Count of buildings within each H3 area.
            - geometry: Polygon geometry of each H3 hexagon.
        """
    # fetching number of building points in area
    buildings_coords = osm.fetch_buildings(amsterdam_boundaries)

    # creating geodataframe from buildings_coords variable
    buildings_dataframe = preprocessing.geodataframe_from_points(buildings_coords, crs)

    # plotting points of green areas in city
    plots.buildings_plotter(buildings_dataframe, amsterdam_boundaries, results_path, "Amsterdam")

    # creating h3_indices for green_areas_dataframe
    buildings_dataframe['h3_indices'] = (
        buildings_dataframe['geometry'].apply(lambda x: preprocessing.get_h3_indices(x, h3_resolution)))

    # creating new dataframe with number of building points as 'count' parameter and new geometry as h3 polygon
    h3_buildings = preprocessing.dataframe_to_h3_dataframe(buildings_dataframe, "buildings_count")

    # plotting number of buildings points in each h3 area
    plots.h3_count_buildings_plotter(buildings_dataframe, h3_buildings, results_path, "Amsterdam")

    return h3_buildings


def population_function(h3_amsterdam_bikes):
    """
        Adds population data to the H3 hexagon areas DataFrame and plots the population distribution.

        This function performs the following steps:
        1. Fetches the population data for each H3 hexagon area using WorldPop data.
        2. Adds the population data to the DataFrame.
        3. Plots the population distribution for the H3 hexagon areas.

        Parameters:
        - h3_amsterdam_bikes (pd.DataFrame): DataFrame containing H3 hexagon areas with bike path data.

        Returns:
        - h3_amsterdam_bikes (pd.DataFrame): Updated DataFrame with an additional column for population:
            - h3_index: H3 hexagon index.
            - bike_paths_count: Count of bike paths within each H3 area.
            - green_areas_count: Count of green areas within each H3 area.
            - buildings_count: Count of buildings within each H3 area.
            - population: Population within each H3 area.
            - geometry: Polygon geometry of each H3 hexagon.
        """
    # fetches population data from worldpop api
    populations = osm.fetch_population_data_worldpop(h3_amsterdam_bikes, data_path / "amsterdam_population.tif")

    # add population variable to dataset
    h3_amsterdam_bikes["population"] = populations

    plots.h3_count_population_plotter(h3_amsterdam_bikes, results_path, "Amsterdam")

    return h3_amsterdam_bikes


def recreational_areas_function(amsterdam_boundaries, crs):
    """
        Adds recreational areas data to the H3 hexagon areas DataFrame and plots the recreational areas distribution.

        This function performs the following steps:
        1. Fetches the recreational areas (e.g., parks, sports centers, schools, malls) within the city boundaries.
        2. Creates a GeoDataFrame from the fetched recreational areas coordinates.
        3. Plots the recreational areas within the city boundaries.
        4. Calculates H3 indices for the recreational areas and aggregates them.
        5. Plots the number of recreational areas within each H3 hexagon.
        6. Returns a DataFrame with H3 hexagon areas and the count of recreational areas within each H3 area.

        Parameters:
        - amsterdam_boundaries (gpd.GeoDataFrame): GeoDataFrame containing the boundaries of Amsterdam.
        - crs (str): Coordinate reference system for the GeoDataFrame.

        Returns:
        - h3_recreational_areas (pd.DataFrame): DataFrame containing the count of recreational areas within each H3 area:
            - h3_index: H3 hexagon index.
            - recreational_areas_count: Count of recreational areas within each H3 area.
            - geometry: Polygon geometry of each H3 hexagon.
        """
    # fetching number of recreational points in area
    recreational_areas_coords = osm.fetch_recreational_areas(amsterdam_boundaries)

    # creating geodataframe from recreational_areas_coords variable
    recreational_areas_dataframe = preprocessing.geodataframe_from_points(recreational_areas_coords, crs)

    # plotting points of recreational areas in city
    plots.recreational_areas_plotter(recreational_areas_dataframe, amsterdam_boundaries, results_path, "Amsterdam")

    # creating h3_indices for green_areas_dataframe
    recreational_areas_dataframe['h3_indices'] = (
        recreational_areas_dataframe['geometry'].apply(lambda x: preprocessing.get_h3_indices(x, h3_resolution)))

    # creating new dataframe with number of green area points as 'count' parameter and new geometry as h3 polygon
    h3_recreational_areas = preprocessing.dataframe_to_h3_dataframe(recreational_areas_dataframe,
                                                                    "recreational_areas_count")

    # plotting number of green area points in each h3 area
    plots.h3_count_recreational_areas_plotter(recreational_areas_dataframe, h3_recreational_areas, results_path,
                                              "Amsterdam")

    return h3_recreational_areas


def centrum_distance_function(h3_amsterdam_bikes):
    """
        Adds distance to the city center (centrum) for each H3 hexagon area in Amsterdam.

        This function performs the following steps:
        1. Fetches the coordinates of the Amsterdam city center (centrum).
        2. Calculates the distance from each H3 hexagon area to the city center.
        3. Plots the distances to the city center for visualization.
        4. Returns the updated DataFrame with the distance to the city center added.

        Parameters:
        - h3_amsterdam_bikes (pd.DataFrame): DataFrame containing H3 hexagon areas in Amsterdam and associated data.

        Returns:
        - h3_amsterdam_bikes (pd.DataFrame): Updated DataFrame with the distance to the city center added:
            - h3_index: H3 hexagon index.
            - distance_to_centrum: Distance from the H3 hexagon to the city center.
            - other columns from the original DataFrame.
        """
    # fetching coordinates of amsterdam centrum point
    central_cords = osm.boundaries_download("Amsterdam centrum")

    # get distance from each h3 area to centrum
    h3_amsterdam_bikes = preprocessing.get_distance_to_centrum(h3_amsterdam_bikes, central_cords)

    plots.distance_to_centrum_plotter(h3_amsterdam_bikes, central_cords, results_path, "Amsterdam")

    return h3_amsterdam_bikes
