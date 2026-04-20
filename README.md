# AgriPredict - Crop Yield Intelligence System

A fully functional web application that predicts crop yield using machine learning and allows users to retrain the model with new data.

## 🎯 Features

- **Yield Prediction**: Predict crop yield based on 9 environmental and farm management factors
- **Model Retraining**: Upload custom CSV datasets to retrain the model
- **Real-time Model Metrics**: View current model performance (R², RMSE, MAE)
- **Data Visualization**: Charts showing feature importance, rainfall impact, crop yields by type
- **Drag-and-Drop Upload**: Easy file upload interface for retraining
- **Backend Integration**: Flask API for predictions and model management

## 📋 Prerequisites

- Python 3.8 or higher (recommended: Python 3.14)
- pip (Python package manager)

## 🚀 Quick Start

### Step 1: Create and activate a virtual environment

#### Windows
```cmd
python -m venv .venv
.\.venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 2: Install Dependencies

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

### Step 3: Prepare Your Data

Place your `crop_yield.csv` file in the same directory as `app.py`. The CSV must contain these columns:
- Region
- Soil_Type
- Crop
- Rainfall_mm
- Temperature_Celsius
- Fertilizer_Used
- Irrigation_Used
- Weather_Condition
- Days_to_Harvest
- Yield_tons_per_hectare

### Step 3: Run the Backend Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

You should see:
```
 * Running on http://localhost:5000
```

### Step 4: Access the Website

Open your browser and navigate to:
```
http://localhost:5000
```

## 🎮 How to Use

### Predict Crop Yield
1. Click on the "🔮 Predict Yield" tab
2. Enter your farm conditions:
   - Crop type
   - Region
   - Soil type
   - Weather condition
   - Rainfall (mm)
   - Temperature (°C)
   - Days to harvest
   - Toggle fertilizer and irrigation usage
3. Click "⚡ Predict Crop Yield"
4. View the prediction and insights

### Retrain the Model
1. Click on the "🔄 Retrain Model" tab
2. Upload a CSV file by:
   - Clicking the upload box and selecting a file, OR
   - Dragging and dropping a CSV file
3. Wait for training to complete
4. View the new model metrics (R², RMSE, MAE)

### View Analysis
1. Click on the "📊 Analysis" tab
2. Explore visualizations:
   - Feature importance scores
   - Average yield by crop type
   - Impact of fertilizer and irrigation
   - Yield by soil type
   - Rainfall vs. crop yield correlation

## 📊 Model Information

- **Algorithm**: Random Forest Regressor
- **Trees**: 100 decision trees
- **Target Variable**: Yield_tons_per_hectare
- **Input Features**: 9 variables
- **Typical Performance**: R² ≈ 0.91, RMSE ≈ 0.4

## 🗂️ Project Structure

```
├── app.py                    # Flask backend server
├── agripredict.html         # Frontend web interface
├── crop_yield.csv           # Training dataset
├── crop_yield_model.py      # Original model training script
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── model.pkl                # Saved trained model (auto-created)
└── uploads/                 # Uploaded CSV files (auto-created)
```

## 🔧 API Endpoints

### POST /predict
Predicts crop yield for given conditions.

**Request:**
```json
{
  "crop": "Wheat",
  "region": "North",
  "soil_type": "Loam",
  "rainfall": 600,
  "temperature": 25,
  "fertilizer": "true",
  "irrigation": "false",
  "weather_condition": "Sunny",
  "days_to_harvest": 100
}
```

**Response:**
```json
{
  "prediction": 4.82,
  "insights": ["Growing conditions look favorable.", "..."],
  "unit": "tons/hectare"
}
```

### POST /retrain
Retrains model with uploaded CSV dataset.

**Request**: Form data with CSV file

**Response:**
```json
{
  "success": true,
  "message": "Model trained successfully",
  "metrics": {
    "r2": 0.9087,
    "rmse": 0.4093,
    "mae": 0.409,
    "mse": 0.1675,
    "train_size": 800000,
    "test_size": 200000,
    "total_samples": 1000000,
    "trained_at": "2024-01-15T10:30:45.123456"
  }
}
```

### GET /metrics
Returns current model performance metrics.

**Response:**
```json
{
  "r2": 0.9087,
  "rmse": 0.4093,
  "mae": 0.409,
  "mse": 0.1675,
  "train_size": 800000,
  "test_size": 200000,
  "total_samples": 1000000,
  "trained_at": "2024-01-15T10:30:45.123456"
}
```

### GET /model-info
Returns model metadata.

**Response:**
```json
{
  "model_type": "Random Forest Regressor",
  "n_estimators": 100,
  "status": "ready",
  "metrics": {...}
}
```

## 💡 Tips for Better Predictions

1. **Adequate Rainfall**: Rainfall is the most important factor (60.7% importance)
2. **Fertilizer Usage**: Using fertilizer increases yield significantly (~1.5 tons/ha)
3. **Irrigation**: Supplementing with irrigation can boost yield by ~1.2 tons/ha
4. **Seasonal Variations**: Temperature affects photosynthesis; optimal range is 20-30°C
5. **Soil Quality**: Different soil types have minor impact; Loam typically performs well

## 🔄 Retraining Tips

- Ensure your CSV has all 10 required columns
- Use at least 100 samples for meaningful training
- Ensure data quality and clean any NULL values
- The model will automatically split data: 80% training, 20% testing
- Wait for the training progress bar to complete before closing

## 🐛 Troubleshooting

**"Failed to connect to backend"**
- Make sure `python app.py` is running
- Check that the server is running on http://localhost:5000
- Check firewall settings

**"Model not loaded"**
- Ensure `crop_yield.csv` is in the same directory as `app.py`
- The model will train on first load (may take a minute)

**Retraining fails**
- Verify all required columns are in your CSV
- Check that the column names exactly match the required names
- Ensure there are no NULL values in the dataset

**Charts not loading**
- Check browser console for errors (F12)
- Make sure Chart.js CDN is accessible

## 📈 Performance Metrics Explanation

- **R² Score**: How well the model explains yield variance (0-1, higher is better)
- **RMSE**: Root Mean Squared Error in tons/hectare (lower is better)
- **MAE**: Mean Absolute Error in tons/hectare (average prediction error)
- **MSE**: Mean Squared Error (penalizes larger errors more)

## 📝 License

This project is open source and available for educational and commercial use.

## 👤 Author

Created as an agricultural technology solution for crop yield prediction and optimization.

---

For more information or support, please check the project documentation or contact the development team.
