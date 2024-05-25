import matplotlib.pyplot as plt


def paths_plotter(bike_paths_gdf, city_bounds_gdf, results_path):
    """
      Plots bike paths over city boundaries and saves the plot as an image.

      Parameters:
      - bike_paths_gdf (GeoDataFrame): GeoDataFrame containing bike paths.
      - city_bounds_gdf (GeoDataFrame): GeoDataFrame containing city boundaries.
      - results_path (str or Path): Path where the resulting plot image will be saved.
      """

    fig, ax = plt.subplots(figsize=(12, 10))
    fig.suptitle("Amsterdam bike paths", fontsize=25)
    bike_paths_gdf.plot(ax=ax)
    city_bounds_gdf.plot(ax=ax, color="black")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    fig.savefig(results_path / "Amsterdam_bike_paths.png")