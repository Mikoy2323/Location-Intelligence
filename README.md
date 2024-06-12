# Location Intelligence

This program calculates the number of bike paths needed in specific areas of Kraków using a machine learning model trained on data extracted from OpenStreetMap about Amsterdam. Number of extra bike paths is calculated for each h3 area in both cities. The features used in the model include the amount of green areas, the amount of recreational areas(schools, shops, sport centers), population density, the number of buildings, and the distance to the city center from the specified area. During testing, models such as Random Forest, XGBoost, and SVM Regression were evaluated. The best performing model was XGBoost, achieving an R² score of 0.92.

## Table of Contents
- [Results](#results)
- [Environment](#environment)
- [Usage](#usage)

## Results
Results of the program are displayed in RESULTS directory.
It contains:
- PLOTS (plots created for chosen cities during feature enigneering)
- PREDICTIONS_PLOTS (plots containing maps of extra bike paths needed in each area)

## Environment
After cloning the repository, you need to set up a conda environment and lock the dependencies using conda-lock. Follow the steps below to achieve this:

1. Navigate to the root directory of the project.
2. Create a new conda environment using the provided `env.yml` file:

   ```bash
   conda env create -n projcet-env -f env.yml
2. Another option is to install locked environment using conda-lock
    ```bash
   conda-lock install --name project-env conda-lock.yml
   
3. Activate the newly created conda environment:
   ```bash
   conda activate project-env

## Usage
  ```bash
python run.py
  ```
Program extracts current data regarding Kraków and creates plots for each feature. New plots are generated for predicted amount of extra needed bike paths in Kraków. 
There is also implementation for plotting feature values for Amsterdam. To use this functionality line #amsterdam_dataset = city_pipeline("Amsterdam") in run.py in main() function has to be uncommented.

File model_creation.ipnyb is jupyer notebook with code used for creating prediction models. MLFlows environment was used in process of creating and testing models.




   

