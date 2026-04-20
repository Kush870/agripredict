import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

import os

def main():
    # ---------------------------------------------------------
    # 1. Load the Dataset
    # ---------------------------------------------------------
    # Please ensure you have downloaded the dataset from Kaggle:
    # https://www.kaggle.com/datasets/samuelotiattakorah/agriculture-crop-yield
    # and placed the CSV file in the same directory as this script.
    # Update the file name below if it differs.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(script_dir, 'crop_yield.csv')
    
    try:
        print(f"Loading dataset from {dataset_path}...")
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f"Error: {dataset_path} not found.")
        print("Please download the dataset from Kaggle and place it in the current directory.")
        print("For demonstration, we will generate a small dummy dataset to show how the model works.")
        
        # Generating dummy data that mimics the Kaggle dataset structure
        np.random.seed(42)
        n_samples = 1000
        df = pd.DataFrame({
            'Region': np.random.choice(['North', 'East', 'South', 'West'], n_samples),
            'Soil_Type': np.random.choice(['Clay', 'Sandy', 'Loam', 'Silt', 'Peaty', 'Chalky'], n_samples),
            'Crop': np.random.choice(['Wheat', 'Rice', 'Maize', 'Barley', 'Soybean', 'Cotton'], n_samples),
            'Rainfall_mm': np.random.uniform(200, 1500, n_samples),
            'Temperature_Celsius': np.random.uniform(15, 40, n_samples),
            'Fertilizer_Used': np.random.choice([True, False], n_samples),
            'Irrigation_Used': np.random.choice([True, False], n_samples),
            'Weather_Condition': np.random.choice(['Sunny', 'Rainy', 'Cloudy'], n_samples),
            'Days_to_Harvest': np.random.randint(60, 180, n_samples),
            # Synthetic target variable with some logic
            'Yield_tons_per_hectare': np.random.uniform(1.5, 8.0, n_samples)
        })

    print("Dataset loaded successfully!")
    print("\nFirst 5 rows of the dataset:")
    print(df.head())

    # ---------------------------------------------------------
    # 2. Data Preprocessing Setup
    # ---------------------------------------------------------
    # The target variable we want to predict
    target = 'Yield_tons_per_hectare'
    
    # Separate features (X) and target (y)
    X = df.drop(columns=[target])
    y = df[target]

    # Identify categorical and numerical columns
    categorical_cols = ['Region', 'Soil_Type', 'Crop', 'Weather_Condition', 'Fertilizer_Used', 'Irrigation_Used']
    numerical_cols = ['Rainfall_mm', 'Temperature_Celsius', 'Days_to_Harvest']

    print("\nCategorical Features:", categorical_cols)
    print("Numerical Features:", numerical_cols)

    # Convert boolean columns to strings for easier one-hot encoding if needed
    for col in ['Fertilizer_Used', 'Irrigation_Used']:
        if X[col].dtype == bool:
            X[col] = X[col].astype(str)

    # Create preprocessing pipelines for numerical and categorical data
    numerical_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore', drop='first')

    # Bundle preprocessing for numerical and categorical data
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ]
    )

    # ---------------------------------------------------------
    # 3. Model Definition
    # ---------------------------------------------------------
    # We use a Random Forest Regressor, an excellent baseline supervised learning model 
    # for tabular data. It handles non-linear relationships well.
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)

    # Create the full modeling pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])

    # ---------------------------------------------------------
    # 4. Train/Test Split
    # ---------------------------------------------------------
    # Split the data into training (80%) and testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"\nTraining data shape: {X_train.shape}")
    print(f"Testing data shape: {X_test.shape}")

    # ---------------------------------------------------------
    # 5. Training the Model
    # ---------------------------------------------------------
    print("\nTraining the Random Forest model...")
    pipeline.fit(X_train, y_train)

    # ---------------------------------------------------------
    # 6. Evaluation and Predictions
    # ---------------------------------------------------------
    print("Evaluating the model on test data...")
    y_pred = pipeline.predict(X_test)

    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("-" * 30)
    print("Model Evaluation Metrics:")
    print("-" * 30)
    print(f"Mean Squared Error (MSE):      {mse:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"Mean Absolute Error (MAE):     {mae:.4f}")
    print(f"R-squared (R2 Score):          {r2:.4f}")
    print("-" * 30)

    # ---------------------------------------------------------
    # 7. Feature Importance Visualization
    # ---------------------------------------------------------
    # Extract feature names after one-hot encoding
    cat_feature_names = pipeline.named_steps['preprocessor'].transformers_[1][1].get_feature_names_out(categorical_cols)
    all_feature_names = numerical_cols + list(cat_feature_names)

    # Extract feature importances from the trained model
    importances = pipeline.named_steps['model'].feature_importances_

    # Create a DataFrame for visualization
    feature_importance_df = pd.DataFrame({
        'Feature': all_feature_names,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)

    print("\nTop 5 Most Important Features:")
    print(feature_importance_df.head())

    # Plot the feature importances
    plt.figure(figsize=(10, 8))
    feature_importance_df.head(15).sort_values(by='Importance', ascending=True).plot(
        kind='barh', x='Feature', y='Importance', color='skyblue', legend=False, ax=plt.gca()
    )
    plt.title('Top 15 Most Important Features in Crop Yield Prediction')
    plt.xlabel('Relative Importance')
    plt.ylabel('Feature')
    plt.tight_layout()
    
    # Save the plot
    plot_filename = 'feature_importance.png'
    plt.savefig(plot_filename)
    print(f"\nFeature importance plot saved as '{plot_filename}'")

if __name__ == '__main__':
    main()
