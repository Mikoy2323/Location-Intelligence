import geopandas as gpd
from pathlib import Path
import src.plots as plots
import src.osm as osm
import src.preprocessing as preprocessing
import pandas as pd
import src.features as features


data_path = Path.cwd() / "DATA"
results_path = Path.cwd() / "RESULTS" / "PLOTS"


def krakow_pipeline():
    pass


def amsterdam_pipeline():
    """
        Processes various features related to bike paths in Amsterdam using H3 hexagons and merges them into a single DataFrame.

        This pipeline performs the following steps:
        1. Reads data containing bike paths in Amsterdam.
        2. Collects CRS (Coordinate Reference System) for the dataset.
        3. Creates boundary points and line for Amsterdam.
        4. Calculates the count of bike paths in each H3 area.
        5. Calculates the count of green areas in each H3 area.
        6. Merges the bike paths DataFrame with the green areas DataFrame.
        7. Calculates the count of buildings in each H3 area.
        8. Merges the bike paths DataFrame with the buildings DataFrame.
        9. Calculates the population count in each H3 area.
        10. Calculates the count of recreational areas (shops, schools, sport centers) in each H3 area.
        11. Merges the bike paths DataFrame with the recreational areas DataFrame.
        12. Calculates the distance from each H3 area to the city center.

        Parameters:
        None

        Returns:
        pd.DataFrame: A DataFrame containing the following columns:
            - h3_index: H3 hexagon index.
            - bike_paths_count: Count of bike paths in each H3 area.
            - green_areas_count: Count of green areas in each H3 area.
            - buildings_count: Count of buildings in each H3 area.
            - population_count: Population count in each H3 area.
            - recreational_areas_count: Count of recreational areas in each H3 area.
            - centrum_distance: Distance from the H3 area to the city center.
        """
    # read data containing bike paths in amsterdam
    amsterdam_bikes = gpd.read_parquet(data_path / "amsterdam_bike_paths_extended.parquet")

    # collect crs for this dataset
    crs = amsterdam_bikes.crs

    # create boundary points of Amsterdam for plots
    amsterdam_boundary_cords = osm.boundaries_download("Amsterdam")

    # create boundary line from points
    amsterdam_boundaries = preprocessing.boundary_from_points(amsterdam_boundary_cords, crs)

    # create feature containing count of bike paths in each h3 area
    h3_bike_paths_amsterdam = features.bike_paths_function(amsterdam_bikes, amsterdam_boundaries)

    # create feature containing count of green areas in each h3 area
    h3_green_areas = features.green_areas_function(amsterdam_boundaries, crs)

    # merge bike paths dataframe with green areas dataframe
    h3_bike_paths_amsterdam = pd.merge(h3_bike_paths_amsterdam,
                                       h3_green_areas[['h3_index', "green_areas_count"]],
                                       on='h3_index',
                                       how='left')

    # create feature containing count of buildings points in each h3 area
    h3_buildings = features.buildings_function(amsterdam_boundaries, crs)

    # merge bike paths dataframe with buildings dataframe
    h3_bike_paths_amsterdam = pd.merge(h3_bike_paths_amsterdam,
                                       h3_buildings[['h3_index', "buildings_count"]],
                                       on='h3_index',
                                       how='left')

    # create feature containing count of population in each h3 area
    h3_bike_paths_amsterdam = features.population_function(h3_bike_paths_amsterdam)

    # create feature containing count of recreational areas (shops, schools, sport centers) in each h3 area
    h3_recreational_areas = features.recreational_areas_function(amsterdam_boundaries, crs)

    # merge bike paths dataframe with buildings dataframe
    h3_bike_paths_amsterdam = pd.merge(h3_bike_paths_amsterdam,
                                       h3_recreational_areas[['h3_index', "recreational_areas_count"]],
                                       on='h3_index', how='left')

    # create feature containing distance from h3 area to city center
    h3_bike_paths_amsterdam = features.centrum_distance_function(h3_bike_paths_amsterdam)

    return h3_bike_paths_amsterdam


def main():
    amsterdam_dataset = amsterdam_pipeline()
    print(amsterdam_dataset)


if __name__ == "__main__":
    main()
