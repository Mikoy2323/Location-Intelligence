import pandas as pd
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import joblib


def scale_data(data):
    """
        Standardizes the numerical values in the provided DataFrame.

        This function applies z-score normalization to each feature in the input
        DataFrame, transforming the data such that it has a mean of 0 and a
        standard deviation of 1.

        Parameters:
        data (pd.DataFrame): A pandas DataFrame containing the data to be standardized.
                             Each column should contain numerical values.

        Returns:
        pd.DataFrame: A new DataFrame with the same column names as the input, where
                      each value has been standardized (mean = 0, standard deviation = 1).
        """
    scaler = StandardScaler()
    scaler.fit(data)
    col_names = data.columns
    data_res = pd.DataFrame(data=scaler.transform(data), columns=col_names)
    return data_res


def krakow_prediction(krakow_dataset):
    """
        Makes predictions using a pre-trained model on the provided Krakow dataset.

        This function loads a pre-trained model from a specified file, scales the relevant
        features of the input dataset, and then makes predictions based on these features.
        The predictions are added as a new column to the input DataFrame.

        Parameters:
        krakow_dataset (pd.DataFrame): A pandas DataFrame containing the dataset for Krakow.

        Returns:
        pd.DataFrame: The input DataFrame with an additional column 'prediction' containing
                      the predictions made by the model.
        """
    model = joblib.load(Path.cwd() / "models_best" / "model.pkl")
    scaled_data = scale_data(krakow_dataset.drop(columns=["h3_index", "bike_paths_count", "geometry"]))
    predictions = model.predict(scaled_data)
    krakow_dataset["prediction"] = predictions
    return krakow_dataset


if __name__ == "__main__":
    pass
