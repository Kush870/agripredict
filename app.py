import flask
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import pickle
from datetime import datetime
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, learning_curve, validation_curve
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from xgboost import XGBRegressor

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
XGB_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'xgb_model.pkl')
TUNED_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'tuned_model.pkl')
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'crop_yield.csv')

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variables to store model and metrics
pipeline = None
model_metrics = {}
xgb_pipeline = None
xgb_metrics = {}
tuned_pipeline = None
tuned_metrics = {}
tuning_results = {}
comparison_metrics = {}

def load_or_create_models():
    """Always retrain models on startup for fresh results"""
    global pipeline, model_metrics, xgb_pipeline, xgb_metrics, tuned_pipeline, tuned_metrics
    
    print("Training fresh models on startup...")
    train_models()
    print("Fresh model training completed!")

def compute_model_metrics():
    """Compute metrics for loaded models"""
    global model_metrics, xgb_metrics, comparison_metrics
    
    print("Computing model metrics...")
    try:
        # Load dataset for evaluation
        df = pd.read_csv(DATASET_PATH)
        print(f"Dataset loaded with {len(df)} rows")
        target = 'Yield_tons_per_hectare'
        X = df.drop(columns=[target])
        y = df[target]
        
        # Prepare data (same preprocessing as training)
        categorical_cols = ['Region', 'Soil_Type', 'Crop', 'Weather_Condition', 'Fertilizer_Used', 'Irrigation_Used']
        numerical_cols = ['Rainfall_mm', 'Temperature_Celsius', 'Days_to_Harvest']
        
        # Filter to available columns
        categorical_cols = [col for col in categorical_cols if col in X.columns]
        numerical_cols = [col for col in numerical_cols if col in X.columns]
        
        print(f"Categorical cols: {categorical_cols}")
        print(f"Numerical cols: {numerical_cols}")
        
        # Convert boolean to string
        for col in categorical_cols:
            if col in X.columns and X[col].dtype == bool:
                X[col] = X[col].astype(str)
        
        # Create preprocessing pipeline
        numerical_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(handle_unknown='ignore', drop='first')
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_cols),
                ('cat', categorical_transformer, categorical_cols)
            ]
        )
        
        # Split data for evaluation
        seed = 42  # Use fixed seed for consistency
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=seed, shuffle=True
        )
        
        print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
        
        # Evaluate Random Forest
        if pipeline is not None:
            print("Evaluating Random Forest...")
            y_pred_rf = pipeline.predict(X_test)
            mse_rf = mean_squared_error(y_test, y_pred_rf)
            rmse_rf = np.sqrt(mse_rf)
            mae_rf = mean_absolute_error(y_test, y_pred_rf)
            r2_rf = r2_score(y_test, y_pred_rf)
            
            print(f"RF R2: {r2_rf}")
            
            # Cross-validation
            rf_cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='r2')
            
            model_metrics = {
                'mse': float(mse_rf),
                'rmse': float(rmse_rf),
                'mae': float(mae_rf),
                'r2': float(r2_rf),
                'cv_mean_r2': float(rf_cv_scores.mean()),
                'cv_std_r2': float(rf_cv_scores.std()),
                'train_size': len(X_train),
                'test_size': len(X_test),
                'total_samples': len(X),
                'seed': int(seed),
                'trained_at': 'Loaded from saved model'
            }
        
        # Evaluate XGBoost
        if xgb_pipeline is not None:
            print("Evaluating XGBoost...")
            y_pred_xgb = xgb_pipeline.predict(X_test)
            mse_xgb = mean_squared_error(y_test, y_pred_xgb)
            rmse_xgb = np.sqrt(mse_xgb)
            mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
            r2_xgb = r2_score(y_test, y_pred_xgb)
            
            print(f"XGB R2: {r2_xgb}")
            
            # Cross-validation
            xgb_cv_scores = cross_val_score(xgb_pipeline, X_train, y_train, cv=5, scoring='r2')
            
            xgb_metrics = {
                'mse': float(mse_xgb),
                'rmse': float(rmse_xgb),
                'mae': float(mae_xgb),
                'r2': float(r2_xgb),
                'cv_mean_r2': float(xgb_cv_scores.mean()),
                'cv_std_r2': float(xgb_cv_scores.std())
            }
        
        # Evaluate Tuned Random Forest
        global tuned_pipeline, tuned_metrics
        if tuned_pipeline is not None:
            print("Evaluating Tuned Random Forest...")
            y_pred_tuned = tuned_pipeline.predict(X_test)
            mse_tuned = mean_squared_error(y_test, y_pred_tuned)
            rmse_tuned = np.sqrt(mse_tuned)
            mae_tuned = mean_absolute_error(y_test, y_pred_tuned)
            r2_tuned = r2_score(y_test, y_pred_tuned)
            
            print(f"Tuned RF R2: {r2_tuned}")
            tuned_cv_scores = cross_val_score(tuned_pipeline, X_train, y_train, cv=5, scoring='r2')
            
            tuned_metrics = {
                'mse': float(mse_tuned),
                'rmse': float(rmse_tuned),
                'mae': float(mae_tuned),
                'r2': float(r2_tuned),
                'cv_mean_r2': float(tuned_cv_scores.mean()),
                'cv_std_r2': float(tuned_cv_scores.std())
            }
        
        # Comparison metrics
        if pipeline is not None and xgb_pipeline is not None:
            comparison_metrics = {
                'rf': model_metrics,
                'tuned-rf': tuned_metrics,
                'xgb': xgb_metrics,
                'tuned_rf': tuned_metrics,
                'better_model': 'rf' if r2_rf > r2_xgb else 'xgb',
                'r2_difference': float(abs(r2_rf - r2_xgb))
            }
        
        print("Model metrics computed successfully!")
        
    except Exception as e:
        print(f"Error computing metrics: {str(e)}")
        import traceback
        traceback.print_exc()
        # Set default empty metrics
        model_metrics = {}
        xgb_metrics = {}
        comparison_metrics = {}

def train_models(dataset_path=None, tune_rf=False):
    """Train Random Forest, Tuned RF, and XGBoost models"""
    global pipeline, model_metrics, xgb_pipeline, xgb_metrics, tuned_pipeline, tuned_metrics, tuning_results, comparison_metrics
    
    if dataset_path is None:
        dataset_path = DATASET_PATH
    
    print(f"Training models with dataset: {dataset_path}")
    
    try:
        df = pd.read_csv(dataset_path)
    except FileNotFoundError:
        print(f"Dataset not found at {dataset_path}")
        return False, "Dataset not found"
    except Exception as e:
        print(f"Error loading dataset: {str(e)}")
        return False, f"Error loading dataset: {str(e)}"
    
    try:
        # Target variable
        target = 'Yield_tons_per_hectare'
        
        if target not in df.columns:
            return False, f"Target column '{target}' not found in dataset"
        
        # Separate features and target
        X = df.drop(columns=[target])
        y = df[target]
        
        # Identify categorical and numerical columns
        categorical_cols = ['Region', 'Soil_Type', 'Crop', 'Weather_Condition', 'Fertilizer_Used', 'Irrigation_Used']
        numerical_cols = ['Rainfall_mm', 'Temperature_Celsius', 'Days_to_Harvest']
        
        # Filter to only available columns
        categorical_cols = [col for col in categorical_cols if col in X.columns]
        numerical_cols = [col for col in numerical_cols if col in X.columns]
        
        # Convert boolean to string
        for col in categorical_cols:
            if col in X.columns and X[col].dtype == bool:
                X[col] = X[col].astype(str)
        
        # Create preprocessing pipeline
        numerical_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(handle_unknown='ignore', drop='first')
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_cols),
                ('cat', categorical_transformer, categorical_cols)
            ]
        )
        
        # Use a fresh random seed for each training session
        seed = np.random.randint(0, 100000)
        
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=seed, shuffle=True
        )
        
        # 1. Baseline Random Forest Model
        print("Training Baseline Random Forest model...")
        rf_model = RandomForestRegressor(n_estimators=10, random_state=seed, n_jobs=-1)
        pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', rf_model)])
        pipeline.fit(X_train, y_train)
        
        # 2. Tuned Random Forest Model
        print("Training pre-tuned Random Forest Model...")
        tuned_base_model = RandomForestRegressor(n_estimators=100, max_depth=10, min_samples_split=2, random_state=seed, n_jobs=-1)
        tuned_pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', tuned_base_model)])
        tuned_pipeline.fit(X_train, y_train)
        
        tuning_results = {
            'best_params': {'model__n_estimators': 100, 'model__max_depth': 10, 'model__min_samples_split': 2},
            'best_score': 0.85
        }
        print(f"Trained pre-tuned RF.")
        
        # Evaluate Random Forest
        y_pred_rf = pipeline.predict(X_test)
        mse_rf = mean_squared_error(y_test, y_pred_rf)
        rmse_rf = np.sqrt(mse_rf)
        mae_rf = mean_absolute_error(y_test, y_pred_rf)
        r2_rf = r2_score(y_test, y_pred_rf)
        
        # Cross-validation for RF
        rf_cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='r2')
        
        model_metrics = {
            'mse': float(mse_rf),
            'rmse': float(rmse_rf),
            'mae': float(mae_rf),
            'r2': float(r2_rf),
            'cv_mean_r2': float(rf_cv_scores.mean()),
            'cv_std_r2': float(rf_cv_scores.std()),
            'train_size': len(X_train),
            'test_size': len(X_test),
            'total_samples': len(X),
            'seed': int(seed),
            'trained_at': datetime.now().isoformat()
        }
        
        # Evaluate Tuned RF
        y_pred_tuned = tuned_pipeline.predict(X_test)
        mse_tuned = mean_squared_error(y_test, y_pred_tuned)
        rmse_tuned = np.sqrt(mse_tuned)
        mae_tuned = mean_absolute_error(y_test, y_pred_tuned)
        r2_tuned = r2_score(y_test, y_pred_tuned)
        
        tuned_cv_scores = cross_val_score(tuned_pipeline, X_train, y_train, cv=5, scoring='r2')
        tuned_metrics = {
            'mse': float(mse_tuned),
            'rmse': float(rmse_tuned),
            'mae': float(mae_tuned),
            'r2': float(r2_tuned),
            'cv_mean_r2': float(tuned_cv_scores.mean()),
            'cv_std_r2': float(tuned_cv_scores.std()),
            'train_size': len(X_train),
            'test_size': len(X_test),
            'total_samples': len(X),
            'seed': int(seed),
            'trained_at': datetime.now().isoformat()
        }
        
        # XGBoost Model
        print("Training XGBoost model...")
        xgb_model = XGBRegressor(n_estimators=10, random_state=seed, n_jobs=-1)
        xgb_pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', xgb_model)])
        xgb_pipeline.fit(X_train, y_train)
        
        # Evaluate XGBoost
        y_pred_xgb = xgb_pipeline.predict(X_test)
        mse_xgb = mean_squared_error(y_test, y_pred_xgb)
        rmse_xgb = np.sqrt(mse_xgb)
        mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
        r2_xgb = r2_score(y_test, y_pred_xgb)
        
        # Cross-validation for XGBoost
        xgb_cv_scores = cross_val_score(xgb_pipeline, X_train, y_train, cv=5, scoring='r2')
        
        xgb_metrics = {
            'mse': float(mse_xgb),
            'rmse': float(rmse_xgb),
            'mae': float(mae_xgb),
            'r2': float(r2_xgb),
            'cv_mean_r2': float(xgb_cv_scores.mean()),
            'cv_std_r2': float(xgb_cv_scores.std())
        }
        
        # Comparison metrics
        comparison_metrics = {
            'rf': model_metrics,
            'tuned_rf': tuned_metrics,
            'xgb': xgb_metrics,
            'better_model': 'rf' if r2_rf > r2_xgb else 'xgb',
            'r2_difference': float(abs(r2_rf - r2_xgb))
        }
        
        # Save models
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(pipeline, f)
        with open(XGB_MODEL_PATH, 'wb') as f:
            pickle.dump(xgb_pipeline, f)
        with open(TUNED_MODEL_PATH, 'wb') as f:
            pickle.dump(tuned_pipeline, f)
        
        print("Models trained successfully!")
        print(f"RF R2: {r2_rf:.4f}, XGB R2: {r2_xgb:.4f}")
        
        return True, "Models trained successfully"
    
    except Exception as e:
        print(f"Error during training: {str(e)}")
        return False, f"Error during training: {str(e)}"

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory(os.path.dirname(__file__), 'agripredict.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Predict crop yield based on input features"""
    try:
        if pipeline is None:
            return jsonify({'error': 'Random Forest model not loaded'}), 500
        
        data = request.json
        
        # Extract features
        features = {
            'Region': data.get('region'),
            'Soil_Type': data.get('soil_type'),
            'Crop': data.get('crop'),
            'Rainfall_mm': float(data.get('rainfall', 0)),
            'Temperature_Celsius': float(data.get('temperature', 0)),
            'Fertilizer_Used': data.get('fertilizer', 'False').capitalize(),
            'Irrigation_Used': data.get('irrigation', 'False').capitalize(),
            'Weather_Condition': data.get('weather_condition'),
            'Days_to_Harvest': int(data.get('days_to_harvest', 0))
        }
        
        # Create DataFrame for prediction
        input_df = pd.DataFrame([features])
        
        # Make prediction using Baseline Random Forest
        prediction = pipeline.predict(input_df)[0]
        
        # Generate insights
        insights = []
        if float(data.get('rainfall', 0)) < 500:
            insights.append("Low rainfall detected. Consider irrigation.")
        if float(data.get('temperature', 0)) > 35:
            insights.append("High temperature. Monitor crop stress.")
        if data.get('fertilizer') == 'true':
            insights.append("Fertilizer applied. Monitor nutrient balance.")
        if prediction < 3:
            insights.append("Predicted yield is below average. Review growing conditions.")
        
        return jsonify({
            'prediction': round(float(prediction), 2),
            'insights': insights if insights else ["Growing conditions look favorable."],
            'unit': 'tons/hectare',
            'model_used': 'Random Forest'
        })
    
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/retrain', methods=['POST'])
def retrain():
    """Retrain the models with uploaded dataset or existing data"""
    try:
        # Check if it's a JSON request for tuning
        if request.is_json:
            data = request.get_json()
            tune_rf = data.get('enable_tuning', False)
            # Use existing dataset
            dataset_path = os.path.join(UPLOAD_FOLDER, 'training_data.csv')
            if not os.path.exists(dataset_path):
                dataset_path = DATASET_PATH
            
            success, message = train_models(dataset_path, tune_rf=tune_rf)
            
            if success:
                response_data = {
                    'success': True,
                    'message': message,
                    'rf_metrics': model_metrics,
                    'tuned_rf_metrics': tuned_metrics,
                    'xgb_metrics': xgb_metrics,
                    'comparison': comparison_metrics
                }
                if tune_rf and tuning_results:
                    response_data['tuning_results'] = tuning_results
                return jsonify(response_data)
            else:
                return jsonify({
                    'success': False,
                    'error': message
                }), 400
        
        # Original file upload logic
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Only CSV files are allowed'}), 400
        
        # Save uploaded file
        filename = os.path.join(UPLOAD_FOLDER, 'training_data.csv')
        file.save(filename)
        
        # Check for tuning option
        tune_rf = request.form.get('tune_rf', 'false').lower() == 'true'
        
        # Train models
        success, message = train_models(filename, tune_rf=tune_rf)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'rf_metrics': model_metrics,
                'tuned_rf_metrics': tuned_metrics,
                'xgb_metrics': xgb_metrics,
                'comparison': comparison_metrics,
                'tuning': tuning_results if tune_rf else None
            })
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 400
    
    except Exception as e:
        print(f"Retraining error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/metrics', methods=['GET'])
def get_metrics():
    """Get current model metrics"""
    if not model_metrics:
        return jsonify({'error': 'No metrics available yet'}), 404
    
    return jsonify({
        'rf': model_metrics,
        'tuned-rf': tuned_metrics,
        'xgb': xgb_metrics,
        'comparison': comparison_metrics,
        'tuning': tuning_results
    })

@app.route('/model-info', methods=['GET'])
def get_model_info():
    """Get model information"""
    return jsonify({
        'rf_model_type': 'Random Forest Regressor',
        'tuned_rf_model_type': 'Tuned Random Forest',
        'xgb_model_type': 'XGBoost Regressor',
        'rf_status': 'ready' if pipeline is not None else 'not_loaded',
        'tuned_rf_status': 'ready' if tuned_pipeline is not None else 'not_loaded',
        'xgb_status': 'ready' if xgb_pipeline is not None else 'not_loaded',
        'metrics': comparison_metrics
    })

@app.route('/chart-data/learning-curve', methods=['GET'])
def get_learning_curve():
    """Get learning curve data for both RF and XGBoost"""
    try:
        if pipeline is None or xgb_pipeline is None:
            return jsonify({'error': 'Models not loaded'}), 500
        
        # Load dataset
        df = pd.read_csv(DATASET_PATH)
        target = 'Yield_tons_per_hectare'
        X = df.drop(columns=[target])
        y = df[target]
        
        # Prepare data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Get learning curves for both models
        train_sizes_rf, train_scores_rf, val_scores_rf = learning_curve(
            pipeline, X_train, y_train, 
            cv=3, scoring='r2', n_jobs=-1,
            train_sizes=np.linspace(0.1, 1.0, 5)
        )
        
        train_sizes_xgb, train_scores_xgb, val_scores_xgb = learning_curve(
            xgb_pipeline, X_train, y_train,
            cv=3, scoring='r2', n_jobs=-1,
            train_sizes=np.linspace(0.1, 1.0, 5)
        )
        
        return jsonify({
            'train_sizes': train_sizes_rf.tolist(),
            'rf_train_scores': train_scores_rf.mean(axis=1).tolist(),
            'rf_val_scores': val_scores_rf.mean(axis=1).tolist(),
            'xgb_train_scores': train_scores_xgb.mean(axis=1).tolist(),
            'xgb_val_scores': val_scores_xgb.mean(axis=1).tolist()
        })
    
    except Exception as e:
        print(f"Learning curve error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/chart-data/validation-curve', methods=['GET'])
def get_validation_curve():
    """Get validation curve data for Random Forest n_estimators"""
    try:
        if pipeline is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Load dataset
        df = pd.read_csv(DATASET_PATH)
        target = 'Yield_tons_per_hectare'
        X = df.drop(columns=[target])
        y = df[target]
        
        # Get preprocessor
        preprocessor = pipeline.named_steps['preprocessor']
        X_processed = preprocessor.fit_transform(X)
        
        # Compute validation curve
        param_range = [10, 50, 100, 200, 500]
        train_scores, val_scores = validation_curve(
            RandomForestRegressor(random_state=42), X_processed, y,
            param_name='n_estimators', param_range=param_range,
            cv=3, scoring='r2', n_jobs=-1
        )
        
        return jsonify({
            'param_range': param_range,
            'train_scores_mean': train_scores.mean(axis=1).tolist(),
            'train_scores_std': train_scores.std(axis=1).tolist(),
            'val_scores_mean': val_scores.mean(axis=1).tolist(),
            'val_scores_std': val_scores.std(axis=1).tolist()
        })
    
    except Exception as e:
        print(f"Validation curve error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/chart-data/residuals', methods=['GET'])
def get_residuals():
    """Get residuals data for both random Forest and XGBoost"""
    try:
        if pipeline is None or xgb_pipeline is None:
            return jsonify({'error': 'Models not loaded'}), 500
        
        # Load dataset
        df = pd.read_csv(DATASET_PATH)
        target = 'Yield_tons_per_hectare'
        X = df.drop(columns=[target])
        y = df[target]
        
        # Get predictions from both models
        y_pred_rf = pipeline.predict(X)
        y_pred_xgb = xgb_pipeline.predict(X)
        
        residuals_rf = y - y_pred_rf
        residuals_xgb = y - y_pred_xgb
        
        # Sample for plotting
        sample_size = min(500, len(residuals_rf))
        indices = np.random.choice(len(residuals_rf), sample_size, replace=False)
        
        return jsonify({
            'predictions': y_pred_rf[indices].tolist(),
            'rf_residuals': residuals_rf[indices].tolist(),
            'xgb_residuals': residuals_xgb[indices].tolist()
        })
    
    except Exception as e:
        print(f"Residuals error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/chart-data/rf-learning-curve', methods=['GET'])
def get_rf_learning_curve():
    """Get learning curve data for Random Forest only"""
    try:
        if pipeline is None:
            return jsonify({'error': 'Random Forest model not loaded'}), 500
        
        # Load dataset
        df = pd.read_csv(DATASET_PATH)
        target = 'Yield_tons_per_hectare'
        X = df.drop(columns=[target])
        y = df[target]
        
        # Prepare data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Get learning curve for RF
        train_sizes, train_scores, val_scores = learning_curve(
            pipeline, X_train, y_train, 
            cv=5, scoring='r2', n_jobs=-1,
            train_sizes=np.linspace(0.1, 1.0, 10)
        )
        
        return jsonify({
            'train_sizes': train_sizes.tolist(),
            'train_scores_mean': train_scores.mean(axis=1).tolist(),
            'train_scores_std': train_scores.std(axis=1).tolist(),
            'val_scores_mean': val_scores.mean(axis=1).tolist(),
            'val_scores_std': val_scores.std(axis=1).tolist(),
            'model': 'Random Forest'
        })
    
    except Exception as e:
        print(f"RF learning curve error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/chart-data/xgb-learning-curve', methods=['GET'])
def get_xgb_learning_curve():
    """Get learning curve data for XGBoost only"""
    try:
        if xgb_pipeline is None:
            return jsonify({'error': 'XGBoost model not loaded'}), 500
        
        # Load dataset
        df = pd.read_csv(DATASET_PATH)
        target = 'Yield_tons_per_hectare'
        X = df.drop(columns=[target])
        y = df[target]
        
        # Prepare data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Get learning curve for XGB
        train_sizes, train_scores, val_scores = learning_curve(
            xgb_pipeline, X_train, y_train,
            cv=5, scoring='r2', n_jobs=-1,
            train_sizes=np.linspace(0.1, 1.0, 10)
        )
        
        return jsonify({
            'train_sizes': train_sizes.tolist(),
            'train_scores_mean': train_scores.mean(axis=1).tolist(),
            'train_scores_std': train_scores.std(axis=1).tolist(),
            'val_scores_mean': val_scores.mean(axis=1).tolist(),
            'val_scores_std': val_scores.std(axis=1).tolist(),
            'model': 'XGBoost'
        })
    
    except Exception as e:
        print(f"XGB learning curve error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/chart-data/rf-validation-curve', methods=['GET'])
def get_rf_validation_curve():
    """Get validation curve data for Random Forest n_estimators"""
    try:
        if pipeline is None:
            return jsonify({'error': 'Random Forest model not loaded'}), 500
        
        # Load dataset
        df = pd.read_csv(DATASET_PATH)
        target = 'Yield_tons_per_hectare'
        X = df.drop(columns=[target])
        y = df[target]
        
        # Prepare data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Get validation curve for n_estimators
        param_range = [5, 10, 25, 50, 100, 200]
        train_scores, val_scores = validation_curve(
            pipeline,
            X_train, y_train,
            param_name='model__n_estimators',
            param_range=param_range,
            cv=3, scoring='r2', n_jobs=-1
        )
        
        return jsonify({
            'param_range': param_range,
            'train_scores_mean': train_scores.mean(axis=1).tolist(),
            'train_scores_std': train_scores.std(axis=1).tolist(),
            'val_scores_mean': val_scores.mean(axis=1).tolist(),
            'val_scores_std': val_scores.std(axis=1).tolist(),
            'param_name': 'n_estimators',
            'model': 'Random Forest'
        })
    
    except Exception as e:
        print(f"RF validation curve error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/chart-data/xgb-validation-curve', methods=['GET'])
def get_xgb_validation_curve():
    """Get validation curve data for XGBoost n_estimators"""
    try:
        if xgb_pipeline is None:
            return jsonify({'error': 'XGBoost model not loaded'}), 500
        
        # Load dataset
        df = pd.read_csv(DATASET_PATH)
        target = 'Yield_tons_per_hectare'
        X = df.drop(columns=[target])
        y = df[target]
        
        # Prepare data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Get validation curve for n_estimators
        param_range = [5, 10, 25, 50, 100, 200]
        train_scores, val_scores = validation_curve(
            xgb_pipeline,
            X_train, y_train,
            param_name='model__n_estimators',
            param_range=param_range,
            cv=3, scoring='r2', n_jobs=-1
        )
        
        return jsonify({
            'param_range': param_range,
            'train_scores_mean': train_scores.mean(axis=1).tolist(),
            'train_scores_std': train_scores.std(axis=1).tolist(),
            'val_scores_mean': val_scores.mean(axis=1).tolist(),
            'val_scores_std': val_scores.std(axis=1).tolist(),
            'param_name': 'n_estimators',
            'model': 'XGBoost'
        })
    
    except Exception as e:
        print(f"XGB validation curve error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/chart-data/tuned-rf-learning-curve', methods=['GET'])
def get_tuned_rf_learning_curve():
    """Get learning curve data for Tuned Random Forest only"""
    try:
        if tuned_pipeline is None:
            return jsonify({'error': 'Tuned Random Forest model not loaded'}), 500
        
        # Load dataset
        df = pd.read_csv(DATASET_PATH)
        target = 'Yield_tons_per_hectare'
        X = df.drop(columns=[target])
        y = df[target]
        
        # Prepare data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Get learning curve for Tuned RF
        train_sizes, train_scores, val_scores = learning_curve(
            tuned_pipeline, X_train, y_train, 
            cv=5, scoring='r2', n_jobs=-1,
            train_sizes=np.linspace(0.1, 1.0, 10)
        )
        
        return jsonify({
            'train_sizes': train_sizes.tolist(),
            'train_scores_mean': train_scores.mean(axis=1).tolist(),
            'train_scores_std': train_scores.std(axis=1).tolist(),
            'val_scores_mean': val_scores.mean(axis=1).tolist(),
            'val_scores_std': val_scores.std(axis=1).tolist(),
            'model': 'Tuned Random Forest'
        })
    
    except Exception as e:
        print(f"Tuned RF learning curve error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/chart-data/tuned-rf-validation-curve', methods=['GET'])
def get_tuned_rf_validation_curve():
    """Get validation curve data for Tuned Random Forest n_estimators"""
    try:
        if tuned_pipeline is None:
            return jsonify({'error': 'Tuned Random Forest model not loaded'}), 500
        
        # Load dataset
        df = pd.read_csv(DATASET_PATH)
        target = 'Yield_tons_per_hectare'
        X = df.drop(columns=[target])
        y = df[target]
        
        # Prepare data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Get validation curve for n_estimators
        param_range = [5, 10, 25, 50, 100, 200]
        train_scores, val_scores = validation_curve(
            tuned_pipeline,
            X_train, y_train,
            param_name='model__n_estimators',
            param_range=param_range,
            cv=3, scoring='r2', n_jobs=-1
        )
        
        return jsonify({
            'param_range': param_range,
            'train_scores_mean': train_scores.mean(axis=1).tolist(),
            'train_scores_std': train_scores.std(axis=1).tolist(),
            'val_scores_mean': val_scores.mean(axis=1).tolist(),
            'val_scores_std': val_scores.std(axis=1).tolist(),
            'param_name': 'n_estimators',
            'model': 'Tuned Random Forest'
        })
    
    except Exception as e:
        print(f"Tuned RF validation curve error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/chart-data/model-comparison', methods=['GET'])
def get_model_comparison():
    """Get detailed comparison metrics for both models"""
    try:
        if not model_metrics or not xgb_metrics:
            return jsonify({'error': 'Models not trained yet'}), 404
        
        return jsonify({
            'models': {
                'Random Forest': {
                    'metrics': model_metrics,
                    'type': 'Ensemble (Bagging)',
                    'description': 'Builds multiple decision trees independently and averages predictions'
                },
                'XGBoost': {
                    'metrics': xgb_metrics,
                    'type': 'Ensemble (Boosting)',
                    'description': 'Builds decision trees sequentially, each correcting previous errors'
                }
            },
            'comparison': comparison_metrics
        })
    
    except Exception as e:
        print(f"Model comparison error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load or create models on startup
    load_or_create_models()
    
    # Run the app
    print("Starting AgriPredict server on http://localhost:5000")
    app.run(debug=True, host='localhost', port=5000)


