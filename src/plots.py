import matplotlib.pyplot as plt


def paths_plotter(bike_paths_gdf, city_bounds_gdf, results_path, city_name):
    """
      Plots bike paths over city boundaries and saves the plot as an image.

      Parameters:
      - bike_paths_gdf (GeoDataFrame): GeoDataFrame containing bike paths.
      - city_bounds_gdf (GeoDataFrame): GeoDataFrame containing city boundaries.
      - results_path (str or Path): Path where the resulting plot image will be saved.
      - city_name (str): Name of the city for which the plot is generated.
      """

    fig, ax = plt.subplots(figsize=(12, 10))
    fig.suptitle(f"{city_name} bike paths", fontsize=25)
    bike_paths_gdf.plot(ax=ax)
    city_bounds_gdf.plot(ax=ax, color="black")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    fig.savefig(results_path / f"{city_name}_bike_paths.png")


def h3_count_bike_path_plotter(bike_path_gdf, h3_df, results_path, city_name):
    """
    Plots bike path count by H3 area and saves the plot as an image.

    Parameters:
    - bike_path_gdf (GeoDataFrame): GeoDataFrame containing bike path geometries.
    - h3_df (GeoDataFrame): GeoDataFrame containing aggregated H3 hexagons with counts and geometries.
    - results_path (str): Path to the directory where the plot image will be saved.
    - city_name (str): Name of the city for which the plot is generated.

    Returns:
    - None
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.suptitle(f"{city_name} bike paths count by h3 area", fontsize=20)
    bike_path_gdf.plot(ax=ax, linewidth=0.5)
    h3_df.plot(column="bike_paths_count", cmap='OrRd', legend=True, ax=ax)

    fig.savefig(results_path / f"{city_name}_h3_bike_paths.png")


def h3_count_green_areas_plotter(green_area_gdf, h3_df, results_path, city_name):
    """
    Plots green areas points count by H3 area and saves the plot as an image.

    Parameters:
    - green_area_gdf (GeoDataFrame): GeoDataFrame containing green areas geometries.
    - h3_df (GeoDataFrame): GeoDataFrame containing aggregated H3 hexagons with counts and geometries.
    - results_path (str): Path to the directory where the plot image will be saved.
    - city_name (str): Name of the city for which the plot is generated.

    Returns:
    - None
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.suptitle(f"{city_name} green areas points count by h3 area", fontsize=20)
    h3_df.plot(column="green_areas_count", cmap='Blues',  legend=True, ax=ax)
    green_area_gdf.plot(ax=ax, markersize=0.05, alpha=0.1, color="green")

    fig.savefig(results_path / f"{city_name}_h3_green_areas.png")


def h3_count_buildings_plotter(buildings_gdf, h3_df, results_path, city_name):
    """
    Plots building points count by H3 area and saves the plot as an image.

    Parameters:
    - buildings_gdf (GeoDataFrame): GeoDataFrame containing buildings geometries.
    - h3_df (GeoDataFrame): GeoDataFrame containing aggregated H3 hexagons with counts and geometries.
    - results_path (str): Path to the directory where the plot image will be saved.
    - city_name (str): Name of the city for which the plot is generated.

    Returns:
    - None
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.suptitle(f"{city_name} buildings points count by h3 area", fontsize=20)
    h3_df.plot(column="buildings_count", cmap='OrRd',  legend=True, ax=ax)
    buildings_gdf.plot(ax=ax, markersize=0.05, alpha=0.1, color="grey")

    fig.savefig(results_path / f"{city_name}_h3_buildings.png")


def green_areas_plotter(points_gdf, city_bounds_gdf, results_path, city_name):
    """
    Plots green area points in green and city boundaries, and saves the plot as an image.

    Parameters:
    - points_gdf (GeoDataFrame): GeoDataFrame containing green area point geometries to be plotted in green.
    - city_boundary_gdf (GeoDataFrame): GeoDataFrame containing city boundary geometries.
    - results_path (str): Path to the directory where the plot image will be saved.
    - city_name (str): Name of the city for which the plot is generated.

    Returns:
    - None
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.suptitle(f"{city_name} green areas", fontsize=20)

    points_gdf.plot(ax=ax, color='green', markersize=5)

    city_bounds_gdf.plot(ax=ax, edgecolor='black', facecolor='none')

    fig.savefig(results_path / f"{city_name}_green_areas.png")


def buildings_plotter(points_gdf, city_bounds_gdf, results_path, city_name):
    """
    Plots buidlings points and city boundaries, and saves the plot as an image.

    Parameters:
    - points_gdf (GeoDataFrame): GeoDataFrame containing buildings point geometries to be plotted in grey.
    - city_boundary_gdf (GeoDataFrame): GeoDataFrame containing city boundary geometries.
    - results_path (str): Path to the directory where the plot image will be saved.
    - city_name (str): Name of the city for which the plot is generated.

    Returns:
    - None
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.suptitle(f"{city_name} buildings", fontsize=20)

    points_gdf.plot(ax=ax, color='grey', markersize=5)

    city_bounds_gdf.plot(ax=ax, edgecolor='black', facecolor='none')

    fig.savefig(results_path / f"{city_name}_buildings.png")


def h3_count_population_plotter(h3_population_gdf, results_path, city_name):
    """
    Plots population by H3 area and saves the plot as an image.

    Parameters:
    - h3_population_gdf (GeoDataFrame): GeoDataFrame containing aggregated H3 hexagons with counts and geometries.
    - results_path (str): Path to the directory where the plot image will be saved.
    - city_name (str): Name of the city for which the plot is generated.

    Returns:
    - None
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.suptitle(f"{city_name} population by h3 area", fontsize=20)
    h3_population_gdf.plot(column="population", cmap='OrRd', legend=True, ax=ax)

    fig.savefig(results_path / f"{city_name}_h3_population.png")


def recreational_areas_plotter(points_gdf, city_bounds_gdf, results_path, city_name):
    """
    Plots recreational_areas points and city boundaries, and saves the plot as an image.

    Parameters:
    - points_gdf (GeoDataFrame): GeoDataFrame containing recreational_areas point geometries to be plotted in black.
    - city_boundary_gdf (GeoDataFrame): GeoDataFrame containing city boundary geometries.
    - results_path (str): Path to the directory where the plot image will be saved.
    - city_name (str): Name of the city for which the plot is generated.

    Returns:
    - None
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.suptitle(f"{city_name} recreational areas", fontsize=20)

    points_gdf.plot(ax=ax, color='black', markersize=5)

    city_bounds_gdf.plot(ax=ax, edgecolor='black', facecolor='none')

    fig.savefig(results_path / f"{city_name}_reacreational_areas.png")


def h3_count_recreational_areas_plotter(recreational_areas_gdf, h3_df, results_path, city_name):
    """
    Plots recreational areas points count by H3 area and saves the plot as an image.

    Parameters:
    - buildings_gdf (GeoDataFrame): GeoDataFrame containing recreational areas geometries.
    - h3_df (GeoDataFrame): GeoDataFrame containing aggregated H3 hexagons with counts and geometries.
    - results_path (str): Path to the directory where the plot image will be saved.
    - city_name (str): Name of the city for which the plot is generated.

    Returns:
    - None
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.suptitle(f"{city_name} recreational areas points count by h3 area", fontsize=20)
    h3_df.plot(column="recreational_areas_count", cmap='OrRd',  legend=True, ax=ax)
    recreational_areas_gdf.plot(ax=ax, markersize=0.4, alpha=1, color="black")

    fig.savefig(results_path / f"{city_name}_h3_recreational_areas.png")


def distance_to_centrum_plotter(h3_df, central_point, results_path, city_name):
    """
    Plots distance from each h3 area to centrum and city boundaries, and saves the plot as an image.

    Parameters:
    - h3_df (GeoDataFrame): GeoDataFrame containing h3 areas and its distances to centrum.
    - city_boundary_gdf (GeoDataFrame): GeoDataFrame containing city boundary geometries.
    - results_path (str): Path to the directory where the plot image will be saved.
    - city_name (str): Name of the city for which the plot is generated.

    Returns:
    - None
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.suptitle(f"Distance from each h3 area to centrum in {city_name}", fontsize=20)

    h3_df.plot(column="distance_to_centrum", cmap='OrRd', legend=True, ax=ax)
    plt.scatter(central_point[0], central_point[1], color="black", s=30, label="Central point")
    ax.legend()
    fig.savefig(results_path / f"{city_name}_distance_to_centrum.png")


def results_h3_count_bike_path_plotter(h3_df, results_path, city_name):
    """
    Plots bike path count prediction by H3 area and saves the plot as an image.

    Parameters:
    - h3_df (GeoDataFrame): GeoDataFrame containing aggregated H3 hexagons with predicted counts of bike_paths and geometries.
    - results_path (str): Path to the directory where the plot image will be saved.
    - city_name (str): Name of the city for which the plot is generated.

    Returns:
    - None
    """
    fig, ax = plt.subplots(1, 2, figsize=(12, 10))
    fig.suptitle(f"{city_name} bike paths count by h3 area", fontsize=20)

    max_value = max(h3_df['bike_paths_count'].max(), h3_df['prediction'].max())

    h3_df.plot(column="bike_paths_count", cmap='OrRd', legend=True, ax=ax[0], vmin=0, vmax=max_value)
    ax[0].set_title(f"Real {city_name} data")

    h3_df.plot(column="prediction", cmap='OrRd', legend=True, ax=ax[1], vmin=0, vmax=max_value)
    ax[1].set_title(f"Predicted {city_name} data")

    fig.savefig(results_path / f"{city_name}_predicted_bike_paths.png")


def results_h3_difference_bike_path_plotter(h3_df, results_path, city_name):
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.suptitle(f"Difference between predicted and actual bike paths in {city_name}  by h3 area", fontsize=20)

    h3_df["difference"] = h3_df["prediction"] - h3_df["bike_paths_count"]
    h3_df.plot(column="difference", cmap='OrRd', legend=True, ax=ax)

    fig.savefig(results_path / f"{city_name}_predicted_difference_bike_paths.png")