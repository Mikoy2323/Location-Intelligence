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


def h3_count_plotter(bike_path_gdf, h3_df, results_path, city_name):
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
    h3_df.plot(column="count", cmap='OrRd', legend=True, ax=ax)

    fig.savefig(results_path / f"{city_name}_h3_bike_paths.png")