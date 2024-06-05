import requests


def boundaries_download(place):
    """
       Downloads boundary coordinates for a specified place using the Nominatim API.

       Parameters:
       - place (str): The name of the place for which boundary coordinates are to be downloaded.

       Returns:
       - coords (list): List of coordinate tuples representing the boundary of the specified place.
         Returns None if no boundary data is found or if there's an error in fetching the data.
       """
    base_url = "https://nominatim.openstreetmap.org/search"

    place_name = place
    params = {"q": place_name,
              "format": "json",
              "polygon_geojson": 1}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()

        coords = data[0]["geojson"]["coordinates"][0][0]
        return coords
    return None
