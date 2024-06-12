import geopandas as gpd
from pathlib import Path
import src.plots as plots
import src.osm as osm
import src.preprocessing as preprocessing
import pandas as pd
import src.features as features
from shapely.geometry import Polygon
import src.modelling as modelling

data_path = Path.cwd() / "DATA"
results_path = Path.cwd() / "RESULTS" / "PLOTS"
results_predictions_path = Path.cwd() / "RESULTS" / "PREDICTIONS_PLOTS"


def city_pipeline(city_name):
    """
        Processes various features related to bike paths in chosen city using H3 hexagons and merges them into a single DataFrame.

        This pipeline performs the following steps:
        1. Reads data containing bike paths in chosen_city.
        2. Collects CRS (Coordinate Reference System) for the dataset.
        3. Creates boundary points and line for chosen_city.
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
    # read data containing bike paths in chosen_city
    if city_name == "Amsterdam":
        city_bikes = gpd.read_parquet(data_path / "amsterdam_bike_paths_extended.parquet")
    else:
        city_bikes = gpd.read_parquet(data_path / "krakow_bike_paths_extended.parquet")

    # collect crs for this dataset
    crs = city_bikes.crs

    # create boundary points of chosen city for plots
    city_boundary_cords = osm.boundaries_download(city_name)

    # create boundary line from points
    city_boundaries = preprocessing.boundary_from_points(city_boundary_cords, crs)

    if city_name == "Amsterdam":
        city_bikes = city_bikes[city_bikes.within(Polygon(city_boundaries.loc[0, "geometry"]))]

    # create feature containing count of bike paths in each h3 area
    h3_bike_paths = features.bike_paths_function(city_bikes, city_boundaries, city_name)

    # create feature containing count of green areas in each h3 area
    h3_green_areas = features.green_areas_function(city_boundaries, crs, city_name)

    # merge bike paths dataframe with green areas dataframe
    h3_bike_paths= pd.merge(h3_bike_paths,
                                       h3_green_areas[['h3_index', "green_areas_count"]],
                                       on='h3_index',
                                       how='left')

    # create feature containing count of buildings points in each h3 area
    h3_buildings = features.buildings_function(city_boundaries, crs, city_name)

    # merge bike paths dataframe with buildings dataframe
    h3_bike_paths = pd.merge(h3_bike_paths,
                                       h3_buildings[['h3_index', "buildings_count"]],
                                       on='h3_index',
                                       how='left')

    # create feature containing count of population in each h3 area
    h3_bike_paths = features.population_function(h3_bike_paths, city_name)

    # create feature containing count of recreational areas (shops, schools, sport centers) in each h3 area
    h3_recreational_areas = features.recreational_areas_function(city_boundaries, crs, city_name)

    # merge bike paths dataframe with buildings dataframe
    h3_bike_paths = pd.merge(h3_bike_paths,
                                       h3_recreational_areas[['h3_index', "recreational_areas_count"]],
                                       on='h3_index', how='left')

    # create feature containing distance from h3 area to city center
    h3_bike_paths = features.centrum_distance_function(h3_bike_paths, city_name)

    return h3_bike_paths


def main():
    #amsterdam_dataset = city_pipeline("Amsterdam")
    #amsterdam_dataset.to_csv("Amsterdam.csv")

    krakow_dataset = city_pipeline("Kraków")
    krakow_dataset.to_csv("Krakow.csv")

    krakow_predictions_df = modelling.krakow_prediction(krakow_dataset)

    plots.results_h3_count_bike_path_plotter(krakow_predictions_df, results_predictions_path, "Kraków")
    plots.results_h3_difference_bike_path_plotter(krakow_predictions_df, results_predictions_path, "Kraków")


if __name__ == "__main__":
    main()
