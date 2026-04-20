# Crop Yield Prediction Model

This project contains a simple supervised machine learning model to predict crop yields (tons per hectare) using a Random Forest algorithm. It is designed to work with the [Agriculture Crop Yield Dataset from Kaggle](https://www.kaggle.com/datasets/samuelotiattakorah/agriculture-crop-yield).

## Setup Instructions

1. **Install Dependencies**
   It's recommended to create a virtual environment first, then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download the Dataset**
   Go to Kaggle and download the `crop_yield.csv`. Place it in the same directory as the script.
   
3. **Run the Model**
   ```bash
   python crop_yield_model.py
   ```

## Model Pipeline

1. **Preprocessing**
   - **Categorical Data:** `Region`, `Soil_Type`, `Crop`, `Weather_Condition`, `Fertilizer_Used`, `Irrigation_Used` are one-hot encoded using `OneHotEncoder`.
   - **Numerical Data:** `Rainfall_mm`, `Temperature_Celsius`, `Days_to_Harvest` are scaled using `StandardScaler`.

2. **Algorithm**
   - **RandomForestRegressor:** We use a Random Forest model as it naturally handles non-linear interactions well and provides useful feature importances out-of-the-box.

3. **Evaluation**
   - We split the data into 80% training and 20% testing sets.
   - We calculate Mean Squared Error (MSE), Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), and R-squared to evaluate model performance.

4. **Feature Importance**
   - The script will export a bar chart `feature_importance.png` showing which features contributed most heavily to the prediction algorithm.
